<template>
  <div class="app-shell">
    <!-- Top navigation bar -->
    <header class="app-shell__header" :class="{ 'app-shell__header--scrolled': isScrolled }">
      <div class="app-shell__container">
        <!-- Logo -->
        <router-link to="/" class="app-shell__logo">
          <svg viewBox="0 0 64 64" fill="none" class="app-shell__logo-icon" aria-hidden="true">
            <rect x="12" y="8" width="40" height="48" rx="4" fill="#F58A1F" stroke="#C8321A" stroke-width="2"/>
            <rect x="16" y="16" width="32" height="8" rx="2" fill="#FFF8EE"/>
            <rect x="16" y="28" width="32" height="8" rx="2" fill="#FFF8EE"/>
            <rect x="16" y="40" width="32" height="8" rx="2" fill="#FFF8EE"/>
          </svg>
          <span class="app-shell__logo-text">Snack Overflow</span>
        </router-link>

        <!-- Desktop navigation -->
        <nav class="app-shell__nav app-shell__nav--desktop">
          <router-link to="/" class="app-shell__nav-link" active-class="app-shell__nav-link--active">
            Dashboard
          </router-link>
          <router-link to="/snacks" class="app-shell__nav-link" active-class="app-shell__nav-link--active">
            Snacks
          </router-link>
        </nav>

        <!-- User menu -->
        <div class="app-shell__user" ref="userMenuRef">
          <button 
            @click="toggleUserMenu" 
            class="app-shell__user-button"
            :aria-expanded="isUserMenuOpen"
            aria-haspopup="true"
          >
            <span class="app-shell__user-name">{{ user?.name }}</span>
            <span v-if="user" class="app-shell__user-role badge" :class="roleBadgeClass">
              {{ user.role }}
            </span>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="app-shell__user-chevron">
              <polyline points="6 9 12 15 18 9"/>
            </svg>
          </button>

          <!-- User dropdown -->
          <Transition name="dropdown">
            <div v-if="isUserMenuOpen" class="app-shell__user-dropdown">
              <div class="app-shell__user-info">
                <span class="app-shell__user-info-name">{{ user?.name }}</span>
                <span class="app-shell__user-info-email">{{ user?.email }}</span>
              </div>
              <div class="app-shell__user-divider"></div>
              <button @click="handleLogout" class="app-shell__user-item">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
                  <polyline points="16 17 21 12 16 7"/>
                  <line x1="21" y1="12" x2="9" y2="12"/>
                </svg>
                Logout
              </button>
            </div>
          </Transition>
        </div>

        <!-- Mobile menu button -->
        <button 
          @click="toggleMobileMenu" 
          class="app-shell__mobile-toggle"
          :aria-expanded="isMobileMenuOpen"
          aria-label="Toggle menu"
        >
          <svg v-if="!isMobileMenuOpen" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="3" y1="12" x2="21" y2="12"/>
            <line x1="3" y1="6" x2="21" y2="6"/>
            <line x1="3" y1="18" x2="21" y2="18"/>
          </svg>
          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"/>
            <line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
        </button>
      </div>
    </header>

    <!-- Mobile navigation -->
    <Transition name="mobile-nav">
      <nav v-if="isMobileMenuOpen" class="app-shell__nav app-shell__nav--mobile">
        <router-link 
          to="/" 
          class="app-shell__mobile-link" 
          active-class="app-shell__mobile-link--active"
          @click="isMobileMenuOpen = false"
        >
          Dashboard
        </router-link>
        <router-link 
          to="/snacks" 
          class="app-shell__mobile-link" 
          active-class="app-shell__mobile-link--active"
          @click="isMobileMenuOpen = false"
        >
          Snacks
        </router-link>
        <div class="app-shell__mobile-divider"></div>
        <button @click="handleLogout" class="app-shell__mobile-link app-shell__mobile-link--logout">
          Logout
        </button>
      </nav>
    </Transition>

    <!-- Main content -->
    <main class="app-shell__main">
      <router-view v-slot="{ Component, route }">
        <Transition :name="transitionName" mode="out-in">
          <component :is="Component" :key="route.path" />
        </Transition>
      </router-view>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { onClickOutside } from '../utils/clickOutside'

const router = useRouter()
const authStore = useAuthStore()

const user = computed(() => authStore.user)
const isAdmin = computed(() => authStore.isAdmin)

const isScrolled = ref(false)
const isUserMenuOpen = ref(false)
const isMobileMenuOpen = ref(false)
const userMenuRef = ref<HTMLElement>()

const roleBadgeClass = computed(() => {
  if (!user.value) return ''
  return user.value.role === 'ADMIN' ? 'badge-stocked' : 'badge-running-low'
})

const transitionName = computed(() => {
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  return prefersReducedMotion ? 'none' : 'fade-slide'
})

function handleScroll() {
  isScrolled.value = window.scrollY > 10
}

function toggleUserMenu() {
  isUserMenuOpen.value = !isUserMenuOpen.value
}

function toggleMobileMenu() {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

function handleLogout() {
  authStore.logout()
  isUserMenuOpen.value = false
  isMobileMenuOpen.value = false
  router.push('/login')
}

// Close user menu when clicking outside
onClickOutside(userMenuRef, () => {
  isUserMenuOpen.value = false
})

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
.app-shell {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Header */
.app-shell__header {
  position: sticky;
  top: 0;
  z-index: 100;
  background-color: var(--color-cream);
  border-bottom: 1px solid var(--color-peach);
  transition: box-shadow var(--transition-base);
}

.app-shell__header--scrolled {
  box-shadow: var(--shadow-md);
}

.app-shell__container {
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--space-4) var(--space-6);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-6);
}

/* Logo */
.app-shell__logo {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  text-decoration: none;
  color: var(--color-charcoal);
  transition: opacity var(--transition-fast);
}

.app-shell__logo:hover {
  opacity: 0.8;
}

.app-shell__logo-icon {
  width: 32px;
  height: 32px;
}

.app-shell__logo-text {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: 600;
  color: var(--color-tomato);
}

/* Desktop navigation */
.app-shell__nav--desktop {
  display: none;
  gap: var(--space-6);
}

.app-shell__nav-link {
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--color-muted);
  text-decoration: none;
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-md);
  transition: color var(--transition-fast), background-color var(--transition-fast);
}

.app-shell__nav-link:hover {
  color: var(--color-charcoal);
  background-color: var(--color-peach);
}

.app-shell__nav-link--active {
  color: var(--color-tomato);
  background-color: rgba(228, 71, 43, 0.1);
}

/* User menu */
.app-shell__user {
  position: relative;
}

.app-shell__user-button {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-3);
  background-color: var(--color-peach);
  border-radius: var(--radius-full);
  border: none;
  cursor: pointer;
  font-family: inherit;
  transition: background-color var(--transition-fast);
}

.app-shell__user-button:hover {
  background-color: var(--color-orange);
}

.app-shell__user-name {
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--color-charcoal);
}

.app-shell__user-role {
  font-size: var(--text-xs);
}

.app-shell__user-chevron {
  width: 16px;
  height: 16px;
  color: var(--color-muted);
  transition: transform var(--transition-fast);
}

.app-shell__user-button[aria-expanded="true"] .app-shell__user-chevron {
  transform: rotate(180deg);
}

.app-shell__user-dropdown {
  position: absolute;
  top: calc(100% + var(--space-2));
  right: 0;
  min-width: 240px;
  background-color: white;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xl);
  padding: var(--space-4);
  z-index: 101;
}

.app-shell__user-info {
  padding-bottom: var(--space-3);
}

.app-shell__user-info-name {
  display: block;
  font-size: var(--text-sm);
  font-weight: 600;
  color: var(--color-charcoal);
}

.app-shell__user-info-email {
  display: block;
  font-size: var(--text-xs);
  color: var(--color-muted);
  margin-top: var(--space-1);
}

.app-shell__user-divider {
  height: 1px;
  background-color: var(--color-peach);
  margin: var(--space-3) 0;
}

.app-shell__user-item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  width: 100%;
  padding: var(--space-2) var(--space-3);
  background: none;
  border: none;
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
  color: var(--color-charcoal);
  cursor: pointer;
  text-align: left;
  font-family: inherit;
  transition: background-color var(--transition-fast);
}

.app-shell__user-item:hover {
  background-color: var(--color-cream);
}

.app-shell__user-item svg {
  width: 16px;
  height: 16px;
  color: var(--color-muted);
}

/* Mobile toggle */
.app-shell__mobile-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: none;
  border: none;
  border-radius: var(--radius-md);
  color: var(--color-charcoal);
  cursor: pointer;
  transition: background-color var(--transition-fast);
}

.app-shell__mobile-toggle:hover {
  background-color: var(--color-peach);
}

.app-shell__mobile-toggle svg {
  width: 24px;
  height: 24px;
}

/* Mobile navigation */
.app-shell__nav--mobile {
  display: flex;
  flex-direction: column;
  padding: var(--space-4);
  background-color: var(--color-cream);
  border-bottom: 1px solid var(--color-peach);
}

.app-shell__mobile-link {
  padding: var(--space-4);
  font-size: var(--text-base);
  font-weight: 500;
  color: var(--color-charcoal);
  text-decoration: none;
  border-radius: var(--radius-md);
  transition: background-color var(--transition-fast);
  text-align: left;
  background: none;
  border: none;
  cursor: pointer;
  font-family: inherit;
  width: 100%;
}

.app-shell__mobile-link:hover {
  background-color: var(--color-peach);
}

.app-shell__mobile-link--active {
  color: var(--color-tomato);
  background-color: rgba(228, 71, 43, 0.1);
}

.app-shell__mobile-link--logout {
  color: var(--color-danger);
}

.app-shell__mobile-divider {
  height: 1px;
  background-color: var(--color-peach);
  margin: var(--space-2) 0;
}

/* Main content */
.app-shell__main {
  flex: 1;
}

/* Transitions */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all var(--transition-fast);
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

.mobile-nav-enter-active,
.mobile-nav-leave-active {
  transition: all var(--transition-base);
}

.mobile-nav-enter-from,
.mobile-nav-leave-to {
  opacity: 0;
  transform: translateY(-100%);
}

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.2s ease-out;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

@media (prefers-reduced-motion: reduce) {
  .fade-slide-enter-active,
  .fade-slide-leave-active {
    transition: none;
  }
}

/* Desktop layout */
@media (min-width: 768px) {
  .app-shell__nav--desktop {
    display: flex;
  }
  
  .app-shell__mobile-toggle {
    display: none;
  }
  
  .app-shell__nav--mobile {
    display: none;
  }
}
</style>
