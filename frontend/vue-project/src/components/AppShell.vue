<template>
  <div class="app-shell">
    <!-- Top navigation bar (Full-scale edge-to-edge on laptop) -->
    <header class="app-shell__header" :class="{ 'app-shell__header--scrolled': isScrolled }">
      <div class="app-shell__container">
        <!-- Logo -->
        <router-link to="/" class="app-shell__logo">
          <div class="app-shell__logo-icon-wrap" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" class="app-shell__logo-icon">
              <rect x="2" y="3" width="20" height="18" rx="4" fill="#FFFFFF" />
              <path d="M7 8h10M7 12h10M7 16h6" stroke="#490982" stroke-width="2.5" stroke-linecap="round" />
            </svg>
          </div>
          <div class="app-shell__logo-text-group">
            <span class="app-shell__logo-text">Snack Overflow</span>
            <span class="app-shell__logo-subtext">Pantry OS</span>
          </div>
        </router-link>

        <!-- Desktop navigation -->
        <nav class="app-shell__nav app-shell__nav--desktop" aria-label="Main navigation">
          <router-link to="/" class="app-shell__nav-link" active-class="app-shell__nav-link--active">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="nav-icon">
              <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
              <polyline points="9 22 9 12 15 12 15 22"/>
            </svg>
            Dashboard
          </router-link>
          <router-link to="/snacks" class="app-shell__nav-link" active-class="app-shell__nav-link--active">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="nav-icon">
              <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/>
              <line x1="3" y1="6" x2="21" y2="6"/>
              <path d="M16 10a4 4 0 0 1-8 0"/>
            </svg>
            Snack Vault
          </router-link>
        </nav>

        <!-- User menu / Sign in -->
        <div v-if="user" class="app-shell__user" ref="userMenuRef">
          <button 
            @click="toggleUserMenu" 
            class="app-shell__user-button"
            :aria-expanded="isUserMenuOpen"
            aria-haspopup="true"
          >
            <div class="app-shell__user-avatar">
              {{ user?.name ? user.name.charAt(0).toUpperCase() : 'U' }}
            </div>
            <div class="app-shell__user-meta">
              <span class="app-shell__user-name">{{ user?.name || 'User' }}</span>
              <span v-if="user" class="app-shell__user-role badge" :class="roleBadgeClass">
                {{ user.role }}
              </span>
            </div>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="app-shell__user-chevron">
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

        <!-- Sign In Button for unauthenticated state -->
        <div v-else class="app-shell__auth-actions">
          <router-link to="/login" class="app-shell__signin-btn" active-class="app-shell__signin-btn--active">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="nav-icon">
              <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4M10 17l5-5-5-5M15 12H3"/>
            </svg>
            Sign In
          </router-link>
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
        <!-- User info banner on mobile drawer -->
        <div v-if="user" class="app-shell__mobile-user-card">
          <div class="app-shell__mobile-avatar">
            {{ user?.name ? user.name.charAt(0).toUpperCase() : 'U' }}
          </div>
          <div class="app-shell__mobile-user-meta">
            <span class="app-shell__mobile-user-name">{{ user?.name }}</span>
            <span class="app-shell__mobile-user-email">{{ user?.email }}</span>
          </div>
          <span class="badge" :class="roleBadgeClass">
            {{ user.role }}
          </span>
        </div>

        <router-link 
          to="/" 
          class="app-shell__mobile-link" 
          active-class="app-shell__mobile-link--active"
          @click="isMobileMenuOpen = false"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="mobile-nav-icon">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
            <polyline points="9 22 9 12 15 12 15 22"/>
          </svg>
          <span>Dashboard</span>
        </router-link>
        <router-link 
          to="/snacks" 
          class="app-shell__mobile-link" 
          active-class="app-shell__mobile-link--active"
          @click="isMobileMenuOpen = false"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="mobile-nav-icon">
            <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/>
            <line x1="3" y1="6" x2="21" y2="6"/>
            <path d="M16 10a4 4 0 0 1-8 0"/>
          </svg>
          <span>Snack Vault</span>
        </router-link>
        <template v-if="user">
          <div class="app-shell__mobile-divider"></div>
          <button @click="handleLogout" class="app-shell__mobile-link app-shell__mobile-link--logout">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="mobile-nav-icon">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
              <polyline points="16 17 21 12 16 7"/>
              <line x1="21" y1="12" x2="9" y2="12"/>
            </svg>
            <span>Logout</span>
          </button>
        </template>
        <template v-else>
          <div class="app-shell__mobile-divider"></div>
          <router-link to="/login" class="app-shell__mobile-link" @click="isMobileMenuOpen = false">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="mobile-nav-icon">
              <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4M10 17l5-5-5-5M15 12H3"/>
            </svg>
            <span>Sign In</span>
          </router-link>
        </template>
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

    <!-- Full-Scale Modern Footer (Purple & White Theme) -->
    <footer class="app-shell__footer">
      <div class="app-shell__footer-container">
        <!-- Grid layout: 4 columns across laptop -->
        <div class="app-shell__footer-grid">
          <!-- Column 1: Brand & Identity -->
          <div class="app-shell__footer-col app-shell__footer-brand">
            <div class="app-shell__footer-logo">
              <div class="app-shell__footer-icon">
                <svg viewBox="0 0 24 24" fill="none">
                  <rect x="2" y="3" width="20" height="18" rx="4" fill="#FFFFFF" />
                  <path d="M7 8h10M7 12h10M7 16h6" stroke="#490982" stroke-width="2.5" stroke-linecap="round" />
                </svg>
              </div>
              <span class="app-shell__footer-title">Snack Overflow</span>
            </div>
            <p class="app-shell__footer-tagline">
              The modern office pantry tracker built for high-performance workplaces. Real-time inventory tracking, zero hunger.
            </p>
            <div class="app-shell__footer-status">
              <span class="status-pulse"></span>
              <span class="status-text">Pantry Inventory Sync: Live</span>
            </div>
          </div>

          <!-- Column 2: Explore Pages -->
          <div class="app-shell__footer-col">
            <h4 class="app-shell__footer-heading">Explore Pages</h4>
            <ul class="app-shell__footer-links">
              <li>
                <router-link to="/">Dashboard Overview</router-link>
              </li>
              <li>
                <router-link to="/snacks">Complete Snack Vault</router-link>
              </li>
              <li>
                <router-link to="/snacks?category=sweet">Sweet Treats</router-link>
              </li>
              <li>
                <router-link to="/snacks?category=healthy-ish">Healthy-ish Picks</router-link>
              </li>
              <li>
                <router-link to="/snacks?status=running_low">Running Low Alerts</router-link>
              </li>
              <li>
                <a href="http://localhost:8000/docs" target="_blank" rel="noopener">Interactive API Docs</a>
              </li>
            </ul>
          </div>

          <!-- Column 3: Our Address & Pantry Location -->
          <div class="app-shell__footer-col">
            <h4 class="app-shell__footer-heading">Our Address</h4>
            <div class="app-shell__footer-contact-item">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="contact-icon">
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                <circle cx="12" cy="10" r="3"/>
              </svg>
              <address class="contact-text">
                Vertex Tech Park, Tower B, Level 6<br>
                742 Cyber City Boulevard, Suite 610<br>
                Whitefield, Bengaluru, KA 560066
              </address>
            </div>
            <div class="app-shell__footer-contact-item">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="contact-icon">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                <polyline points="22,6 12,13 2,6"/>
              </svg>
              <a href="mailto:pantry@snackoverflow.com" class="contact-text">pantry@snackoverflow.com</a>
            </div>
            <div class="app-shell__footer-contact-item">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="contact-icon">
                <circle cx="12" cy="12" r="10"/>
                <polyline points="12 6 12 12 16 14"/>
              </svg>
              <span class="contact-text">Pantry Open: 24/7 for Employees</span>
            </div>
          </div>

          <!-- Column 4: Social Media & Connect -->
          <div class="app-shell__footer-col">
            <h4 class="app-shell__footer-heading">Connect With Us</h4>
            <p class="app-shell__footer-social-intro">
              Follow our pantry updates, restock events, and tech news across our social channels:
            </p>
            <div class="app-shell__footer-socials">
              <!-- LinkedIn -->
              <a href="https://linkedin.com" target="_blank" rel="noopener noreferrer" class="social-btn" aria-label="LinkedIn">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.46 8.76a1.6 1.6 0 1 0 0-3.2 1.6 1.6 0 0 0 0 3.2m1.4 9.74v-8.37H5.06v8.37h2.8z"/>
                </svg>
              </a>
              <!-- GitHub -->
              <a href="https://github.com" target="_blank" rel="noopener noreferrer" class="social-btn" aria-label="GitHub">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2A10 10 0 0 0 2 12c0 4.42 2.87 8.17 6.84 9.5.5.08.66-.23.66-.5v-1.69c-2.77.6-3.36-1.34-3.36-1.34-.46-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.87 1.52 2.34 1.07 2.91.83.1-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.92 0-1.11.38-2 1.03-2.71-.1-.25-.45-1.29.1-2.64 0 0 .84-.27 2.75 1.02.79-.22 1.65-.33 2.5-.33.85 0 1.71.11 2.5.33 1.91-1.29 2.75-1.02 2.75-1.02.55 1.35.2 2.39.1 2.64.65.71 1.03 1.6 1.03 2.71 0 3.82-2.34 4.66-4.57 4.91.36.31.69.92.69 1.85V21c0 .27.16.59.67.5C19.14 20.16 22 16.42 22 12A10 10 0 0 0 12 2z"/>
                </svg>
              </a>
              <!-- Twitter / X -->
              <a href="https://twitter.com" target="_blank" rel="noopener noreferrer" class="social-btn" aria-label="X (Twitter)">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
                </svg>
              </a>
              <!-- Instagram -->
              <a href="https://instagram.com" target="_blank" rel="noopener noreferrer" class="social-btn" aria-label="Instagram">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838a6.162 6.162 0 1 0 0 12.324 6.162 6.162 0 0 0 0-12.324zm0 10.162a3.999 3.999 0 1 1 0-7.998 3.999 3.999 0 0 1 0 7.998zm6.406-11.845a1.44 1.44 0 1 0 0 2.881 1.44 1.44 0 0 0 0-2.881z"/>
                </svg>
              </a>
            </div>
            <div class="app-shell__footer-badge-box">
              <span class="palette-tag">#490982 Purple Edition</span>
            </div>
          </div>
        </div>

        <!-- Footer Bottom Bar -->
        <div class="app-shell__footer-bottom">
          <p class="copyright-text">
            &copy; 2026 <strong>Snack Overflow</strong> &bull; Crafted with precision for high-velocity teams.
          </p>
          <div class="bottom-links">
            <span class="bottom-link">Privacy Policy</span>
            <span class="bottom-sep">&bull;</span>
            <span class="bottom-link">Terms of Service</span>
            <span class="bottom-sep">&bull;</span>
            <span class="bottom-link">Pantry Code of Conduct</span>
          </div>
        </div>
      </div>
    </footer>
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
  return user.value.role === 'ADMIN' ? 'badge-admin' : 'badge-member'
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
  background-color: #FFFFFF;
  width: 100%;
  max-width: 100vw;
  overflow-x: hidden;
}

/* ── Full-Scale Header (#490982 Purple) ── */
.app-shell__header {
  position: sticky;
  top: 0;
  z-index: 100;
  background-color: #490982;
  box-shadow: 0 2px 12px rgba(73, 9, 130, 0.25);
  transition: all var(--transition-base);
  width: 100%;
  max-width: 100vw;
  box-sizing: border-box;
  overflow-x: clip;
}

.app-shell__header--scrolled {
  box-shadow: 0 4px 20px rgba(73, 9, 130, 0.4);
}

/* Edge-to-edge full width on laptop */
.app-shell__container {
  width: 100%;
  max-width: 100%;
  margin: 0;
  padding: 0.85rem clamp(1.25rem, 3.5vw, 3.5rem);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-6);
  box-sizing: border-box;
  min-width: 0;
}

/* Logo */
.app-shell__logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  text-decoration: none;
  transition: transform var(--transition-fast), opacity var(--transition-fast);
}

.app-shell__logo:hover {
  transform: translateY(-1px);
}

.app-shell__logo-icon-wrap {
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-md);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.app-shell__logo-icon {
  width: 100%;
  height: 100%;
}

.app-shell__logo-text-group {
  display: flex;
  flex-direction: column;
}

.app-shell__logo-text {
  font-family: var(--font-display);
  font-size: 1.35rem;
  font-weight: 700;
  color: #FFFFFF;
  line-height: 1.1;
  letter-spacing: -0.01em;
}

.app-shell__logo-subtext {
  font-size: 0.7rem;
  color: #D4B6F7;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

/* Desktop navigation */
.app-shell__nav--desktop {
  display: none;
  align-items: center;
  gap: var(--space-3);
}

.app-shell__nav-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-size: var(--text-sm);
  font-weight: 500;
  color: rgba(255, 255, 255, 0.85);
  text-decoration: none;
  padding: 0.55rem 1rem;
  border-radius: var(--radius-full);
  transition: all var(--transition-fast);
}

.nav-icon {
  width: 16px;
  height: 16px;
  opacity: 0.85;
}

.app-shell__nav-link:hover {
  color: #FFFFFF;
  background-color: rgba(255, 255, 255, 0.15);
}

.app-shell__nav-link--active {
  color: #490982;
  background-color: #FFFFFF;
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.app-shell__nav-link--active .nav-icon {
  stroke: #490982;
  opacity: 1;
}

/* User menu */
.app-shell__user {
  position: relative;
}

.app-shell__user-button {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  padding: 0.35rem 0.85rem 0.35rem 0.45rem;
  background-color: rgba(255, 255, 255, 0.14);
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: var(--radius-full);
  cursor: pointer;
  font-family: inherit;
  transition: all var(--transition-fast);
}

.app-shell__user-button:hover {
  background-color: rgba(255, 255, 255, 0.22);
}

.app-shell__user-avatar {
  width: 30px;
  height: 30px;
  border-radius: var(--radius-full);
  background-color: #FFFFFF;
  color: #490982;
  font-weight: 700;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.app-shell__user-meta {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.app-shell__user-name {
  font-size: var(--text-sm);
  font-weight: 500;
  color: #FFFFFF;
}

.badge-admin {
  background-color: #FBBF24;
  color: #78350F;
  font-size: 0.65rem;
  padding: 0.1rem 0.45rem;
  font-weight: 700;
  border-radius: var(--radius-full);
  text-transform: uppercase;
}

.badge-member {
  background-color: rgba(255, 255, 255, 0.25);
  color: #FFFFFF;
  font-size: 0.65rem;
  padding: 0.1rem 0.45rem;
  font-weight: 600;
  border-radius: var(--radius-full);
  text-transform: uppercase;
}

.app-shell__user-chevron {
  width: 14px;
  height: 14px;
  color: rgba(255, 255, 255, 0.7);
  transition: transform var(--transition-fast);
}

.app-shell__user-button[aria-expanded="true"] .app-shell__user-chevron {
  transform: rotate(180deg);
}

.app-shell__user-dropdown {
  position: absolute;
  top: calc(100% + var(--space-2));
  right: 0;
  min-width: 250px;
  max-width: calc(100vw - 2rem);
  box-sizing: border-box;
  background-color: #FFFFFF;
  border: 1px solid var(--color-peach);
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
  color: #190B2E;
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
  color: #190B2E;
  cursor: pointer;
  text-align: left;
  font-family: inherit;
  transition: background-color var(--transition-fast);
}

.app-shell__user-item:hover {
  background-color: #F8F4FD;
  color: #490982;
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
  background: rgba(255, 255, 255, 0.15);
  border: none;
  border-radius: var(--radius-md);
  color: #FFFFFF;
  cursor: pointer;
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
  background-color: #350661;
  border-bottom: 2px solid rgba(255, 255, 255, 0.15);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.25);
  width: 100%;
  max-width: 100vw;
  box-sizing: border-box;
  overflow-x: hidden;
}

.app-shell__mobile-user-card {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  background-color: rgba(255, 255, 255, 0.12);
  border-radius: var(--radius-lg);
  margin-bottom: var(--space-3);
  border: 1px solid rgba(255, 255, 255, 0.18);
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
  overflow: hidden;
}

.app-shell__mobile-avatar {
  width: 38px;
  height: 38px;
  border-radius: var(--radius-full);
  background-color: #FFFFFF;
  color: #490982;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  flex-shrink: 0;
}

.app-shell__mobile-user-meta,
.app-shell__mobile-user-details {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.app-shell__mobile-user-card .badge {
  flex-shrink: 0;
}

.app-shell__mobile-user-name {
  font-size: var(--text-sm);
  font-weight: 700;
  color: #FFFFFF;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  min-width: 0;
}

.app-shell__mobile-user-email {
  font-size: 0.75rem;
  color: #D4B6F7;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  min-width: 0;
}

.app-shell__mobile-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  font-size: var(--text-base);
  font-weight: 600;
  color: #FFFFFF;
  text-decoration: none;
  border-radius: var(--radius-lg);
  margin-bottom: var(--space-2);
  min-height: 44px;
  transition: all var(--transition-fast);
}

.mobile-nav-icon {
  width: 18px;
  height: 18px;
  opacity: 0.85;
}

.app-shell__mobile-link:hover,
.app-shell__mobile-link--active {
  background-color: #490982;
  color: #FFFFFF;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.app-shell__mobile-link--logout {
  color: #FCA5A5;
  background: none;
  border: none;
  cursor: pointer;
  text-align: left;
  font-family: inherit;
  width: 100%;
}

.app-shell__mobile-link--logout:hover {
  background-color: rgba(239, 68, 68, 0.2);
  color: #FECACA;
}

.app-shell__mobile-divider {
  height: 1px;
  background-color: rgba(255, 255, 255, 0.15);
  margin: var(--space-2) 0;
}

/* Main Content */
.app-shell__main {
  flex: 1;
}

/* ── Full-Scale Modern Footer (#490982 Purple) ── */
.app-shell__footer {
  width: 100%;
  background-color: #490982;
  color: #FFFFFF;
  margin-top: auto;
  border-top: 3px solid #6816B3;
}

.app-shell__footer-container {
  width: 100%;
  max-width: 100%;
  margin: 0;
  padding: 4rem clamp(1.25rem, 3.5vw, 3.5rem) 2rem;
  box-sizing: border-box;
}

.app-shell__footer-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2.5rem;
  margin-bottom: 3rem;
}

.app-shell__footer-col {
  display: flex;
  flex-direction: column;
}

.app-shell__footer-brand {
  max-width: 380px;
}

.app-shell__footer-logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.app-shell__footer-icon {
  width: 32px;
  height: 32px;
}

.app-shell__footer-title {
  font-family: var(--font-display);
  font-size: 1.5rem;
  font-weight: 700;
  color: #FFFFFF;
  letter-spacing: -0.01em;
}

.app-shell__footer-tagline {
  font-size: var(--text-sm);
  color: #D4B6F7;
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.app-shell__footer-status {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.35rem 0.85rem;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: var(--radius-full);
  border: 1px solid rgba(255, 255, 255, 0.15);
  width: fit-content;
}

.status-pulse {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #10B981;
  box-shadow: 0 0 8px #10B981;
}

.status-text {
  font-size: 0.75rem;
  font-weight: 600;
  color: #FFFFFF;
}

.app-shell__footer-heading {
  font-family: var(--font-display);
  font-size: 1.15rem;
  font-weight: 600;
  color: #FFFFFF;
  margin-bottom: 1.25rem;
  position: relative;
  padding-bottom: 0.5rem;
}

.app-shell__footer-heading::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: 0;
  width: 32px;
  height: 2px;
  background-color: #A855F7;
  border-radius: 2px;
}

.app-shell__footer-links {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
}

.app-shell__footer-links li a {
  color: #D4B6F7;
  text-decoration: none;
  font-size: var(--text-sm);
  transition: all var(--transition-fast);
  display: inline-block;
}

.app-shell__footer-links li a:hover {
  color: #FFFFFF;
  transform: translateX(3px);
}

.app-shell__footer-contact-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.contact-icon {
  width: 18px;
  height: 18px;
  stroke: #A855F7;
  flex-shrink: 0;
  margin-top: 0.2rem;
}

.contact-text {
  font-style: normal;
  font-size: var(--text-sm);
  color: #D4B6F7;
  line-height: 1.5;
  text-decoration: none;
}

a.contact-text:hover {
  color: #FFFFFF;
}

.app-shell__footer-social-intro {
  font-size: var(--text-sm);
  color: #D4B6F7;
  line-height: 1.5;
  margin-bottom: 1.25rem;
}

.app-shell__footer-socials {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.social-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: var(--radius-full);
  background-color: rgba(255, 255, 255, 0.12);
  color: #FFFFFF;
  transition: all var(--transition-fast);
  text-decoration: none;
  border: 1px solid rgba(255, 255, 255, 0.18);
}

.social-btn:hover {
  background-color: #FFFFFF;
  color: #490982;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
}

.social-btn svg {
  width: 18px;
  height: 18px;
}

.app-shell__footer-badge-box {
  margin-top: 0.5rem;
}

.palette-tag {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.3rem 0.75rem;
  background-color: rgba(168, 85, 247, 0.2);
  color: #E9D5FF;
  border-radius: var(--radius-full);
  border: 1px solid rgba(168, 85, 247, 0.4);
}

.app-shell__auth-actions {
  display: flex;
  align-items: center;
}

.app-shell__signin-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-size: var(--text-sm);
  font-weight: 600;
  color: #490982;
  background-color: #FFFFFF;
  text-decoration: none;
  padding: 0.5rem 1.15rem;
  border-radius: var(--radius-full);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.12);
  transition: all var(--transition-fast);
}

.app-shell__signin-btn:hover {
  background-color: #FAF5FE;
  transform: translateY(-1px);
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.18);
}

.app-shell__signin-btn--active {
  background-color: #F1E8F8;
  color: #490982;
  border: 1.5px solid rgba(255, 255, 255, 0.6);
}

/* Footer Bottom */
.app-shell__footer-bottom {
  padding-top: 2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.15);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.copyright-text {
  font-size: 0.85rem;
  color: #C4A1EC;
  margin: 0;
  text-align: center;
}

.bottom-links {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
  justify-content: center;
}

.bottom-link {
  font-size: 0.8rem;
  color: #D4B6F7;
  cursor: pointer;
  transition: color var(--transition-fast);
}

.bottom-link:hover {
  color: #FFFFFF;
}

.bottom-sep {
  color: rgba(255, 255, 255, 0.3);
  font-size: 0.8rem;
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

/* Mobile (< 768px) enhancements */
@media (max-width: 767px) {
  .app-shell__container {
    padding: 0.65rem 1rem;
    gap: 0.5rem;
  }

  .app-shell__logo {
    gap: 0.5rem;
  }

  .app-shell__logo-icon-wrap {
    width: 32px;
    height: 32px;
  }

  .app-shell__logo-text {
    font-size: 1.15rem;
  }

  .app-shell__logo-subtext {
    font-size: 0.6rem;
  }

  .app-shell__user-meta,
  .app-shell__user-chevron {
    display: none;
  }

  .app-shell__user-button {
    padding: 2px;
    background: transparent;
    border: 1.5px solid rgba(255, 255, 255, 0.4);
  }

  .app-shell__user-avatar {
    width: 32px;
    height: 32px;
    font-size: 0.8125rem;
  }

  .app-shell__mobile-toggle {
    width: 36px;
    height: 36px;
  }

  .app-shell__signin-btn {
    padding: 0.35rem 0.85rem;
    font-size: 0.8125rem;
  }

  .app-shell__footer-container {
    padding: 2.5rem 1rem 1.5rem;
  }

  .app-shell__footer-grid {
    gap: 1.75rem;
    margin-bottom: 2rem;
  }

  .app-shell__footer-brand {
    max-width: 100%;
  }

  .app-shell__footer-title {
    font-size: 1.25rem;
  }

  .app-shell__footer-tagline {
    font-size: 0.8125rem;
    margin-bottom: 1rem;
  }

  .app-shell__footer-heading {
    font-size: 1.05rem;
    margin-bottom: 0.85rem;
  }

  .bottom-links {
    gap: 0.5rem;
  }

  .bottom-link {
    font-size: 0.75rem;
  }
}

/* Responsive Breakpoints */
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

  .app-shell__footer-grid {
    grid-template-columns: 1.5fr 1fr 1.2fr 1fr;
    gap: 3rem;
  }

  .app-shell__footer-bottom {
    flex-direction: row;
  }

  .copyright-text {
    text-align: left;
  }
}

@media (min-width: 1200px) {
  .app-shell__container {
    padding-left: clamp(2rem, 5vw, 5rem);
    padding-right: clamp(2rem, 5vw, 5rem);
  }

  .app-shell__footer-container {
    padding-left: clamp(2rem, 5vw, 5rem);
    padding-right: clamp(2rem, 5vw, 5rem);
  }
}
</style>
