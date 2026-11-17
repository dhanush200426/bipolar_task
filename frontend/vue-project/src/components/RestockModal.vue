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
        aria-labelledby="restock-snack-title"
        tabindex="-1"
      >
        <!-- Mobile Bottom Sheet Handle -->
        <div class="modal-handle-bar" aria-hidden="true"></div>

        <!-- Modal Header -->
        <div class="modal-header">
          <div class="modal-header__title-group">
            <div class="modal-header__icon" aria-hidden="true">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" />
                <polyline points="3.27 6.96 12 12.01 20.73 6.96" />
                <line x1="12" y1="22.08" x2="12" y2="12" />
              </svg>
            </div>
            <div>
              <h2 id="restock-snack-title" class="modal-title">Restock Pantry</h2>
              <p class="modal-subtitle">{{ snack?.name }}</p>
            </div>
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

        <!-- Restock Form -->
        <form @submit.prevent="handleSubmit" class="modal-form" novalidate>
          <!-- Current Stock Info -->
          <div class="restock-current-badge">
            <span class="current-label">Current Stock:</span>
            <span class="current-value">{{ snack?.quantity ?? 0 }} packets</span>
          </div>

          <!-- Quick Chips (+5, +10, +20) -->
          <div class="form-group">
            <label class="form-label">Quick Add Chips</label>
            <div class="quick-chips">
              <button
                v-for="chip in [5, 10, 20]"
                :key="chip"
                type="button"
                class="chip-btn"
                :disabled="isSubmitting"
                @click="addAmount(chip)"
              >
                +{{ chip }}
              </button>
              <button
                type="button"
                class="chip-btn chip-btn--reset"
                :disabled="isSubmitting"
                title="Reset amount to 10"
                @click="amount = 10"
              >
                Reset
              </button>
            </div>
          </div>

          <!-- Amount Input Field -->
          <div class="form-group">
            <label for="restock-amount" class="form-label">
              Restock Quantity (1 – 10,000) <span class="required-star">*</span>
            </label>
            <div class="amount-stepper-wrap">
              <button
                type="button"
                class="stepper-btn"
                :disabled="isSubmitting || amount <= 1"
                aria-label="Decrease amount by 1"
                @click="amount > 1 && amount--"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                  <line x1="5" y1="12" x2="19" y2="12" />
                </svg>
              </button>
              <input
                id="restock-amount"
                ref="amountInputRef"
                v-model.number="amount"
                type="number"
                min="1"
                max="10000"
                class="form-input amount-input"
                :class="{ 'form-input--error': error }"
                required
                :disabled="isSubmitting"
                @input="error = ''"
              />
              <button
                type="button"
                class="stepper-btn"
                :disabled="isSubmitting || amount >= 10000"
                aria-label="Increase amount by 1"
                @click="amount < 10000 && amount++"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                  <line x1="12" y1="5" x2="12" y2="19" />
                  <line x1="5" y1="12" x2="19" y2="12" />
                </svg>
              </button>
            </div>
            <span v-if="error" class="form-error" role="alert">{{ error }}</span>
            <span class="form-help-text">
              New total will be: <strong>{{ (snack?.quantity ?? 0) + (amount > 0 ? amount : 0) }}</strong> packets.
            </span>
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
              class="btn-primary btn-primary--restock"
              :disabled="isSubmitting"
            >
              <svg v-if="isSubmitting" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="btn-spinner">
                <circle cx="12" cy="12" r="10" stroke-opacity="0.25" />
                <path d="M12 2a10 10 0 0 1 10 10" />
              </svg>
              <span>{{ isSubmitting ? 'Restocking...' : `Restock (+${amount || 0})` }}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, watch, toRef } from 'vue';
import type { Snack } from '../api/types';
import { snacksApi } from '../api/snacks';
import { useToast } from '../composables/useToast';
import { useModalAccessibility } from '../composables/useModalAccessibility';

const props = defineProps<{
  isOpen: boolean;
  snack: Snack | null;
}>();

const emit = defineEmits<{
  (e: 'close'): void;
  (e: 'restocked', snack: Snack): void;
}>();

const { success: toastSuccess, error: toastError } = useToast();

const modalRef = ref<HTMLElement | null>(null);
const amountInputRef = ref<HTMLInputElement | null>(null);

const amount = ref<number>(10);
const isSubmitting = ref(false);
const error = ref('');

useModalAccessibility({
  isOpen: toRef(props, 'isOpen'),
  modalRef,
  onClose: handleClose,
  initialFocusRef: amountInputRef,
});

watch(
  () => props.isOpen,
  (val) => {
    if (val) {
      amount.value = 10;
      error.value = '';
    }
  }
);

function addAmount(chip: number) {
  const current = amount.value || 0;
  amount.value = Math.min(10000, current + chip);
  error.value = '';
}

function handleClose() {
  if (!isSubmitting.value) {
    emit('close');
  }
}

async function handleSubmit() {
  if (!props.snack) return;

  error.value = '';

  if (amount.value === undefined || amount.value === null || isNaN(amount.value) || amount.value < 1) {
    error.value = 'Amount must be at least 1 packet';
    amountInputRef.value?.focus();
    return;
  }

  if (amount.value > 10000) {
    error.value = 'Amount cannot exceed 10,000 packets';
    amountInputRef.value?.focus();
    return;
  }

  isSubmitting.value = true;

  try {
    const updated = await snacksApi.restock(props.snack.id, {
      amount: Math.floor(amount.value),
    });

    toastSuccess(`Restocked ${amount.value} packets of "${updated.name}"!`);
    emit('restocked', updated);
    emit('close');
  } catch (err: any) {
    error.value = err?.message || 'Failed to restock snack. Please check connection.';
    toastError(error.value);
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
  max-width: 440px;
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
  width: 34px;
  height: 34px;
  border-radius: var(--radius-md);
  background: #E8F5E9;
  color: var(--color-success);
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
  line-height: 1.15;
}

.modal-subtitle {
  font-size: var(--text-xs);
  color: var(--color-muted);
  margin: 0;
  max-width: 260px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
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

.restock-current-badge {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-3) var(--space-4);
  background-color: var(--color-cream);
  border-radius: var(--radius-md);
  border: 1px solid rgba(31, 27, 24, 0.08);
}

.current-label {
  font-size: var(--text-xs);
  font-weight: 600;
  color: var(--color-muted);
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.current-value {
  font-size: var(--text-sm);
  font-weight: 800;
  color: var(--color-charcoal);
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

.quick-chips {
  display: flex;
  gap: var(--space-2);
}

.chip-btn {
  flex: 1;
  height: 36px;
  background-color: var(--color-cream);
  border: 1.5px solid rgba(31, 27, 24, 0.12);
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
  font-weight: 700;
  color: var(--color-charcoal);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.chip-btn:hover:not(:disabled) {
  background-color: var(--color-peach);
  border-color: var(--color-tomato);
  color: var(--color-tomato);
  transform: translateY(-1px);
}

.chip-btn--reset {
  color: var(--color-muted);
  font-size: var(--text-xs);
  flex: 0 0 60px;
}

.amount-stepper-wrap {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.stepper-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  border-radius: var(--radius-md);
  border: 1.5px solid rgba(31, 27, 24, 0.16);
  background-color: var(--color-cream);
  color: var(--color-charcoal);
  cursor: pointer;
  transition: all var(--transition-fast);
  flex-shrink: 0;
}

.stepper-btn:hover:not(:disabled) {
  background-color: rgba(31, 27, 24, 0.08);
}

.stepper-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.stepper-btn svg {
  width: 16px;
  height: 16px;
}

.amount-input {
  flex: 1;
  height: 44px;
  text-align: center;
  font-size: var(--text-lg);
  font-weight: 800;
  font-feature-settings: 'tnum';
  border: 1.5px solid rgba(31, 27, 24, 0.16);
  border-radius: var(--radius-md);
  padding: 0 var(--space-3);
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
}

.amount-input:focus {
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
}

.btn-primary--restock {
  background-color: var(--color-success);
  box-shadow: 0 2px 4px rgba(46, 158, 107, 0.3);
}

.btn-primary--restock:hover:not(:disabled) {
  background-color: #248157;
  box-shadow: 0 4px 8px rgba(46, 158, 107, 0.4);
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  height: 44px;
  padding: 0 var(--space-6);
  border: none;
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
  font-weight: 700;
  color: #ffffff;
  cursor: pointer;
  transition: all var(--transition-fast);
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
