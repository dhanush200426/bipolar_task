<template>
  <Teleport to="body">
    <div
      v-if="isOpen"
      class="modal-backdrop"
      role="presentation"
      @click.self="handleClose"
    >
      <div
        ref="dialogRef"
        class="modal-dialog modal-dialog--sheet modal-dialog--delete"
        role="dialog"
        aria-modal="true"
        aria-labelledby="delete-snack-title"
        aria-describedby="delete-snack-desc"
        tabindex="-1"
      >
        <!-- Mobile Bottom Sheet Handle -->
        <div class="modal-handle-bar" aria-hidden="true"></div>

        <div class="delete-dialog__body">
          <!-- Destructive Icon -->
          <div class="delete-dialog__icon-wrap" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="delete-icon">
              <path d="M3 6h18" />
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6" />
              <path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
              <line x1="10" y1="11" x2="10" y2="17" />
              <line x1="14" y1="11" x2="14" y2="17" />
            </svg>
          </div>

          <h2 id="delete-snack-title" class="delete-dialog__title">Delete Snack</h2>
          <p id="delete-snack-desc" class="delete-dialog__desc">
            Are you sure you want to remove <strong>"{{ snack?.name }}"</strong> from the office pantry?
            This will delete all its voting and activity records permanently.
          </p>

          <div v-if="error" class="modal-form__error-banner" role="alert">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="error-banner__icon">
              <circle cx="12" cy="12" r="10" />
              <line x1="12" y1="8" x2="12" y2="12" />
              <line x1="12" y1="16" x2="12.01" y2="16" />
            </svg>
            <span>{{ error }}</span>
          </div>

          <!-- Actions -->
          <div class="delete-dialog__actions">
            <button
              ref="cancelBtnRef"
              type="button"
              class="btn-secondary"
              :disabled="isDeleting"
              @click="handleClose"
            >
              Cancel
            </button>
            <button
              type="button"
              class="btn-destructive"
              :disabled="isDeleting"
              @click="handleConfirmDelete"
            >
              <svg v-if="isDeleting" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="btn-spinner">
                <circle cx="12" cy="12" r="10" stroke-opacity="0.25" />
                <path d="M12 2a10 10 0 0 1 10 10" />
              </svg>
              <span>{{ isDeleting ? 'Deleting...' : 'Yes, Delete Snack' }}</span>
            </button>
          </div>
        </div>
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
  (e: 'deleted', snackId: string): void;
}>();

const { success: toastSuccess, warning: toastWarning, error: toastError } = useToast();

const dialogRef = ref<HTMLElement | null>(null);
const cancelBtnRef = ref<HTMLButtonElement | null>(null);

const isDeleting = ref(false);
const error = ref('');

useModalAccessibility({
  isOpen: toRef(props, 'isOpen'),
  modalRef: dialogRef,
  onClose: handleClose,
  initialFocusRef: cancelBtnRef,
});

watch(
  () => props.isOpen,
  (val) => {
    if (val) {
      error.value = '';
    }
  }
);

function handleClose() {
  if (!isDeleting.value) {
    emit('close');
  }
}

async function handleConfirmDelete() {
  if (!props.snack) return;

  isDeleting.value = true;
  error.value = '';
  const snackId = props.snack.id;
  const snackName = props.snack.name;

  try {
    await snacksApi.delete(snackId);
    toastSuccess(`Deleted "${snackName}" from pantry.`);
    emit('deleted', snackId);
    emit('close');
  } catch (err: any) {
    // Graceful 404 handling (e.g. if another admin deleted it)
    if (err?.code === 'SNACK_NOT_FOUND' || err?.code === 'NOT_FOUND' || err?.status === 404) {
      toastWarning(`"${snackName}" was already deleted from the pantry.`);
      emit('deleted', snackId);
      emit('close');
    } else {
      error.value = err?.message || 'Failed to delete snack. Please try again.';
      toastError(error.value);
    }
  } finally {
    isDeleting.value = false;
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

.delete-dialog__body {
  padding: var(--space-6);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.delete-dialog__icon-wrap {
  width: 56px;
  height: 56px;
  border-radius: var(--radius-full);
  background-color: #FDF2F2;
  color: var(--color-danger);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: var(--space-4);
  box-shadow: 0 0 0 8px rgba(211, 47, 47, 0.08);
}

.delete-icon {
  width: 28px;
  height: 28px;
}

.delete-dialog__title {
  font-family: var(--font-display);
  font-size: var(--text-2xl);
  font-weight: 800;
  color: var(--color-charcoal);
  margin: 0 0 var(--space-2);
}

.delete-dialog__desc {
  font-size: var(--text-sm);
  color: var(--color-muted);
  line-height: 1.5;
  margin: 0 0 var(--space-6);
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
  margin-bottom: var(--space-4);
  width: 100%;
  text-align: left;
}

.error-banner__icon {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.delete-dialog__actions {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-3);
  width: 100%;
}

@media (max-width: 480px) {
  .delete-dialog__actions {
    flex-direction: column-reverse;
  }
  .btn-secondary,
  .btn-destructive {
    width: 100%;
  }
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

.btn-destructive {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  height: 44px;
  padding: 0 var(--space-6);
  background-color: var(--color-danger);
  border: none;
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
  font-weight: 700;
  color: #ffffff;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(211, 47, 47, 0.35);
  transition: all var(--transition-fast);
}

.btn-destructive:hover:not(:disabled) {
  background-color: #B71C1C;
  transform: translateY(-1px);
  box-shadow: 0 4px 10px rgba(211, 47, 47, 0.45);
}

.btn-destructive:disabled,
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
