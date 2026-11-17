<template>
  <div class="snacks-view" ref="snacksViewRef">
    <!-- Page Header (Full scale across laptop) -->
    <header class="snacks-view__header">
      <div class="snacks-view__header-container">
        <div class="snacks-view__header-badge">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="header-badge__icon">
            <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z" />
            <line x1="3" y1="6" x2="21" y2="6" />
            <path d="M16 10a4 4 0 0 1-8 0" />
          </svg>
          <span>Pantry Vault</span>
        </div>
        <h1 class="snacks-view__title">Office Snack Vault</h1>
        <p class="snacks-view__subtitle">
          Browse all snacks, cast your votes, and fuel up. Everything in one unified catalog.
        </p>
      </div>
    </header>

    <!-- Sticky Filter & Control Bar (Full-scale edge-to-edge across laptop) -->
    <nav
      class="snacks-view__sticky-bar"
      :class="{ 'snacks-view__sticky-bar--pinned': isScrolledPastHeader }"
      aria-label="Snack catalog filters"
    >
      <div class="snacks-view__sticky-container">
        <!-- Top row of bar: Horizontally Scrollable Category Tabs -->
        <div class="snacks-view__tabs-wrapper" role="tablist" aria-label="Snack Categories">
          <button
            v-for="cat in categoryOptions"
            :key="cat.value"
            type="button"
            role="tab"
            :aria-selected="currentCategory === cat.value"
            class="snacks-view__tab-btn"
            :class="{ 'snacks-view__tab-btn--active': currentCategory === cat.value }"
            @click="selectCategory(cat.value)"
          >
            <span class="snacks-view__tab-icon" v-if="cat.icon" aria-hidden="true">{{ cat.icon }}</span>
            <span class="snacks-view__tab-label">{{ cat.label }}</span>
          </button>
        </div>

        <!-- Secondary row / Controls: Status filter, Search, Sort, and Item Count -->
        <div class="snacks-view__controls-row">
          <!-- Total Count Indicator -->
          <div class="snacks-view__count-badge" v-if="!isLoading && !error">
            <span class="count-num">{{ total }}</span>
            <span class="count-label">{{ total === 1 ? 'snack' : 'snacks' }}</span>
          </div>

          <!-- Debounced Search Input -->
          <div class="snacks-view__search-wrap">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2.5"
              class="snacks-view__search-icon"
              aria-hidden="true"
            >
              <circle cx="11" cy="11" r="8" />
              <line x1="21" y1="21" x2="16.65" y2="16.65" />
            </svg>
            <input
              v-model="searchInput"
              type="text"
              class="snacks-view__search-input"
              placeholder="Search snacks..."
              aria-label="Search snacks by name"
              @input="onSearchInput"
              @keydown.esc="clearSearch"
            />
            <button
              v-if="searchInput"
              type="button"
              class="snacks-view__search-clear"
              aria-label="Clear search input"
              title="Clear search"
              @click="clearSearch"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <line x1="18" y1="6" x2="6" y2="18" />
                <line x1="6" y1="6" x2="18" y2="18" />
              </svg>
            </button>
          </div>

          <!-- Status Filter Dropdown with Theme & Animations -->
          <div class="snacks-view__dropdown-wrap" ref="statusDropdownRef">
            <button
              type="button"
              class="snacks-dropdown-btn"
              :class="{
                'snacks-dropdown-btn--open': isStatusDropdownOpen,
                'snacks-dropdown-btn--filtered': currentStatus !== ''
              }"
              aria-haspopup="listbox"
              :aria-expanded="isStatusDropdownOpen"
              aria-label="Filter by stock status"
              @click="toggleStatusDropdown"
            >
              <span class="status-indicator-dot" :class="`dot--${currentStatus || 'all'}`" aria-hidden="true"></span>
              <span class="dropdown-btn-label">{{ currentStatusLabel }}</span>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="dropdown-chevron" :class="{ 'dropdown-chevron--flipped': isStatusDropdownOpen }">
                <polyline points="6 9 12 15 18 9" />
              </svg>
            </button>

            <!-- Dropdown Menu Animation -->
            <Transition name="filter-dropdown">
              <div
                v-if="isStatusDropdownOpen"
                class="snacks-dropdown-menu"
                role="listbox"
                aria-label="Stock status options"
              >
                <div class="dropdown-menu-header">Filter by Status</div>
                <button
                  v-for="opt in statusOptions"
                  :key="opt.value"
                  type="button"
                  role="option"
                  :aria-selected="currentStatus === opt.value"
                  class="dropdown-menu-item"
                  :class="{ 'dropdown-menu-item--selected': currentStatus === opt.value }"
                  @click="selectStatus(opt.value)"
                >
                  <span class="status-indicator-dot" :class="opt.dotClass" aria-hidden="true"></span>
                  <span class="item-label">{{ opt.label }}</span>
                  <svg v-if="currentStatus === opt.value" class="item-check" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                    <polyline points="20 6 9 17 4 12" />
                  </svg>
                </button>
              </div>
            </Transition>
          </div>

          <!-- Arranging Order / Sort Dropdown with Theme & Animations -->
          <div class="snacks-view__dropdown-wrap" ref="sortDropdownRef">
            <button
              type="button"
              class="snacks-dropdown-btn"
              :class="{
                'snacks-dropdown-btn--open': isSortDropdownOpen,
                'snacks-dropdown-btn--filtered': currentSortCombined !== 'name:asc'
              }"
              aria-haspopup="listbox"
              :aria-expanded="isSortDropdownOpen"
              aria-label="Sort snacks by arranging order"
              @click="toggleSortDropdown"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="sort-icon-prefix">
                <line x1="4" y1="6" x2="20" y2="6" />
                <line x1="4" y1="12" x2="14" y2="12" />
                <line x1="4" y1="18" x2="8" y2="18" />
              </svg>
              <span class="dropdown-btn-label">{{ currentSortLabel }}</span>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="dropdown-chevron" :class="{ 'dropdown-chevron--flipped': isSortDropdownOpen }">
                <polyline points="6 9 12 15 18 9" />
              </svg>
            </button>

            <!-- Dropdown Menu Animation -->
            <Transition name="filter-dropdown">
              <div
                v-if="isSortDropdownOpen"
                class="snacks-dropdown-menu snacks-dropdown-menu--sort"
                role="listbox"
                aria-label="Arranging order options"
              >
                <div class="dropdown-menu-header">Arranging Order</div>
                <button
                  v-for="opt in sortOptions"
                  :key="opt.value"
                  type="button"
                  role="option"
                  :aria-selected="currentSortCombined === opt.value"
                  class="dropdown-menu-item"
                  :class="{ 'dropdown-menu-item--selected': currentSortCombined === opt.value }"
                  @click="selectSort(opt.value)"
                >
                  <span class="item-label">{{ opt.label }}</span>
                  <svg v-if="currentSortCombined === opt.value" class="item-check" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                    <polyline points="20 6 9 17 4 12" />
                  </svg>
                </button>
              </div>
            </Transition>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content Area (Full Scale Grid) -->
    <main class="snacks-view__main" ref="gridContainerRef">
      <div class="snacks-view__container">
        <!-- Loading State: Skeleton Grid -->
        <div v-if="isLoading" class="snacks-grid snacks-grid--skeleton" aria-busy="true" aria-label="Loading snacks">
          <div v-for="i in 8" :key="`skeleton-${i}`" class="skeleton-card">
            <div class="skeleton-card__media skeleton-shimmer"></div>
            <div class="skeleton-card__body">
              <div class="skeleton-card__line skeleton-card__line--title skeleton-shimmer"></div>
              <div class="skeleton-card__line skeleton-card__line--sub skeleton-shimmer"></div>
              <div class="skeleton-card__footer skeleton-shimmer"></div>
            </div>
          </div>
        </div>

        <!-- Error State -->
        <ErrorState
          v-else-if="error"
          title="Couldn't load snacks"
          :message="error"
          :show-retry="true"
          @retry="fetchSnacks"
        />

        <!-- Empty State -->
        <EmptyState
          v-else-if="snacks.length === 0"
          title="No snacks match your filters"
          message="Try adjusting your category, status filter, or search keywords."
        >
          <template #action>
            <button
              type="button"
              class="snacks-view__clear-filters-btn"
              @click="clearAllFilters"
            >
              Clear filters
            </button>
          </template>
        </EmptyState>

        <!-- Snack Cards Grid: Unified All-In-One Page -->
        <div v-else class="snacks-grid" ref="cardsGridRef">
          <SnackCard
            v-for="snack in snacks"
            :key="snack.id"
            :snack="snack"
            :is-admin="authStore.isAdmin"
            :is-restocked="restockedSnackId === snack.id"
            :is-deleting="deletingSnackId === snack.id"
            @update:snack="onSnackUpdatedInList"
            @consumed="onSnackConsumed"
            @voted="onSnackVoted"
            @edit="openEditModal"
            @restock="openRestockModal"
            @delete="openDeleteModal"
          />
        </div>

        <!-- Single Page End Cap (Replaces 1,2,3 pagination) -->
        <div v-if="!isLoading && !error && snacks.length > 0" class="snacks-view__all-loaded">
          <div class="all-loaded-line"></div>
          <div class="all-loaded-content">
            <span class="all-loaded-dot"></span>
            <span class="all-loaded-text">All {{ snacks.length }} items displayed on one page</span>
          </div>
          <div class="all-loaded-line"></div>
        </div>
      </div>
    </main>

    <!-- Floating Action Button (FAB) -->
    <!-- Role-based: Member -> Snack of the Week; Admin -> + Add Snack -->
    <aside class="snacks-view__fab-container">
      <!-- Admin FAB: + Add snack -->
      <button
        v-if="authStore.isAdmin"
        type="button"
        class="snacks-view__fab snacks-view__fab--admin"
        aria-label="Add new snack"
        title="Add new snack"
        @click="isAddModalOpen = true"
      >
        <span class="snacks-view__fab-pulse" aria-hidden="true"></span>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="snacks-view__fab-icon">
          <line x1="12" y1="5" x2="12" y2="19" />
          <line x1="5" y1="12" x2="19" y2="12" />
        </svg>
        <span class="snacks-view__fab-text">Add snack</span>
      </button>

      <!-- Member FAB: Snack of the Week -->
      <button
        v-else
        type="button"
        class="snacks-view__fab snacks-view__fab--member"
        aria-label="Go to Snack of the Week"
        title="View Snack of the Week"
        @click="goToSnackOfTheWeek"
      >
        <span class="snacks-view__fab-pulse" aria-hidden="true"></span>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="snacks-view__fab-icon">
          <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
        </svg>
        <span class="snacks-view__fab-text">Snack of the Week</span>
      </button>
    </aside>

    <!-- Admin Modals (rendered ONLY when user is an admin) -->
    <template v-if="authStore.isAdmin">
      <AddSnackModal
        :is-open="isAddModalOpen"
        @close="isAddModalOpen = false"
        @created="onSnackCreated"
      />
      <EditSnackModal
        :is-open="isEditModalOpen"
        :snack="selectedSnackForEdit"
        @close="isEditModalOpen = false"
        @updated="onSnackEdited"
      />
      <RestockModal
        :is-open="isRestockModalOpen"
        :snack="selectedSnackForRestock"
        @close="isRestockModalOpen = false"
        @restocked="onSnackRestocked"
      />
      <DeleteConfirmDialog
        :is-open="isDeleteModalOpen"
        :snack="selectedSnackForDelete"
        @close="isDeleteModalOpen = false"
        @deleted="onSnackDeleted"
      />
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, onBeforeUnmount, nextTick } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import type { Snack, SnackCategoryType } from '../api/types';
import { snacksApi } from '../api/snacks';
import { useAuthStore } from '../stores/auth';
import { useToast } from '../composables/useToast';
import SnackCard from '../components/SnackCard.vue';
import EmptyState from '../components/EmptyState.vue';
import ErrorState from '../components/ErrorState.vue';
import AddSnackModal from '../components/AddSnackModal.vue';
import EditSnackModal from '../components/EditSnackModal.vue';
import RestockModal from '../components/RestockModal.vue';
import DeleteConfirmDialog from '../components/DeleteConfirmDialog.vue';
import { onClickOutside } from '../utils/clickOutside';
import gsap from 'gsap';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const { info: toastInfo } = useToast();

// Category tab definitions
const categoryOptions = [
  { label: 'All', value: '', icon: '🍪' },
  { label: 'Sweet', value: 'sweet', icon: '🍫' },
  { label: 'Savoury', value: 'savoury', icon: '🥨' },
  { label: 'Drink', value: 'drink', icon: '☕' },
  { label: 'Healthy-ish', value: 'healthy-ish', icon: '🍏' },
];

const VALID_CATEGORIES = new Set<string>(['sweet', 'savoury', 'drink', 'healthy-ish']);
const VALID_STATUSES = new Set<string>(['stocked', 'running_low', 'gone']);
const VALID_SORT_COLUMNS = new Set<string>(['name', 'quantity', 'votes', 'created_at']);
const VALID_ORDERS = new Set<string>(['asc', 'desc']);

// Filter & State Variables
const currentCategory = ref<string>('');
const currentStatus = ref<string>('');
const searchInput = ref<string>('');
const sortBy = ref<'name' | 'quantity' | 'votes' | 'created_at'>('name');
const sortOrder = ref<'asc' | 'desc'>('asc');
// Load all items in one continuous list (no page-by-page 1,2,3)
const pageSize = ref<number>(50);

// Combined sort string helper for the select dropdown
const currentSortCombined = computed({
  get: () => `${sortBy.value}:${sortOrder.value}`,
  set: (val: string) => {
    const parts = val.split(':');
    const col = parts[0];
    const ord = parts[1];
    if (col && VALID_SORT_COLUMNS.has(col)) {
      sortBy.value = col as any;
    }
    if (ord && VALID_ORDERS.has(ord)) {
      sortOrder.value = ord as any;
    }
  },
});

// Dropdown States, Options, and Handlers
const isStatusDropdownOpen = ref(false);
const isSortDropdownOpen = ref(false);
const statusDropdownRef = ref<HTMLElement | null>(null);
const sortDropdownRef = ref<HTMLElement | null>(null);

const statusOptions = [
  { value: '', label: 'Status: All', dotClass: 'dot--all' },
  { value: 'stocked', label: 'Stocked', dotClass: 'dot--stocked' },
  { value: 'running_low', label: 'Running Low', dotClass: 'dot--running-low' },
  { value: 'gone', label: 'Out of Stock', dotClass: 'dot--gone' },
];

const sortOptions = [
  { value: 'name:asc', label: 'Name: A to Z' },
  { value: 'name:desc', label: 'Name: Z to A' },
  { value: 'quantity:desc', label: 'Stock: High to Low' },
  { value: 'quantity:asc', label: 'Stock: Low to High' },
  { value: 'votes:desc', label: 'Votes: Most Popular' },
  { value: 'votes:asc', label: 'Votes: Least Popular' },
  { value: 'created_at:desc', label: 'Newest Added' },
  { value: 'created_at:asc', label: 'Oldest Added' },
];

const currentStatusLabel = computed(() => {
  const opt = statusOptions.find(o => o.value === currentStatus.value);
  return opt ? opt.label : 'Status: All';
});

const currentSortLabel = computed(() => {
  const opt = sortOptions.find(o => o.value === currentSortCombined.value);
  return opt ? opt.label : 'Sort by';
});

function toggleStatusDropdown() {
  isStatusDropdownOpen.value = !isStatusDropdownOpen.value;
  if (isStatusDropdownOpen.value) {
    isSortDropdownOpen.value = false;
  }
}

function toggleSortDropdown() {
  isSortDropdownOpen.value = !isSortDropdownOpen.value;
  if (isSortDropdownOpen.value) {
    isStatusDropdownOpen.value = false;
  }
}

function selectStatus(val: string) {
  if (currentStatus.value === val) {
    isStatusDropdownOpen.value = false;
    return;
  }
  currentStatus.value = val;
  isStatusDropdownOpen.value = false;
  onFilterChange();
}

function selectSort(val: string) {
  if (currentSortCombined.value === val) {
    isSortDropdownOpen.value = false;
    return;
  }
  currentSortCombined.value = val;
  isSortDropdownOpen.value = false;
  onSortChange();
}

onClickOutside(statusDropdownRef as any, () => {
  isStatusDropdownOpen.value = false;
});

onClickOutside(sortDropdownRef as any, () => {
  isSortDropdownOpen.value = false;
});

// Response Data
const snacks = ref<Snack[]>([]);
const total = ref<number>(0);
const isLoading = ref<boolean>(true);
const error = ref<string>('');

// Stale response tracking & AbortController
let currentRequestId = 0;
let abortController: AbortController | null = null;
let searchDebounceTimer: ReturnType<typeof setTimeout> | null = null;

// Modal & Action State
const isAddModalOpen = ref(false);
const isEditModalOpen = ref(false);
const selectedSnackForEdit = ref<Snack | null>(null);
const isRestockModalOpen = ref(false);
const selectedSnackForRestock = ref<Snack | null>(null);
const restockedSnackId = ref<string | null>(null);
const isDeleteModalOpen = ref(false);
const selectedSnackForDelete = ref<Snack | null>(null);
const deletingSnackId = ref<string | null>(null);

const isScrolledPastHeader = ref(false);
const snacksViewRef = ref<HTMLElement | null>(null);
const gridContainerRef = ref<HTMLElement | null>(null);
const cardsGridRef = ref<HTMLElement | null>(null);

// ---------------------------------------------------------------------------
// QUERY PARAMS PARSER & VALIDATOR
// ---------------------------------------------------------------------------
function parseQueryParams() {
  const qCategory = (route.query.category as string) || '';
  currentCategory.value = VALID_CATEGORIES.has(qCategory) ? qCategory : '';

  const qStatus = (route.query.status as string) || '';
  currentStatus.value = VALID_STATUSES.has(qStatus) ? qStatus : '';

  const qSearch = (route.query.q as string) || '';
  searchInput.value = qSearch;

  const qSortBy = (route.query.sort_by as string) || 'name';
  sortBy.value = (VALID_SORT_COLUMNS.has(qSortBy) ? qSortBy : 'name') as any;

  const qOrder = (route.query.order as string) || 'asc';
  sortOrder.value = (VALID_ORDERS.has(qOrder) ? qOrder : 'asc') as any;
}

/**
 * Push current filter state to the URL.
 * All items live on a single page, so page number is omitted.
 */
function syncUrl(replace = true) {
  const query: Record<string, string> = {};

  if (currentCategory.value) query.category = currentCategory.value;
  if (currentStatus.value) query.status = currentStatus.value;
  if (searchInput.value.trim()) query.q = searchInput.value.trim();
  if (sortBy.value !== 'name') query.sort_by = sortBy.value;
  if (sortOrder.value !== 'asc') query.order = sortOrder.value;

  if (replace) {
    router.replace({ query });
  } else {
    router.push({ query });
  }
}

// ---------------------------------------------------------------------------
// DATA FETCHING & STALE RESPONSE SHIELD
// ---------------------------------------------------------------------------
async function fetchSnacks() {
  isLoading.value = true;
  error.value = '';

  // Cancel prior in-flight request
  if (abortController) {
    abortController.abort();
  }
  abortController = new AbortController();
  const requestId = ++currentRequestId;

  try {
    const res = await snacksApi.list(
      {
        page: 1,
        page_size: pageSize.value,
        category: currentCategory.value || undefined,
        status: currentStatus.value || undefined,
        q: searchInput.value.trim() || undefined,
        sort_by: sortBy.value,
        order: sortOrder.value,
      },
      { signal: abortController.signal }
    );

    // If a newer request was dispatched while this was in flight, ignore this stale result
    if (requestId !== currentRequestId) {
      return;
    }

    snacks.value = res.items || (res as any).snacks || [];
    total.value = res.total || 0;

    // Trigger stagger animation on entered cards
    nextTick(() => {
      animateCards();
    });
  } catch (err: any) {
    // Abort errors are expected when cancelling stale requests
    if (err?.name === 'AbortError') {
      return;
    }
    if (requestId === currentRequestId) {
      error.value = err?.message || 'Failed to fetch pantry snacks. Please try again.';
    }
  } finally {
    if (requestId === currentRequestId) {
      isLoading.value = false;
    }
  }
}

// ---------------------------------------------------------------------------
// GSAP ENTRANCE ANIMATION
// ---------------------------------------------------------------------------
function animateCards() {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    return;
  }

  if (!cardsGridRef.value) return;
  const cards = cardsGridRef.value.querySelectorAll('.snack-card');
  if (cards.length === 0) return;

  gsap.fromTo(
    cards,
    {
      opacity: 0,
      y: 18,
    },
    {
      opacity: 1,
      y: 0,
      duration: 0.28,
      stagger: 0.04,
      ease: 'power2.out',
    }
  );
}

// ---------------------------------------------------------------------------
// FILTER / SEARCH HANDLERS
// ---------------------------------------------------------------------------
function selectCategory(category: string) {
  if (currentCategory.value === category) return;
  currentCategory.value = category;
  syncUrl(false);
  fetchSnacks();
}

function onFilterChange() {
  syncUrl(false);
  fetchSnacks();
}

function onSortChange() {
  syncUrl(false);
  fetchSnacks();
}

function onSearchInput() {
  if (searchDebounceTimer) {
    clearTimeout(searchDebounceTimer);
  }

  searchDebounceTimer = setTimeout(() => {
    syncUrl(true);
    fetchSnacks();
  }, 300);
}

function clearSearch() {
  if (!searchInput.value) return;
  searchInput.value = '';
  syncUrl(true);
  fetchSnacks();
}

function clearAllFilters() {
  currentCategory.value = '';
  currentStatus.value = '';
  searchInput.value = '';
  sortBy.value = 'name';
  sortOrder.value = 'asc';
  syncUrl(false);
  fetchSnacks();
}

// ---------------------------------------------------------------------------
// CARD MUTATION & CONCURRENCY EVENT HANDLERS
// ---------------------------------------------------------------------------
function onSnackUpdatedInList(updated: Snack) {
  const index = snacks.value.findIndex((s) => s.id === updated.id);
  if (index !== -1) {
    snacks.value[index] = updated;
  }
}

function onSnackConsumed(updated: Snack) {
  onSnackUpdatedInList(updated);
}

function onSnackVoted(updated: Snack) {
  onSnackUpdatedInList(updated);
}

// ---------------------------------------------------------------------------
// ADMIN MODAL HANDLERS
// ---------------------------------------------------------------------------
function openEditModal(snack: Snack) {
  selectedSnackForEdit.value = snack;
  isEditModalOpen.value = true;
}

function openRestockModal(snack: Snack) {
  selectedSnackForRestock.value = snack;
  isRestockModalOpen.value = true;
}

function openDeleteModal(snack: Snack) {
  selectedSnackForDelete.value = snack;
  isDeleteModalOpen.value = true;
}

async function onSnackCreated(created: Snack) {
  await fetchSnacks();
}

function onSnackEdited(updated: Snack) {
  onSnackUpdatedInList(updated);
}

function onSnackRestocked(updated: Snack) {
  onSnackUpdatedInList(updated);
  restockedSnackId.value = updated.id;
  setTimeout(() => {
    if (restockedSnackId.value === updated.id) {
      restockedSnackId.value = null;
    }
  }, 2000);
}

async function onSnackDeleted(snackId: string) {
  deletingSnackId.value = snackId;
  setTimeout(async () => {
    snacks.value = snacks.value.filter((s) => s.id !== snackId);
    total.value = Math.max(0, total.value - 1);
    deletingSnackId.value = null;
    await fetchSnacks();
  }, 350);
}

function goToSnackOfTheWeek() {
  router.push('/#snack-of-the-week');
}

// ---------------------------------------------------------------------------
// SCROLL LISTENER FOR STICKY BAR
// ---------------------------------------------------------------------------
function handleWindowScroll() {
  const scrollY = window.scrollY;
  isScrolledPastHeader.value = scrollY > 120;
}

// ---------------------------------------------------------------------------
// WATCH ROUTE & LIFECYCLE
// ---------------------------------------------------------------------------
watch(
  () => route.query,
  () => {
    parseQueryParams();
    fetchSnacks();
  }
);

onMounted(() => {
  parseQueryParams();
  fetchSnacks();
  window.addEventListener('scroll', handleWindowScroll, { passive: true });
});

onBeforeUnmount(() => {
  if (abortController) {
    abortController.abort();
  }
  if (searchDebounceTimer) {
    clearTimeout(searchDebounceTimer);
  }
  window.removeEventListener('scroll', handleWindowScroll);
});
</script>

<style scoped>
.snacks-view {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #FFFFFF;
  padding-bottom: var(--space-16);
}

/* Full-scale container across laptop */
.snacks-view__container {
  width: 100%;
  max-width: 100%;
  margin: 0;
  padding: 0 clamp(1.25rem, 3.5vw, 3.5rem);
  box-sizing: border-box;
}

/* Page Header */
.snacks-view__header {
  padding: 3rem clamp(1.25rem, 3.5vw, 3.5rem) 2rem;
  text-align: center;
  background: linear-gradient(180deg, #F6EFFC 0%, #FFFFFF 100%);
  border-bottom: 1px solid #EADBFA;
}

.snacks-view__header-container {
  max-width: 800px;
  margin: 0 auto;
}

.snacks-view__header-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  border-radius: var(--radius-full);
  background-color: #F1E8F8;
  color: #490982;
  border: 1px solid #E3D1F5;
  font-size: var(--text-xs);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  margin-bottom: var(--space-3);
}

.header-badge__icon {
  width: 14px;
  height: 14px;
}

.snacks-view__title {
  font-family: var(--font-display);
  font-size: clamp(2rem, 3.5vw, 3rem);
  font-weight: 800;
  color: #490982;
  margin: 0 0 var(--space-2);
  line-height: 1.15;
}

.snacks-view__subtitle {
  font-size: var(--text-base);
  color: #6C5D82;
  margin: 0;
  line-height: 1.6;
}

/* Sticky Filter & Control Bar */
.snacks-view__sticky-bar {
  position: sticky;
  top: 60px;
  z-index: 30;
  background-color: rgba(255, 255, 255, 0.96);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border-bottom: 1px solid #EADBFA;
  transition: all var(--transition-base);
}

.snacks-view__sticky-bar--pinned {
  box-shadow: 0 6px 18px rgba(73, 9, 130, 0.08);
}

.snacks-view__sticky-container {
  width: 100%;
  max-width: 100%;
  margin: 0;
  padding: var(--space-3) clamp(1.25rem, 3.5vw, 3.5rem);
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  box-sizing: border-box;
}

@media (min-width: 960px) {
  .snacks-view__sticky-container {
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
  }
}

/* Category Tabs */
.snacks-view__tabs-wrapper {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
  -ms-overflow-style: none;
  padding: 4px 0;
}

.snacks-view__tabs-wrapper::-webkit-scrollbar {
  display: none;
}

.snacks-view__tab-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  height: 42px;
  padding: 0 1.25rem;
  border-radius: var(--radius-full);
  border: 1.5px solid #E6D7F6;
  background-color: #FFFFFF;
  color: #190B2E;
  font-size: var(--text-sm);
  font-weight: 600;
  cursor: pointer;
  scroll-snap-align: start;
  flex-shrink: 0;
  transition: all var(--transition-fast);
  user-select: none;
}

.snacks-view__tab-btn:hover:not(.snacks-view__tab-btn--active) {
  background-color: #F8F4FC;
  border-color: #490982;
  color: #490982;
}

.snacks-view__tab-btn--active {
  background-color: #490982;
  border-color: #350661;
  color: #FFFFFF;
  font-weight: 700;
  box-shadow: 0 4px 12px rgba(73, 9, 130, 0.28);
}

.snacks-view__tab-icon {
  font-size: 16px;
}

/* Controls Row */
.snacks-view__controls-row {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  flex-wrap: wrap;
}

@media (min-width: 640px) {
  .snacks-view__controls-row {
    flex-wrap: nowrap;
  }
}

/* Item Count Badge */
.snacks-view__count-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.45rem 0.85rem;
  background-color: #F3EAFB;
  border-radius: var(--radius-full);
  border: 1px solid #E3D1F5;
  white-space: nowrap;
}

.count-num {
  font-weight: 700;
  color: #490982;
  font-size: var(--text-sm);
}

.count-label {
  font-size: 0.75rem;
  color: #6C5D82;
  font-weight: 600;
  text-transform: uppercase;
}

/* Search input */
.snacks-view__search-wrap {
  position: relative;
  display: flex;
  align-items: center;
  flex: 1;
  min-width: 200px;
}

.snacks-view__search-icon {
  position: absolute;
  left: 12px;
  width: 16px;
  height: 16px;
  color: #6C5D82;
  pointer-events: none;
}

.snacks-view__search-input {
  width: 100%;
  height: 42px;
  padding: 0 32px 0 38px;
  border-radius: var(--radius-full);
  border: 1.5px solid #E6D7F6;
  background-color: #FFFFFF;
  font-size: var(--text-sm);
  color: #190B2E;
  transition: all var(--transition-fast);
}

.snacks-view__search-input:focus {
  outline: none;
  border-color: #490982;
  box-shadow: 0 0 0 3px rgba(73, 9, 130, 0.15);
}

.snacks-view__search-clear {
  position: absolute;
  right: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  border: none;
  background: transparent;
  color: #6C5D82;
  cursor: pointer;
  border-radius: var(--radius-full);
}

.snacks-view__search-clear:hover {
  color: #190B2E;
  background: #F3EAFB;
}

.snacks-view__search-clear svg {
  width: 14px;
  height: 14px;
}

/* Custom Filter & Sort Dropdowns */
.snacks-view__dropdown-wrap {
  position: relative;
  flex-shrink: 0;
}

.snacks-dropdown-btn {
  height: 42px;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0 1rem;
  background-color: #FFFFFF;
  border: 1.5px solid #E6D7F6;
  border-radius: var(--radius-full);
  font-size: var(--text-sm);
  font-weight: 600;
  color: #190B2E;
  cursor: pointer;
  white-space: nowrap;
  box-shadow: 0 1px 3px rgba(73, 9, 130, 0.04);
  transition: all var(--transition-fast);
}

.snacks-dropdown-btn:hover {
  border-color: #490982;
  background-color: #FAF5FE;
  box-shadow: 0 3px 10px rgba(73, 9, 130, 0.08);
}

.snacks-dropdown-btn--open {
  border-color: #490982;
  background-color: #F1E8F8;
  color: #490982;
  box-shadow: 0 0 0 3px rgba(73, 9, 130, 0.15);
}

.snacks-dropdown-btn--filtered {
  border-color: #490982;
  background-color: #FAF5FE;
  color: #490982;
}

.sort-icon-prefix {
  width: 15px;
  height: 15px;
  color: #490982;
  flex-shrink: 0;
}

.dropdown-btn-label {
  font-size: var(--text-sm);
}

.dropdown-chevron {
  width: 15px;
  height: 15px;
  color: #6C5D82;
  transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), color 0.15s ease;
  flex-shrink: 0;
}

.dropdown-chevron--flipped {
  transform: rotate(180deg);
  color: #490982;
}

.status-indicator-dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  flex-shrink: 0;
}

.dot--all {
  background-color: #490982;
  box-shadow: 0 0 0 2px rgba(73, 9, 130, 0.2);
}

.dot--stocked {
  background-color: #10B981;
  box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.25);
}

.dot--running_low,
.dot--running-low {
  background-color: #F59E0B;
  box-shadow: 0 0 0 2px rgba(245, 158, 11, 0.25);
}

.dot--gone {
  background-color: #EF4444;
  box-shadow: 0 0 0 2px rgba(239, 68, 68, 0.25);
}

.snacks-dropdown-menu {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  min-width: 210px;
  background-color: #FFFFFF;
  border: 1px solid #EADBFA;
  border-radius: 16px;
  box-shadow: 0 16px 36px rgba(73, 9, 130, 0.15), 0 4px 12px rgba(0, 0, 0, 0.04);
  padding: 6px;
  z-index: 50;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

.snacks-dropdown-menu--sort {
  min-width: 220px;
}

.dropdown-menu-header {
  font-size: 0.6875rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #6C5D82;
  padding: 0.5rem 0.75rem 0.35rem;
}

.dropdown-menu-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 0.65rem;
  padding: 0.55rem 0.75rem;
  border: none;
  background: transparent;
  border-radius: 10px;
  font-size: var(--text-sm);
  font-weight: 500;
  color: #190B2E;
  text-align: left;
  cursor: pointer;
  transition: all 0.15s ease;
}

.dropdown-menu-item:hover {
  background-color: #FAF5FE;
  color: #490982;
  transform: translateX(2px);
}

.dropdown-menu-item--selected {
  background-color: #F1E8F8;
  color: #490982;
  font-weight: 700;
}

.item-label {
  flex: 1;
}

.item-check {
  width: 16px;
  height: 16px;
  color: #490982;
  flex-shrink: 0;
}

/* Dropdown Animation */
.filter-dropdown-enter-active,
.filter-dropdown-leave-active {
  transition: opacity 0.22s cubic-bezier(0.16, 1, 0.3, 1),
              transform 0.22s cubic-bezier(0.16, 1, 0.3, 1);
  transform-origin: top right;
}

.filter-dropdown-enter-from,
.filter-dropdown-leave-to {
  opacity: 0;
  transform: translateY(-8px) scale(0.96);
}

/* Main Content Area */
.snacks-view__main {
  flex: 1;
  padding-top: var(--space-6);
}

/* Responsive Grid across laptop */
.snacks-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.75rem;
}

@media (min-width: 600px) {
  .snacks-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 992px) {
  .snacks-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (min-width: 1300px) {
  .snacks-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (min-width: 1600px) {
  .snacks-grid {
    grid-template-columns: repeat(5, 1fr);
  }
}

/* All-Loaded Single Page Footer */
.snacks-view__all-loaded {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
  margin-top: 3.5rem;
  margin-bottom: 2rem;
}

.all-loaded-line {
  flex: 1;
  height: 1px;
  background-color: #E6D7F6;
}

.all-loaded-content {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.4rem 1rem;
  background-color: #FAF7FD;
  border: 1px solid #E6D7F6;
  border-radius: var(--radius-full);
}

.all-loaded-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #490982;
}

.all-loaded-text {
  font-size: 0.85rem;
  font-weight: 600;
  color: #6C5D82;
}

/* Clear Filters Button in EmptyState */
.snacks-view__clear-filters-btn {
  height: 44px;
  padding: 0 var(--space-6);
  background-color: #490982;
  color: #FFFFFF;
  border: none;
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
  font-weight: 700;
  cursor: pointer;
  transition: all var(--transition-fast);
  box-shadow: 0 4px 12px rgba(73, 9, 130, 0.25);
}

.snacks-view__clear-filters-btn:hover {
  background-color: #350661;
  transform: translateY(-1px);
}

/* Skeleton Loading Grid */
.skeleton-card {
  background: #FFFFFF;
  border-radius: var(--radius-xl);
  padding: var(--space-5);
  border: 1.5px solid #F0E6F8;
  display: flex;
  flex-direction: column;
  height: 320px;
}

.skeleton-card__media {
  height: 140px;
  border-radius: var(--radius-lg);
  margin-bottom: var(--space-4);
}

.skeleton-card__body {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.skeleton-card__line {
  border-radius: var(--radius-sm);
}

.skeleton-card__line--title {
  height: 22px;
  width: 75%;
}

.skeleton-card__line--sub {
  height: 16px;
  width: 45%;
}

.skeleton-card__footer {
  margin-top: auto;
  height: 42px;
  border-radius: var(--radius-md);
}

.skeleton-shimmer {
  background: linear-gradient(
    90deg,
    rgba(73, 9, 130, 0.04) 0%,
    rgba(73, 9, 130, 0.08) 50%,
    rgba(73, 9, 130, 0.04) 100%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

/* Floating Action Button (FAB) */
.snacks-view__fab-container {
  position: fixed;
  bottom: calc(var(--space-6) + env(safe-area-inset-bottom, 0px));
  right: calc(var(--space-6) + env(safe-area-inset-right, 0px));
  z-index: 40;
}

.snacks-view__fab {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  height: 52px;
  padding: 0 var(--space-5);
  border-radius: var(--radius-full);
  border: none;
  font-family: var(--font-body);
  font-size: var(--text-sm);
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(73, 9, 130, 0.35);
  transition: transform var(--transition-fast), box-shadow var(--transition-fast);
  user-select: none;
}

.snacks-view__fab:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(73, 9, 130, 0.45);
}

.snacks-view__fab:active {
  transform: translateY(0);
}

/* Admin FAB */
.snacks-view__fab--admin {
  background-color: #490982;
  color: #FFFFFF;
}

.snacks-view__fab--admin .snacks-view__fab-pulse {
  position: absolute;
  inset: 0;
  border-radius: var(--radius-full);
  animation: fabRingPurple 2.2s infinite ease-out;
  pointer-events: none;
}

@keyframes fabRingPurple {
  0% { box-shadow: 0 0 0 0 rgba(73, 9, 130, 0.55); }
  70% { box-shadow: 0 0 0 16px rgba(73, 9, 130, 0); }
  100% { box-shadow: 0 0 0 0 rgba(73, 9, 130, 0); }
}

/* Member FAB */
.snacks-view__fab--member {
  background-color: #9B51E0;
  color: #FFFFFF;
}

.snacks-view__fab--member .snacks-view__fab-pulse {
  position: absolute;
  inset: 0;
  border-radius: var(--radius-full);
  animation: fabRingViolet 2.2s infinite ease-out;
  pointer-events: none;
}

@keyframes fabRingViolet {
  0% { box-shadow: 0 0 0 0 rgba(155, 81, 224, 0.6); }
  70% { box-shadow: 0 0 0 16px rgba(155, 81, 224, 0); }
  100% { box-shadow: 0 0 0 0 rgba(155, 81, 224, 0); }
}

.snacks-view__fab-icon {
  width: 20px;
  height: 20px;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}

@media (prefers-reduced-motion: reduce) {
  .skeleton-shimmer {
    animation: none;
  }
}
</style>
