<template>
  <Teleport to="body">
    <div class="toast-container" role="alert" aria-live="polite">
      <TransitionGroup name="toast">
        <div
          v-for="toast in toasts"
          :key="toast.id"
          :class="['toast', `toast--${toast.type}`]"
        >
          <span class="toast__message">{{ toast.message }}</span>
          <button
            @click="removeToast(toast.id)"
            class="toast__close"
            aria-label="Close"
            type="button"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
          </button>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { useToast } from '../composables/useToast';

const { toasts, removeToast } = useToast();
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: var(--space-6);
  right: var(--space-6);
  z-index: 1000;
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  max-width: 400px;
}

.toast {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-3);
  padding: var(--space-4);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  background-color: var(--color-charcoal);
  color: white;
  min-width: 280px;
}

.toast--success {
  background-color: var(--color-success);
}

.toast--error {
  background-color: var(--color-danger);
}

.toast--warning {
  background-color: var(--color-warning);
}

.toast--info {
  background-color: var(--color-charcoal);
}

.toast__message {
  flex: 1;
  font-size: var(--text-sm);
}

.toast__close {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  color: inherit;
  opacity: 0.7;
  transition: opacity var(--transition-fast);
  border-radius: var(--radius-sm);
}

.toast__close:hover {
  opacity: 1;
}

.toast__close:focus-visible {
  outline: 2px solid white;
  outline-offset: 2px;
}

.toast-enter-active,
.toast-leave-active {
  transition: all var(--transition-base);
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

@media (prefers-reduced-motion: reduce) {
  .toast-enter-active,
  .toast-leave-active {
    transition: none;
  }
}
</style>
