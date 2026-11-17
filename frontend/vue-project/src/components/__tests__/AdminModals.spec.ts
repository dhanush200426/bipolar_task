import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount } from '@vue/test-utils';
import AddSnackModal from '../AddSnackModal.vue';
import EditSnackModal from '../EditSnackModal.vue';
import RestockModal from '../RestockModal.vue';
import DeleteConfirmDialog from '../DeleteConfirmDialog.vue';
import type { Snack } from '../../api/types';
import { snacksApi } from '../../api/snacks';

vi.mock('../../api/snacks', () => ({
  snacksApi: {
    create: vi.fn(),
    update: vi.fn(),
    restock: vi.fn(),
    delete: vi.fn(),
  },
}));

const mockSnack: Snack = {
  id: 'snack-100',
  name: 'Artisan Sourdough Pretzels',
  category: 'savoury',
  quantity: 15,
  low_stock_threshold: 5,
  status: 'stocked',
  vote_count: 8,
  voted_by_me: false,
  created_at: '2026-01-01T00:00:00Z',
  updated_at: '2026-01-01T00:00:00Z',
};

const mountOptions = {
  global: {
    stubs: {
      teleport: true,
    },
  },
};

describe('AddSnackModal.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('validates required fields before submitting', async () => {
    const wrapper = mount(AddSnackModal, {
      props: { isOpen: true },
      ...mountOptions,
    });

    // Submit with empty name
    const form = wrapper.find('form');
    await form.trigger('submit');

    expect(wrapper.find('.form-error').text()).toBe('Please provide a snack name');
    expect(snacksApi.create).not.toHaveBeenCalled();
  });

  it('displays inline error for duplicate snack name (SNACK_NAME_TAKEN)', async () => {
    vi.mocked(snacksApi.create).mockRejectedValueOnce({
      code: 'SNACK_NAME_TAKEN',
      message: 'Snack name already exists',
    });

    const wrapper = mount(AddSnackModal, {
      props: { isOpen: true },
      ...mountOptions,
    });

    await wrapper.find('#add-snack-name').setValue('Existing Snack');
    await wrapper.find('form').trigger('submit');

    await wrapper.vm.$nextTick();
    expect(wrapper.find('.form-error').text()).toBe('A snack with this name already exists in the pantry');
  });

  it('submits valid snack and emits created event', async () => {
    const createdSnack: Snack = { ...mockSnack, id: 'new-id', name: 'Fresh Berries', category: 'healthy-ish' };
    vi.mocked(snacksApi.create).mockResolvedValueOnce(createdSnack);

    const wrapper = mount(AddSnackModal, {
      props: { isOpen: true },
      ...mountOptions,
    });

    await wrapper.find('#add-snack-name').setValue('Fresh Berries');
    await wrapper.find('#add-snack-category').setValue('healthy-ish');
    await wrapper.find('#add-snack-quantity').setValue(12);
    await wrapper.find('#add-snack-threshold').setValue(4);

    await wrapper.find('form').trigger('submit');
    await wrapper.vm.$nextTick();

    expect(snacksApi.create).toHaveBeenCalledWith({
      name: 'Fresh Berries',
      category: 'healthy-ish',
      quantity: 12,
      low_stock_threshold: 4,
    });
    expect(wrapper.emitted('created')?.[0]?.[0]).toEqual(createdSnack);
  });
});

describe('EditSnackModal.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('populates fields and does NOT contain a quantity input', () => {
    const wrapper = mount(EditSnackModal, {
      props: { isOpen: true, snack: mockSnack },
      ...mountOptions,
    });

    expect((wrapper.find('#edit-snack-name').element as HTMLInputElement).value).toBe(mockSnack.name);
    expect((wrapper.find('#edit-snack-category').element as HTMLSelectElement).value).toBe(mockSnack.category);
    expect((wrapper.find('#edit-snack-threshold').element as HTMLInputElement).value).toBe('5');

    // Confirm quantity input does NOT exist in the form (only adjusted via Restock)
    expect(wrapper.find('#edit-snack-quantity').exists()).toBe(false);
  });

  it('submits updated values and emits updated event', async () => {
    const updatedSnack: Snack = { ...mockSnack, name: 'Renamed Pretzels', low_stock_threshold: 8 };
    vi.mocked(snacksApi.update).mockResolvedValueOnce(updatedSnack);

    const wrapper = mount(EditSnackModal, {
      props: { isOpen: true, snack: mockSnack },
      ...mountOptions,
    });

    await wrapper.find('#edit-snack-name').setValue('Renamed Pretzels');
    await wrapper.find('#edit-snack-threshold').setValue(8);
    await wrapper.find('form').trigger('submit');

    await wrapper.vm.$nextTick();
    expect(snacksApi.update).toHaveBeenCalledWith('snack-100', {
      name: 'Renamed Pretzels',
      category: 'savoury',
      low_stock_threshold: 8,
    });
    expect(wrapper.emitted('updated')?.[0]?.[0]).toEqual(updatedSnack);
  });
});

describe('RestockModal.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('chips increment amount and stepper updates correctly', async () => {
    const wrapper = mount(RestockModal, {
      props: { isOpen: true, snack: mockSnack },
      ...mountOptions,
    });

    const amountInput = wrapper.find('#restock-amount');
    expect((amountInput.element as HTMLInputElement).value).toBe('10');

    // Click +20 chip
    const chips = wrapper.findAll('.chip-btn');
    const chip20 = chips.find((c) => c.text().includes('+20'))!;
    await chip20.trigger('click');
    await wrapper.vm.$nextTick();

    expect((wrapper.vm as any).amount).toBe(30);
  });

  it('calls restock API and emits restocked event', async () => {
    const restockedSnack: Snack = { ...mockSnack, quantity: 25 };
    vi.mocked(snacksApi.restock).mockResolvedValueOnce(restockedSnack);

    const wrapper = mount(RestockModal, {
      props: { isOpen: true, snack: mockSnack },
      ...mountOptions,
    });

    await wrapper.find('#restock-amount').setValue(10);
    await wrapper.find('form').trigger('submit');

    await wrapper.vm.$nextTick();
    expect(snacksApi.restock).toHaveBeenCalledWith('snack-100', { amount: 10 });
    expect(wrapper.emitted('restocked')?.[0]?.[0]).toEqual(restockedSnack);
  });
});

describe('DeleteConfirmDialog.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('displays snack name and confirms deletion', async () => {
    vi.mocked(snacksApi.delete).mockResolvedValueOnce();

    const wrapper = mount(DeleteConfirmDialog, {
      props: { isOpen: true, snack: mockSnack },
      ...mountOptions,
    });

    expect(wrapper.find('.delete-dialog__desc').text()).toContain(mockSnack.name);

    const deleteBtn = wrapper.find('.btn-destructive');
    await deleteBtn.trigger('click');

    await wrapper.vm.$nextTick();
    expect(snacksApi.delete).toHaveBeenCalledWith('snack-100');
    expect(wrapper.emitted('deleted')?.[0]?.[0]).toBe('snack-100');
  });

  it('handles 404 gracefully when snack is already deleted', async () => {
    vi.mocked(snacksApi.delete).mockRejectedValueOnce({
      code: 'SNACK_NOT_FOUND',
      status: 404,
      message: 'Snack not found',
    });

    const wrapper = mount(DeleteConfirmDialog, {
      props: { isOpen: true, snack: mockSnack },
      ...mountOptions,
    });

    const deleteBtn = wrapper.find('.btn-destructive');
    await deleteBtn.trigger('click');

    await wrapper.vm.$nextTick();
    // Emits deleted so frontend removes the card from view without crashing
    expect(wrapper.emitted('deleted')?.[0]?.[0]).toBe('snack-100');
  });
});
