<template>
  <Teleport to="body">
    <div
      v-if="isOpen"
      class="modal-backdrop"
      role="presentation"
      @click.self="handleClose"
    >
      <div
        ref="modalRef"
        class="modal-dialog modal-dialog--sheet"
        role="dialog"
        aria-modal="true"
        aria-labelledby="add-snack-title"
        tabindex="-1"
      >
        <!-- Modal Drag Handle for Mobile Bottom Sheet -->
        <div class="modal-handle-bar" aria-hidden="true"></div>

        <!-- Modal Header -->
        <div class="modal-header">
          <div class="modal-header__title-group">
            <div class="modal-header__icon" aria-hidden="true">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <circle cx="12" cy="12" r="10" />
                <line x1="12" y1="8" x2="12" y2="16" />
                <line x1="8" y1="12" x2="16" y2="12" />
              </svg>
            </div>
            <h2 id="add-snack-title" class="modal-title">Add New Snack</h2>
          </div>
          <button
            type="button"
            class="modal-close-btn"
            aria-label="Close dialog"
            title="Close dialog (Esc)"
            @click="handleClose"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
          </button>
        </div>

        <!-- Modal Form -->
        <form @submit.prevent="handleSubmit" class="modal-form" novalidate>
          <!-- Name Field -->
          <div class="form-group">
            <label for="add-snack-name" class="form-label">
              Snack Name <span class="required-star">*</span>
            </label>
            <input
              id="add-snack-name"
              ref="nameInputRef"
              v-model="name"
              type="text"
              class="form-input"
              :class="{ 'form-input--error': errors.name }"
              placeholder="e.g. Sea Salt Dark Chocolate Chips"
              maxlength="255"
              required
              :disabled="isSubmitting"
              @input="errors.name = ''"
            />
            <span v-if="errors.name" class="form-error" role="alert">{{ errors.name }}</span>
          </div>

          <!-- Category Field -->
          <div class="form-group">
            <label for="add-snack-category" class="form-label">
              Category <span class="required-star">*</span>
            </label>
            <select
              id="add-snack-category"
              v-model="category"
              class="form-select"
              required
              :disabled="isSubmitting"
            >
              <option value="sweet">Sweet</option>
              <option value="savoury">Savoury</option>
              <option value="drink">Drink</option>
              <option value="healthy-ish">Healthy-ish</option>
            </select>
          </div>

          <!-- Quantity & Low Stock Threshold Grid -->
          <div class="form-row">
            <div class="form-group">
              <label for="add-snack-quantity" class="form-label">
                Initial Stock <span class="required-star">*</span>
              </label>
              <input
                id="add-snack-quantity"
                v-model.number="quantity"
                type="number"
                min="0"
                class="form-input"
                :class="{ 'form-input--error': errors.quantity }"
                required
                :disabled="isSubmitting"
                @input="errors.quantity = ''"
              />
              <span v-if="errors.quantity" class="form-error" role="alert">{{ errors.quantity }}</span>
            </div>

            <div class="form-group">
              <label for="add-snack-threshold" class="form-label">
                Low Stock Alert At
              </label>
              <input
                id="add-snack-threshold"
                v-model.number="lowStockThreshold"
                type="number"
                min="0"
                class="form-input"
                :class="{ 'form-input--error': errors.threshold }"
                :disabled="isSubmitting"
                @input="errors.threshold = ''"
              />
              <span v-if="errors.threshold" class="form-error" role="alert">{{ errors.threshold }}</span>
            </div>
          </div>

          <!-- Global Form Error Message -->
          <div v-if="globalError" class="modal-form__error-banner" role="alert">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="error-banner__icon">
              <circle cx="12" cy="12" r="10" />
              <line x1="12" y1="8" x2="12" y2="12" />
              <line x1="12" y1="16" x2="12.01" y2="16" />
            </svg>
            <span>{{ globalError }}</span>
          </div>

          <!-- Modal Actions -->
          <div class="modal-actions">
            <button
              type="button"
              class="btn-secondary"
              :disabled="isSubmitting"
              @click="handleClose"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="btn-primary"
              :disabled="isSubmitting"
            >
              <svg v-if="isSubmitting" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="btn-spinner">
                <circle cx="12" cy="12" r="10" stroke-opacity="0.25" />
                <path d="M12 2a10 10 0 0 1 10 10" />
              </svg>
              <span>{{ isSubmitting ? 'Adding...' : 'Add Snack' }}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, reactive, watch, toRef } from 'vue';
import type { Snack, SnackCategoryType } from '../api/types';
import { snacksApi } from '../api/snacks';
import { useToast } from '../composables/useToast';
import { useModalAccessibility } from '../composables/useModalAccessibility';

const props = defineProps<{
  isOpen: boolean;
}>();

const emit = defineEmits<{
  (e: 'close'): void;
  (e: 'created', snack: Snack): void;
}>();

const { success: toastSuccess } = useToast();

const modalRef = ref<HTMLElement | null>(null);
const nameInputRef = ref<HTMLInputElement | null>(null);

const name = ref('');
const category = ref<SnackCategoryType>('sweet');
const quantity = ref(10);
const lowStockThreshold = ref(5);
const isSubmitting = ref(false);
const globalError = ref('');

const errors = reactive({
  name: '',
  quantity: '',
  threshold: '',
});

// Setup focus trap, esc listener, return focus, and body scroll lock
useModalAccessibility({
  isOpen: toRef(props, 'isOpen'),
  modalRef,
  onClose: handleClose,
  initialFocusRef: nameInputRef,
});

// Reset form when modal opens
watch(
  () => props.isOpen,
  (val) => {
    if (val) {
      name.value = '';
      category.value = 'sweet';
      quantity.value = 10;
      lowStockThreshold.value = 5;
      globalError.value = '';
      errors.name = '';
      errors.quantity = '';
      errors.threshold = '';
    }
  }
);

function handleClose() {
  if (!isSubmitting.value) {
    emit('close');
  }
}

async function handleSubmit() {
  errors.name = '';
  errors.quantity = '';
  errors.threshold = '';
  globalError.value = '';

  const trimmedName = name.value.trim();
  if (!trimmedName) {
    errors.name = 'Please provide a snack name';
    nameInputRef.value?.focus();
    return;
  }

  if (trimmedName.length > 255) {
    errors.name = 'Snack name must be 255 characters or fewer';
    nameInputRef.value?.focus();
    return;
  }

  if (quantity.value === undefined || quantity.value === null || isNaN(quantity.value) || quantity.value < 0) {
    errors.quantity = 'Quantity must be 0 or greater';
    return;
  }

  if (lowStockThreshold.value === undefined || lowStockThreshold.value === null || isNaN(lowStockThreshold.value) || lowStockThreshold.value < 0) {
    errors.threshold = 'Threshold must be 0 or greater';
    return;
  }

  isSubmitting.value = true;

  try {
    const created = await snacksApi.create({
      name: trimmedName,
      category: category.value,
      quantity: Math.floor(quantity.value),
      low_stock_threshold: Math.floor(lowStockThreshold.value),
    });

    toastSuccess(`Added "${created.name}" to the pantry!`);
    emit('created', created);
    emit('close');
  } catch (err: any) {
    // Show inline server error for duplicate snack name
    if (
      err?.code === 'SNACK_NAME_TAKEN' ||
      err?.code === 'DUPLICATE_NAME' ||
      err?.message?.toLowerCase().includes('already exists')
    ) {
      errors.name = 'A snack with this name already exists in the pantry';
      nameInputRef.value?.focus();
    } else {
      globalError.value = err?.message || 'Failed to add snack. Please try again.';
    }
  } finally {
    isSubmitting.value = false;
  }
}
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  inset: 0;
  background-color: rgba(31, 27, 24, 0.6);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-4);
  z-index: 100;
  animation: fadeIn 0.2s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal-dialog {
  background: #ffffff;
  border-radius: var(--radius-2xl);
  width: 100%;
  max-width: 480px;
  box-shadow: var(--shadow-xl);
  border: 1px solid rgba(31, 27, 24, 0.08);
  overflow: hidden;
  animation: scaleUp 0.25s ease-out;
}

@keyframes scaleUp {
  from {
    transform: scale(0.96) translateY(8px);
    opacity: 0;
  }
  to {
    transform: scale(1) translateY(0);
    opacity: 1;
  }
}

/* Mobile Bottom Sheet Style */
@media (max-width: 640px) {
  .modal-backdrop {
    align-items: flex-end;
    padding: 0;
  }

  .modal-dialog--sheet {
    max-width: 100%;
    border-bottom-left-radius: 0;
    border-bottom-right-radius: 0;
    max-height: 90vh;
    overflow-y: auto;
    animation: slideUpSheet 0.28s cubic-bezier(0.16, 1, 0.3, 1);
    padding-bottom: env(safe-area-inset-bottom, 16px);
  }

  @keyframes slideUpSheet {
    from {
      transform: translateY(100%);
    }
    to {
      transform: translateY(0);
    }
  }

  .modal-handle-bar {
    width: 40px;
    height: 5px;
    background-color: rgba(31, 27, 24, 0.2);
    border-radius: var(--radius-full);
    margin: 10px auto 4px;
    display: block;
  }
}

.modal-handle-bar {
  display: none;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-4) var(--space-6);
  background: var(--color-cream);
  border-bottom: 1px solid rgba(31, 27, 24, 0.08);
}

.modal-header__title-group {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.modal-header__icon {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-md);
  background: var(--color-peach);
  color: var(--color-tomato);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-header__icon svg {
  width: 18px;
  height: 18px;
}

.modal-title {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  font-weight: 700;
  color: var(--color-charcoal);
  margin: 0;
}

.modal-close-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: transparent;
  border: none;
  border-radius: var(--radius-full);
  color: var(--color-muted);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.modal-close-btn:hover {
  background: rgba(31, 27, 24, 0.08);
  color: var(--color-charcoal);
}

.modal-close-btn svg {
  width: 18px;
  height: 18px;
}

.modal-form {
  padding: var(--space-6);
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-4);
}

.form-label {
  font-size: var(--text-xs);
  font-weight: 700;
  color: var(--color-charcoal);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.required-star {
  color: var(--color-danger);
}

.form-input,
.form-select {
  width: 100%;
  height: 44px;
  padding: 0 var(--space-3);
  background: #ffffff;
  border: 1.5px solid rgba(31, 27, 24, 0.16);
  border-radius: var(--radius-md);
  font-family: var(--font-body);
  font-size: var(--text-base);
  color: var(--color-charcoal);
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
}

.form-input:focus,
.form-select:focus {
  outline: none;
  border-color: var(--color-tomato);
  box-shadow: 0 0 0 3px rgba(228, 71, 43, 0.15);
}

.form-input--error {
  border-color: var(--color-danger);
}

.form-error {
  font-size: var(--text-xs);
  color: var(--color-danger);
  font-weight: 600;
}

.modal-form__error-banner {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-3);
  background-color: #FDF2F2;
  border: 1px solid rgba(211, 47, 47, 0.25);
  border-radius: var(--radius-md);
  color: var(--color-danger);
  font-size: var(--text-sm);
}

.error-banner__icon {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.modal-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: var(--space-3);
  margin-top: var(--space-2);
}

.btn-secondary {
  height: 44px;
  padding: 0 var(--space-5);
  background: transparent;
  border: 1.5px solid rgba(31, 27, 24, 0.16);
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
  font-weight: 600;
  color: var(--color-charcoal);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.btn-secondary:hover:not(:disabled) {
  background: var(--color-cream);
  border-color: rgba(31, 27, 24, 0.3);
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  height: 44px;
  padding: 0 var(--space-6);
  background: var(--color-tomato);
  border: none;
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
  font-weight: 700;
  color: #ffffff;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(228, 71, 43, 0.3);
  transition: all var(--transition-fast);
}

.btn-primary:hover:not(:disabled) {
  background: var(--color-chili);
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(228, 71, 43, 0.4);
}

.btn-primary:disabled,
.btn-secondary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-spinner {
  width: 16px;
  height: 16px;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  100% { transform: rotate(360deg); }
}

@media (prefers-reduced-motion: reduce) {
  .modal-backdrop,
  .modal-dialog,
  .modal-dialog--sheet {
    animation: none;
  }
}
</style>
