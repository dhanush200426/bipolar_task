<template>
  <nav class="pagination" aria-label="Pagination Navigation" v-if="totalPages > 1 || total > 0">
    <!-- Info label: "Page 2 of 5, 53 snacks" -->
    <div class="pagination__info" aria-live="polite">
      Page <span class="pagination__current-bold">{{ currentPage }}</span> of
      <span class="pagination__current-bold">{{ totalPages || 1 }}</span>
      <span class="pagination__total-count"> ({{ total }} {{ total === 1 ? 'snack' : 'snacks' }})</span>
    </div>

    <!-- Controls Row -->
    <div class="pagination__controls">
      <!-- Previous Button -->
      <button
        type="button"
        class="pagination__btn pagination__btn--prev"
        :disabled="currentPage <= 1"
        :aria-disabled="currentPage <= 1"
        aria-label="Previous page"
        @click="goToPage(currentPage - 1)"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="pagination__icon" aria-hidden="true">
          <polyline points="15 18 9 12 15 6" />
        </svg>
        <span class="pagination__btn-text">Prev</span>
      </button>

      <!-- Page Numbers -->
      <div class="pagination__pages" role="list">
        <template v-for="(item, index) in visiblePages" :key="index">
          <!-- Ellipsis -->
          <span v-if="item === '...'" class="pagination__ellipsis" aria-hidden="true">
            &hellip;
          </span>

          <!-- Page Button -->
          <button
            v-else
            type="button"
            class="pagination__page-btn"
            :class="{ 'pagination__page-btn--active': item === currentPage }"
            :aria-label="`Page ${item}`"
            :aria-current="item === currentPage ? 'page' : undefined"
            @click="goToPage(item as number)"
          >
            {{ item }}
          </button>
        </template>
      </div>

      <!-- Next Button -->
      <button
        type="button"
        class="pagination__btn pagination__btn--next"
        :disabled="currentPage >= totalPages || totalPages === 0"
        :aria-disabled="currentPage >= totalPages || totalPages === 0"
        aria-label="Next page"
        @click="goToPage(currentPage + 1)"
      >
        <span class="pagination__btn-text">Next</span>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="pagination__icon" aria-hidden="true">
          <polyline points="9 18 15 12 9 6" />
        </svg>
      </button>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  currentPage: number;
  totalPages: number;
  total: number;
}>();

const emit = defineEmits<{
  (e: 'change', page: number): void;
}>();

function goToPage(page: number) {
  if (page >= 1 && page <= props.totalPages && page !== props.currentPage) {
    emit('change', page);
  }
}

/**
 * Computes a list of visible page numbers and ellipses.
 * e.g. [1, 2, 3, 4, 5] or [1, '...', 4, 5, 6, '...', 10]
 */
const visiblePages = computed(() => {
  const current = props.currentPage;
  const total = props.totalPages;
  if (total <= 7) {
    return Array.from({ length: total }, (_, i) => i + 1);
  }

  const pages: (number | string)[] = [];
  pages.push(1);

  if (current > 3) {
    pages.push('...');
  }

  const start = Math.max(2, current - 1);
  const end = Math.min(total - 1, current + 1);

  for (let i = start; i <= end; i++) {
    pages.push(i);
  }

  if (current < total - 2) {
    pages.push('...');
  }

  pages.push(total);

  return pages;
});
</script>

<style scoped>
.pagination {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--space-3);
  padding: var(--space-6) var(--space-4);
  margin-top: var(--space-6);
}

@media (min-width: 640px) {
  .pagination {
    flex-direction: row;
    justify-content: space-between;
  }
}

.pagination__info {
  font-size: var(--text-sm);
  color: var(--color-muted);
}

.pagination__current-bold {
  font-weight: 700;
  color: var(--color-charcoal);
}

.pagination__total-count {
  margin-left: 4px;
  font-weight: 500;
}

.pagination__controls {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.pagination__btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  height: 40px;
  padding: 0 var(--space-4);
  background-color: #ffffff;
  border: 1.5px solid rgba(31, 27, 24, 0.12);
  border-radius: var(--radius-md);
  color: var(--color-charcoal);
  font-size: var(--text-sm);
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-fast);
  min-width: var(--touch-target, 44px);
}

.pagination__btn:hover:not(:disabled) {
  background-color: var(--color-cream);
  border-color: var(--color-tomato);
  color: var(--color-tomato);
}

.pagination__btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  background-color: rgba(31, 27, 24, 0.04);
}

.pagination__icon {
  width: 16px;
  height: 16px;
}

.pagination__pages {
  display: flex;
  align-items: center;
  gap: 4px;
}

.pagination__page-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 38px;
  border-radius: var(--radius-md);
  border: 1px solid transparent;
  background: transparent;
  color: var(--color-charcoal);
  font-size: var(--text-sm);
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.pagination__page-btn:hover:not(.pagination__page-btn--active) {
  background-color: var(--color-peach);
  color: var(--color-tomato);
}

.pagination__page-btn--active {
  background-color: var(--color-tomato);
  color: #ffffff;
  font-weight: 700;
  box-shadow: 0 2px 4px rgba(228, 71, 43, 0.3);
}

.pagination__ellipsis {
  padding: 0 6px;
  color: var(--color-muted);
  user-select: none;
}
</style>
