<template>
  <div class="loading-state" aria-busy="true" aria-live="polite">
    <div class="loading-state__shimmer">
      <div class="loading-state__shimmer-item"></div>
      <div class="loading-state__shimmer-item"></div>
      <div class="loading-state__shimmer-item"></div>
    </div>
    <p class="loading-state__text">{{ message }}</p>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  message?: string;
}>();
</script>

<style scoped>
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-12);
}

.loading-state__shimmer {
  display: flex;
  gap: var(--space-4);
  margin-bottom: var(--space-6);
}

.loading-state__shimmer-item {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  background: linear-gradient(
    90deg,
    var(--color-peach) 25%,
    var(--color-cream) 50%,
    var(--color-peach) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

.loading-state__text {
  font-size: var(--text-sm);
  color: var(--color-muted);
}

@media (prefers-reduced-motion: reduce) {
  .loading-state__shimmer-item {
    animation: none;
    background-color: var(--color-peach);
  }
}
</style>
