import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount } from '@vue/test-utils';
import SnackCard from '../SnackCard.vue';
import type { Snack } from '../../api/types';
import { snacksApi } from '../../api/snacks';
import { votesApi } from '../../api/votes';

vi.mock('../../api/snacks', () => ({
  snacksApi: {
    consume: vi.fn(),
    get: vi.fn(),
  },
}));

vi.mock('../../api/votes', () => ({
  votesApi: {
    vote: vi.fn(),
    unvote: vi.fn(),
  },
}));

const mockStockedSnack: Snack = {
  id: 'snack-1',
  name: 'Crispy Pretzel Bites',
  category: 'savoury',
  quantity: 8,
  low_stock_threshold: 3,
  status: 'stocked',
  vote_count: 5,
  voted_by_me: false,
  created_at: '2026-01-01T00:00:00Z',
  updated_at: '2026-01-01T00:00:00Z',
};

const mockRunningLowSnack: Snack = {
  id: 'snack-2',
  name: 'Matcha Green Tea',
  category: 'drink',
  quantity: 2,
  low_stock_threshold: 4,
  status: 'running_low',
  vote_count: 12,
  voted_by_me: true,
  created_at: '2026-01-01T00:00:00Z',
  updated_at: '2026-01-01T00:00:00Z',
};

const mockGoneSnack: Snack = {
  id: 'snack-3',
  name: 'Caramel Macaron',
  category: 'sweet',
  quantity: 0,
  low_stock_threshold: 5,
  status: 'gone',
  vote_count: 9,
  voted_by_me: false,
  created_at: '2026-01-01T00:00:00Z',
  updated_at: '2026-01-01T00:00:00Z',
};

describe('SnackCard.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders snack title, category, quantity and status badge properly', () => {
    const wrapper = mount(SnackCard, {
      props: { snack: mockStockedSnack },
    });

    expect(wrapper.find('.snack-card__title').text()).toBe('Crispy Pretzel Bites');
    expect(wrapper.find('.snack-card__category-chip').text()).toBe('Savoury');
    expect(wrapper.find('.snack-card__quantity-num').text()).toBe('8');
    expect(wrapper.find('.snack-card__status-badge').text()).toContain('Stocked');
  });

  it('shows amber ribbon and running-low class for low stock snacks', () => {
    const wrapper = mount(SnackCard, {
      props: { snack: mockRunningLowSnack },
    });

    expect(wrapper.classes()).toContain('snack-card--running-low');
    expect(wrapper.find('.snack-card__ribbon').exists()).toBe(true);
    expect(wrapper.find('.snack-card__status-badge').text()).toContain('Running low');
  });

  it('mutes gone snacks and disables consume button and stepper', () => {
    const wrapper = mount(SnackCard, {
      props: { snack: mockGoneSnack },
    });

    expect(wrapper.classes()).toContain('snack-card--gone');
    expect(wrapper.find('.snack-card__status-badge').text()).toContain('Gone');

    const consumeBtn = wrapper.find('.snack-card__consume-btn');
    expect((consumeBtn.element as HTMLButtonElement).disabled).toBe(true);
    expect(consumeBtn.text()).toContain('Out of stock');

    const stepperBtns = wrapper.findAll('.snack-card__stepper-btn');
    stepperBtns.forEach((btn) => {
      expect((btn.element as HTMLButtonElement).disabled).toBe(true);
    });
  });

  it('stepper increments and decrements within valid bounds [1, min(qty, 10)]', async () => {
    const wrapper = mount(SnackCard, {
      props: { snack: mockStockedSnack }, // quantity = 8
    });

    const stepperValue = wrapper.find('.snack-card__stepper-value');
    const stepperBtns = wrapper.findAll('.snack-card__stepper-btn');
    const decBtn = stepperBtns[0]!;
    const incBtn = stepperBtns[1]!;

    expect(stepperValue.text()).toBe('1');
    expect((decBtn.element as HTMLButtonElement).disabled).toBe(true);

    // Increment
    await incBtn.trigger('click');
    expect(stepperValue.text()).toBe('2');
    expect((decBtn.element as HTMLButtonElement).disabled).toBe(false);

    // Decrement back to 1
    await decBtn.trigger('click');
    expect(stepperValue.text()).toBe('1');
    expect((decBtn.element as HTMLButtonElement).disabled).toBe(true);
  });

  it('handles consume successfully and emits update:snack and consumed events', async () => {
    const updatedSnack: Snack = { ...mockStockedSnack, quantity: 7 };
    vi.mocked(snacksApi.consume).mockResolvedValueOnce(updatedSnack);

    const wrapper = mount(SnackCard, {
      props: { snack: mockStockedSnack },
    });

    const consumeBtn = wrapper.find('.snack-card__consume-btn');
    await consumeBtn.trigger('click');

    expect(snacksApi.consume).toHaveBeenCalledWith('snack-1', { amount: 1 });
    await wrapper.vm.$nextTick();

    expect(wrapper.emitted('update:snack')).toBeTruthy();
    expect(wrapper.emitted('consumed')).toBeTruthy();
  });

  it('handles 409 INSUFFICIENT_STOCK: shakes card and refreshes from server', async () => {
    const conflictError = { code: 'INSUFFICIENT_STOCK', status: 409, message: 'Only 0 left' };
    vi.mocked(snacksApi.consume).mockRejectedValueOnce(conflictError);

    const freshServerSnack: Snack = { ...mockStockedSnack, quantity: 0, status: 'gone' };
    vi.mocked(snacksApi.get).mockResolvedValueOnce(freshServerSnack);

    const wrapper = mount(SnackCard, {
      props: { snack: mockStockedSnack },
    });

    const consumeBtn = wrapper.find('.snack-card__consume-btn');
    await consumeBtn.trigger('click');

    expect(snacksApi.consume).toHaveBeenCalledWith('snack-1', { amount: 1 });
    await wrapper.vm.$nextTick();

    // Verify card shaken and fresh data fetched
    expect(snacksApi.get).toHaveBeenCalledWith('snack-1');
    expect(wrapper.classes()).toContain('snack-card--shake');
  });

  it('toggles vote and calls vote/unvote API', async () => {
    vi.mocked(votesApi.vote).mockResolvedValueOnce({ vote_count: 6, voted_by_me: true });

    const wrapper = mount(SnackCard, {
      props: { snack: mockStockedSnack }, // voted_by_me is false
    });

    const voteBtn = wrapper.find('.snack-card__vote-btn');
    await voteBtn.trigger('click');

    expect(votesApi.vote).toHaveBeenCalledWith('snack-1');
    await wrapper.vm.$nextTick();

    expect(wrapper.emitted('update:snack')?.[0]?.[0]).toMatchObject({
      vote_count: 6,
      voted_by_me: true,
    });
  });
});
