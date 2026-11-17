import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import Pagination from '../Pagination.vue';

describe('Pagination.vue', () => {
  it('renders page info correctly', () => {
    const wrapper = mount(Pagination, {
      props: {
        currentPage: 2,
        totalPages: 5,
        total: 53,
      },
    });

    expect(wrapper.find('.pagination__info').text()).toContain('Page 2 of 5 (53 snacks)');
  });

  it('disables previous button on first page and next button on last page', () => {
    const wrapperFirst = mount(Pagination, {
      props: {
        currentPage: 1,
        totalPages: 5,
        total: 50,
      },
    });

    const prevBtn = wrapperFirst.find('.pagination__btn--prev');
    const nextBtn = wrapperFirst.find('.pagination__btn--next');

    expect((prevBtn.element as HTMLButtonElement).disabled).toBe(true);
    expect((nextBtn.element as HTMLButtonElement).disabled).toBe(false);

    const wrapperLast = mount(Pagination, {
      props: {
        currentPage: 5,
        totalPages: 5,
        total: 50,
      },
    });

    expect((wrapperLast.find('.pagination__btn--prev').element as HTMLButtonElement).disabled).toBe(false);
    expect((wrapperLast.find('.pagination__btn--next').element as HTMLButtonElement).disabled).toBe(true);
  });

  it('emits change event when clicking next or a page number', async () => {
    const wrapper = mount(Pagination, {
      props: {
        currentPage: 2,
        totalPages: 5,
        total: 50,
      },
    });

    const nextBtn = wrapper.find('.pagination__btn--next');
    await nextBtn.trigger('click');

    expect(wrapper.emitted('change')).toBeTruthy();
    expect(wrapper.emitted('change')?.[0]).toEqual([3]);

    const page1Btn = wrapper.findAll('.pagination__page-btn').find((btn) => btn.text() === '1');
    expect(page1Btn).toBeTruthy();
    await page1Btn?.trigger('click');

    expect(wrapper.emitted('change')?.[1]).toEqual([1]);
  });
});
