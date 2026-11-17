<template>
  <div class="not-found-view">
    <div class="not-found-view__illustration" aria-hidden="true">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="10" />
        <path d="M8 14s1.5 2 4 2 4-2 4-2" />
        <line x1="9" y1="9" x2="9.01" y2="9" />
        <line x1="15" y1="9" x2="15.01" y2="9" />
      </svg>
    </div>
    <h1>This snack isn't on the menu</h1>
    <p>We couldn't find the page you're looking for.</p>
    <div class="not-found-view__actions">
      <router-link to="/" class="not-found-view__primary">Go Home</router-link>
      <router-link to="/snacks" class="not-found-view__secondary">View Snacks</router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
// 404 Not Found page with playful food theme
</script>

<style scoped>
.not-found-view {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: var(--space-12);
  text-align: center;
}

.not-found-view__illustration {
  width: 120px;
  height: 120px;
  color: var(--color-tomato);
  margin-bottom: var(--space-8);
}

.not-found-view__illustration svg {
  width: 100%;
  height: 100%;
}

.not-found-view h1 {
  font-size: var(--text-4xl);
  margin-bottom: var(--space-4);
  color: var(--color-charcoal);
}

.not-found-view p {
  font-size: var(--text-lg);
  color: var(--color-muted);
  margin-bottom: var(--space-8);
  max-width: 400px;
}

.not-found-view__actions {
  display: flex;
  gap: var(--space-4);
  flex-wrap: wrap;
  justify-content: center;
}

.not-found-view__primary,
.not-found-view__secondary {
  padding: var(--space-3) var(--space-6);
  font-weight: 600;
  border-radius: var(--radius-md);
  transition: background-color var(--transition-fast);
}

.not-found-view__primary {
  background-color: var(--color-tomato);
  color: white;
}

.not-found-view__primary:hover {
  background-color: var(--color-chili);
}

.not-found-view__primary:focus-visible {
  outline: 2px solid var(--color-tomato);
  outline-offset: 2px;
}

.not-found-view__secondary {
  background-color: var(--color-peach);
  color: var(--color-charcoal);
}

.not-found-view__secondary:hover {
  background-color: var(--color-orange);
}

.not-found-view__secondary:focus-visible {
  outline: 2px solid var(--color-tomato);
  outline-offset: 2px;
}
</style>
