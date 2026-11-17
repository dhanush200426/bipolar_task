<template>
  <div class="error-state">
    <div class="error-state__icon" aria-hidden="true">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="10" />
        <line x1="12" y1="8" x2="12" y2="12" />
        <line x1="12" y1="16" x2="12.01" y2="16" />
      </svg>
    </div>
    <h2 class="error-state__title">{{ title }}</h2>
    <p class="error-state__message">{{ message }}</p>
    <button
      v-if="showRetry"
      @click="$emit('retry')"
      class="error-state__retry"
      type="button"
    >
      Try Again
    </button>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title: string;
  message: string;
  showRetry?: boolean;
}>();

defineEmits<{
  retry: [];
}>();
</script>

<style scoped>
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-12);
  text-align: center;
  min-height: 200px;
}

.error-state__icon {
  width: 64px;
  height: 64px;
  color: var(--color-danger);
  margin-bottom: var(--space-6);
}

.error-state__title {
  font-size: var(--text-xl);
  margin-bottom: var(--space-3);
  color: var(--color-charcoal);
}

.error-state__message {
  font-size: var(--text-base);
  color: var(--color-muted);
  margin-bottom: var(--space-6);
  max-width: 400px;
}

.error-state__retry {
  padding: var(--space-3) var(--space-6);
  background-color: var(--color-tomato);
  color: white;
  font-weight: 600;
  border-radius: var(--radius-md);
  transition: background-color var(--transition-fast);
}

.error-state__retry:hover {
  background-color: var(--color-chili);
}

.error-state__retry:focus-visible {
  outline: 2px solid var(--color-tomato);
  outline-offset: 2px;
}
</style>
