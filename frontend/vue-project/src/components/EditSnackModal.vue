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
        aria-labelledby="edit-snack-title"
        tabindex="-1"
      >
        <!-- Mobile Bottom Sheet Handle -->
        <div class="modal-handle-bar" aria-hidden="true"></div>

        <!-- Modal Header -->
        <div class="modal-header">
          <div class="modal-header__title-group">
            <div class="modal-header__icon" aria-hidden="true">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
              </svg>
            </div>
            <h2 id="edit-snack-title" class="modal-title">Edit Snack</h2>
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

        <!-- Modal Form (name, category, low_stock_threshold ONLY) -->
        <form @submit.prevent="handleSubmit" class="modal-form" novalidate>
          <div class="modal-form__note">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="note-icon" aria-hidden="true">
              <circle cx="12" cy="12" r="10" />
              <line x1="12" y1="16" x2="12" y2="12" />
              <line x1="12" y1="8" x2="12.01" y2="8" />
            </svg>
            <span>Stock quantity ({{ snack?.quantity ?? 0 }}) is adjusted via the <strong>Restock</strong> control.</span>
          </div>

          <!-- Name Field -->
          <div class="form-group">
            <label for="edit-snack-name" class="form-label">
              Snack Name <span class="required-star">*</span>
            </label>
            <input
              id="edit-snack-name"
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
            <label for="edit-snack-category" class="form-label">
              Category <span class="required-star">*</span>
            </label>
            <select
              id="edit-snack-category"
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

          <!-- Low Stock Threshold Field -->
          <div class="form-group">
            <label for="edit-snack-threshold" class="form-label">
              Low Stock Alert Threshold <span class="required-star">*</span>
            </label>
            <input
              id="edit-snack-threshold"
              v-model.number="lowStockThreshold"
              type="number"
              min="0"
              class="form-input"
              :class="{ 'form-input--error': errors.threshold }"
              required
              :disabled="isSubmitting"
              @input="errors.threshold = ''"
            />
            <span v-if="errors.threshold" class="form-error" role="alert">{{ errors.threshold }}</span>
            <span class="form-help-text">
              Card will show amber ribbon when quantity falls below or equal to this number.
            </span>
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
              <span>{{ isSubmitting ? 'Saving...' : 'Save Changes' }}</span>
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
  snack: Snack | null;
}>();

const emit = defineEmits<{
  (e: 'close'): void;
  (e: 'updated', snack: Snack): void;
}>();

const { success: toastSuccess } = useToast();

const modalRef = ref<HTMLElement | null>(null);
const nameInputRef = ref<HTMLInputElement | null>(null);

const name = ref('');
const category = ref<SnackCategoryType>('sweet');
const lowStockThreshold = ref(5);
const isSubmitting = ref(false);
const globalError = ref('');

const errors = reactive({
  name: '',
  threshold: '',
});

useModalAccessibility({
  isOpen: toRef(props, 'isOpen'),
  modalRef,
  onClose: handleClose,
  initialFocusRef: nameInputRef,
});

// Populate form when modal opens or snack changes
watch(
  () => [props.isOpen, props.snack],
  () => {
    if (props.isOpen && props.snack) {
      name.value = props.snack.name;
      category.value = props.snack.category;
      lowStockThreshold.value = props.snack.low_stock_threshold;
      globalError.value = '';
      errors.name = '';
      errors.threshold = '';
    }
  },
  { immediate: true }
);

function handleClose() {
  if (!isSubmitting.value) {
    emit('close');
  }
}

async function handleSubmit() {
  if (!props.snack) return;

  errors.name = '';
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

  if (lowStockThreshold.value === undefined || lowStockThreshold.value === null || isNaN(lowStockThreshold.value) || lowStockThreshold.value < 0) {
    errors.threshold = 'Threshold must be 0 or greater';
    return;
  }

  isSubmitting.value = true;

  try {
    const updated = await snacksApi.update(props.snack.id, {
      name: trimmedName,
      category: category.value,
      low_stock_threshold: Math.floor(lowStockThreshold.value),
    });

    toastSuccess(`Updated "${updated.name}" successfully!`);
    emit('updated', updated);
    emit('close');
  } catch (err: any) {
    if (
      err?.code === 'SNACK_NAME_TAKEN' ||
      err?.code === 'DUPLICATE_NAME' ||
      err?.message?.toLowerCase().includes('already exists')
    ) {
      errors.name = 'A snack with this name already exists in the pantry';
      nameInputRef.value?.focus();
    } else {
      globalError.value = err?.message || 'Failed to update snack. Please try again.';
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
    from { transform: translateY(100%); }
    to { transform: translateY(0); }
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

.modal-form__note {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: var(--space-3);
  background-color: var(--color-cream);
  border-radius: var(--radius-md);
  border: 1px solid rgba(31, 27, 24, 0.08);
  font-size: var(--text-xs);
  color: var(--color-muted);
  line-height: 1.4;
}

.note-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
  color: var(--color-orange);
  margin-top: 1px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
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

.form-help-text {
  font-size: var(--text-xs);
  color: var(--color-muted);
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
