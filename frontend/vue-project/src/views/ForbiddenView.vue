<template>
  <div class="forbidden-view">
    <div class="forbidden-view__icon" aria-hidden="true">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
        <path d="M7 11V7a5 5 0 0 1 10 0v4" />
      </svg>
    </div>
    <h1>Access Denied</h1>
    <p>You don't have permission to access this page.</p>
    <router-link to="/" class="forbidden-view__back">Go to Dashboard</router-link>
  </div>
</template>

<script setup lang="ts">
// 403 Forbidden page
</script>

<style scoped>
.forbidden-view {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: var(--space-12);
  text-align: center;
}

.forbidden-view__icon {
  width: 80px;
  height: 80px;
  color: var(--color-warning);
  margin-bottom: var(--space-8);
}

.forbidden-view__icon svg {
  width: 100%;
  height: 100%;
}

.forbidden-view h1 {
  font-size: var(--text-3xl);
  margin-bottom: var(--space-4);
  color: var(--color-charcoal);
}

.forbidden-view p {
  font-size: var(--text-lg);
  color: var(--color-muted);
  margin-bottom: var(--space-8);
  max-width: 400px;
}

.forbidden-view__back {
  padding: var(--space-3) var(--space-6);
  background-color: var(--color-tomato);
  color: white;
  font-weight: 600;
  border-radius: var(--radius-md);
  transition: background-color var(--transition-fast);
}

.forbidden-view__back:hover {
  background-color: var(--color-chili);
}

.forbidden-view__back:focus-visible {
  outline: 2px solid var(--color-tomato);
  outline-offset: 2px;
}
</style>
