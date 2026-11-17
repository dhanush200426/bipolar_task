<template>
  <div class="snack-illustration" :class="`snack-illustration--${category}`" aria-hidden="true">
    <!-- Sweet: Cookie -->
    <svg v-if="category === 'sweet'" viewBox="0 0 64 64" fill="none" class="snack-illustration__svg">
      <circle cx="32" cy="32" r="26" fill="#F7B733" stroke="#C8321A" stroke-width="2.5" />
      <circle cx="23" cy="23" r="3.5" fill="#C8321A" />
      <circle cx="41" cy="27" r="3.5" fill="#C8321A" />
      <circle cx="33" cy="41" r="3.5" fill="#C8321A" />
      <circle cx="21" cy="37" r="3" fill="#C8321A" />
      <circle cx="43" cy="39" r="3" fill="#C8321A" />
      <circle cx="32" cy="26" r="2.5" fill="#E4472B" />
    </svg>

    <!-- Savoury: Snack Packet -->
    <svg v-else-if="category === 'savoury'" viewBox="0 0 64 64" fill="none" class="snack-illustration__svg">
      <rect x="13" y="7" width="38" height="50" rx="6" fill="#F58A1F" stroke="#C8321A" stroke-width="2.5" />
      <path d="M13 14H51" stroke="#C8321A" stroke-width="2" stroke-dasharray="2 2" />
      <path d="M13 50H51" stroke="#C8321A" stroke-width="2" stroke-dasharray="2 2" />
      <circle cx="32" cy="32" r="12" fill="#FFF8EE" stroke="#E4472B" stroke-width="2" />
      <path d="M28 28L36 36M36 28L28 36" stroke="#C8321A" stroke-width="2.5" stroke-linecap="round" />
    </svg>

    <!-- Drink: Hot Mug / Cup -->
    <svg v-else-if="category === 'drink'" viewBox="0 0 64 64" fill="none" class="snack-illustration__svg">
      <path d="M15 18H43C43 18 45 18 45 22V40C45 49 37 55 29 55C21 55 13 49 13 40V22C13 18 15 18 15 18Z" fill="#E4472B" stroke="#1F1B18" stroke-width="2.5" />
      <path d="M45 25H52C56 25 57 32 57 33C57 34 56 41 52 41H45" fill="none" stroke="#1F1B18" stroke-width="2.5" stroke-linecap="round" />
      <path d="M22 13C22 13 24 9 24 7" stroke="#F7B733" stroke-width="2" stroke-linecap="round" opacity="0.9" />
      <path d="M29 13C29 13 31 8 31 6" stroke="#F7B733" stroke-width="2" stroke-linecap="round" opacity="0.9" />
      <path d="M36 13C36 13 38 9 38 7" stroke="#F7B733" stroke-width="2" stroke-linecap="round" opacity="0.9" />
      <ellipse cx="29" cy="22" rx="12" ry="3" fill="#FFF8EE" opacity="0.7" />
    </svg>

    <!-- Healthy-ish: Fresh Apple / Fruit -->
    <svg v-else viewBox="0 0 64 64" fill="none" class="snack-illustration__svg">
      <!-- Leaf & Stem -->
      <path d="M32 18V8" stroke="#6B625B" stroke-width="2.5" stroke-linecap="round" />
      <path d="M32 12C37 9 44 11 44 11C44 11 43 17 38 18C33 19 32 12 32 12Z" fill="#2E9E6B" stroke="#1F1B18" stroke-width="1.5" />
      <!-- Apple body -->
      <path d="M32 23C26 17 14 19 14 32C14 45 26 55 32 57C38 55 50 45 50 32C50 19 38 17 32 23Z" fill="#2E9E6B" stroke="#1F1B18" stroke-width="2.5" />
      <!-- Highlight -->
      <path d="M22 26C18 30 18 38 21 42" stroke="#FFF8EE" stroke-width="2" stroke-linecap="round" opacity="0.6" />
    </svg>
  </div>
</template>

<script setup lang="ts">
import type { SnackCategoryType } from '../api/types';

defineProps<{
  category: SnackCategoryType | string;
}>();
</script>

<style scoped>
.snack-illustration {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}

.snack-illustration__svg {
  width: 100%;
  height: 100%;
  max-width: 96px;
  max-height: 96px;
  filter: drop-shadow(0 4px 6px rgba(31, 27, 24, 0.08));
  transition: transform var(--transition-base);
}

.snack-illustration:hover .snack-illustration__svg {
  transform: scale(1.05) rotate(2deg);
}

@media (prefers-reduced-motion: reduce) {
  .snack-illustration:hover .snack-illustration__svg {
    transform: none;
  }
}
</style>
