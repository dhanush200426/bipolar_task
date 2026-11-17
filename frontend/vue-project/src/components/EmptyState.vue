<template>
  <div class="empty-state">
    <div class="empty-state__icon" aria-hidden="true">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="10" />
        <line x1="8" y1="12" x2="16" y2="12" />
        <line x1="12" y1="8" x2="12" y2="16" />
      </svg>
    </div>
    <h2 class="empty-state__title">{{ title }}</h2>
    <p class="empty-state__message">{{ message }}</p>
    <slot name="action"></slot>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title: string;
  message: string;
}>();
</script>

<style scoped>
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-12);
  text-align: center;
  min-height: 200px;
}

.empty-state__icon {
  width: 64px;
  height: 64px;
  color: var(--color-muted);
  margin-bottom: var(--space-6);
}

.empty-state__title {
  font-size: var(--text-xl);
  margin-bottom: var(--space-3);
  color: var(--color-charcoal);
}

.empty-state__message {
  font-size: var(--text-base);
  color: var(--color-muted);
  margin-bottom: var(--space-6);
  max-width: 400px;
}
</style>
