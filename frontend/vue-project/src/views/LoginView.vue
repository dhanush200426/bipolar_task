<template>
  <div class="login-view">
    <!-- Hero Section (Full Scale matching Dashboard) -->
    <section class="login-view__hero" ref="heroRef">
      <div 
        class="login-view__garnish login-view__garnish--1"
        :style="garnish1Style"
        aria-hidden="true"
      >
        <svg viewBox="0 0 32 32" fill="none">
          <path d="M16 4L18 12L26 14L18 16L16 24L14 16L6 14L14 12L16 4Z" fill="#E9D5FF" opacity="0.6"/>
        </svg>
      </div>
      <div 
        class="login-view__garnish login-view__garnish--2"
        :style="garnish2Style"
        aria-hidden="true"
      >
        <svg viewBox="0 0 32 32" fill="none">
          <path d="M16 4L18 12L26 14L18 16L16 24L14 16L6 14L14 12L16 4Z" fill="#C084FC" opacity="0.5"/>
        </svg>
      </div>
      <div 
        class="login-view__garnish login-view__garnish--3"
        :style="garnish3Style"
        aria-hidden="true"
      >
        <svg viewBox="0 0 32 32" fill="none">
          <circle cx="16" cy="16" r="6" fill="#A855F7" opacity="0.4"/>
        </svg>
      </div>

      <div class="login-view__hero-container">
        <div class="login-view__hero-badge">
          <span class="live-dot"></span>
          <span>Snack Overflow Portal</span>
        </div>
        <h1 class="login-view__hero-title">Welcome to Your Office Pantry</h1>
        <p class="login-view__hero-subtitle">
          Sign in to track real-time stock levels, vote for weekly snacks, or manage pantry supplies.
        </p>
      </div>
    </section>

    <!-- Main Content Container (Full Scale Edge-to-Edge like Dashboard) -->
    <main class="login-view__main">
      <div class="login-view__container">
        <div class="login-view__layout">
          <!-- Left Column: Feature Highlights & Quick Fill Demo Accounts -->
          <div class="login-view__info-panel">
            <div class="info-card">
              <h2 class="info-card__title">Why Snack Overflow?</h2>
              <p class="info-card__desc">
                High-performance teams run on good snacks. Our intelligent pantry OS eliminates guesswork and keeps everyone energized.
              </p>

              <div class="feature-pills">
                <div class="feature-pill">
                  <div class="feature-pill__icon feature-pill__icon--radar">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/>
                    </svg>
                  </div>
                  <div class="feature-pill__content">
                    <h4>Live Stock Radar</h4>
                    <p>Instant status alerts when snacks are stocked, running low, or completely gone.</p>
                  </div>
                </div>

                <div class="feature-pill">
                  <div class="feature-pill__icon feature-pill__icon--vote">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
                    </svg>
                  </div>
                  <div class="feature-pill__content">
                    <h4>Democratic Snack of the Week</h4>
                    <p>Cast your vote every Friday to crown the office's most popular pantry snack.</p>
                  </div>
                </div>

                <div class="feature-pill">
                  <div class="feature-pill__icon feature-pill__icon--restock">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
                    </svg>
                  </div>
                  <div class="feature-pill__content">
                    <h4>Instant Restock & Auditing</h4>
                    <p>Admins manage inventory in real time with atomic stock updates and audit trails.</p>
                  </div>
                </div>
              </div>

              <!-- Quick Demo Account Switcher -->
              <div class="quick-demo-section">
                <div class="quick-demo-header">
                  <span class="quick-demo-label">⚡ Quick-Fill Demo Credentials</span>
                  <span class="quick-demo-hint">Click a card to auto-populate</span>
                </div>
                <div class="quick-demo-cards">
                  <button
                    type="button"
                    class="quick-demo-card"
                    :class="{ 'quick-demo-card--selected': email === 'admin@snackoverflow.com' }"
                    @click="fillDemoAccount('admin@snackoverflow.com')"
                  >
                    <div class="demo-card-top">
                      <span class="demo-role-badge demo-role-badge--admin">Admin</span>
                      <span class="demo-click-hint">Click to Fill</span>
                    </div>
                    <div class="demo-email">admin@snackoverflow.com</div>
                    <div class="demo-desc">Full CRUD rights, add snacks, restock, edit & delete</div>
                  </button>

                  <button
                    type="button"
                    class="quick-demo-card"
                    :class="{ 'quick-demo-card--selected': email === 'member@snackoverflow.com' }"
                    @click="fillDemoAccount('member@snackoverflow.com')"
                  >
                    <div class="demo-card-top">
                      <span class="demo-role-badge demo-role-badge--member">Member</span>
                      <span class="demo-click-hint">Click to Fill</span>
                    </div>
                    <div class="demo-email">member@snackoverflow.com</div>
                    <div class="demo-desc">Browse inventory, vote on snacks, view live stock</div>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Right Column: Login Form Card -->
          <div class="login-view__form-panel">
            <div class="login-card">
              <div class="login-card__header">
                <h2 class="login-card__title">Sign In</h2>
                <p class="login-card__subtitle">Enter your email and password to access the pantry</p>
              </div>

              <form @submit.prevent="handleSubmit" class="login-card__form" novalidate>
                <div class="login-card__field">
                  <label for="email" class="login-card__label">Work Email</label>
                  <input
                    id="email"
                    v-model="email"
                    type="email"
                    class="login-card__input"
                    :class="{ 'login-card__input--error': emailError }"
                    placeholder="name@snackoverflow.com"
                    @blur="validateEmail"
                    required
                  />
                  <span v-if="emailError" class="login-card__error-text">{{ emailError }}</span>
                </div>

                <div class="login-card__field">
                  <div class="login-card__label-row">
                    <label for="password" class="login-card__label">Password</label>
                    <span class="login-card__demo-tag">Any password accepted for demo</span>
                  </div>
                  <div class="login-card__password-wrapper">
                    <input
                      id="password"
                      v-model="password"
                      :type="showPassword ? 'text' : 'password'"
                      class="login-card__input login-card__input--password"
                      :class="{ 'login-card__input--error': passwordError }"
                      placeholder="••••••••••••"
                      @blur="validatePassword"
                      required
                    />
                    <button
                      type="button"
                      @click="showPassword = !showPassword"
                      class="login-card__toggle-password"
                      :aria-label="showPassword ? 'Hide password' : 'Show password'"
                    >
                      <svg v-if="showPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                        <line x1="1" y1="1" x2="23" y2="23"/>
                      </svg>
                      <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                        <circle cx="12" cy="12" r="3"/>
                      </svg>
                    </button>
                  </div>
                  <span v-if="passwordError" class="login-card__error-text">{{ passwordError }}</span>
                </div>

                <div v-if="submitError" class="login-card__submit-error" role="alert">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
                    <circle cx="12" cy="10" r="10"/>
                    <line x1="12" y1="8" x2="12" y2="12"/>
                    <line x1="12" y1="16" x2="12.01" y2="16"/>
                  </svg>
                  <span>{{ submitError }}</span>
                </div>

                <button
                  type="submit"
                  class="login-card__submit-btn"
                  :disabled="isLoading || !isFormValid"
                >
                  <span v-if="!isLoading">Sign In to Snack Overflow</span>
                  <span v-else class="login-card__loading">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <circle cx="12" cy="12" r="10" stroke-opacity="0.25"/>
                      <path d="M12 2a10 10 0 0 1 10 10" stroke-linecap="round"/>
                    </svg>
                    Signing in...
                  </span>
                </button>
              </form>

              <div class="login-card__footer">
                <div class="security-note">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                    <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                  </svg>
                  <span>Protected by Argon2id & JWT Authentication</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { getErrorMessage } from '../utils/errorMessages'
import type { ErrorCode } from '../api/types'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const showPassword = ref(false)
const emailError = ref('')
const passwordError = ref('')
const submitError = ref('')

const heroRef = ref<HTMLElement>()
const mouseX = ref(0)
const mouseY = ref(0)
const prefersReducedMotion = ref(false)

// Quick autofill demo credentials
function fillDemoAccount(demoEmail: string) {
  email.value = demoEmail
  password.value = 'DemoPass2026!'
  emailError.value = ''
  passwordError.value = ''
  submitError.value = ''
}

// Check for reduced motion preference & parallax mouse tracking
onMounted(() => {
  prefersReducedMotion.value = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  if (!prefersReducedMotion.value && window.innerWidth >= 768) {
    window.addEventListener('mousemove', handleMouseMove)
  }
})

onUnmounted(() => {
  window.removeEventListener('mousemove', handleMouseMove)
})

function handleMouseMove(event: MouseEvent) {
  if (!heroRef.value) return
  const rect = heroRef.value.getBoundingClientRect()
  const centerX = rect.left + rect.width / 2
  const centerY = rect.top + rect.height / 2
  mouseX.value = (event.clientX - centerX) / rect.width
  mouseY.value = (event.clientY - centerY) / rect.height
}

const garnish1Style = computed(() => {
  if (prefersReducedMotion.value) return {}
  return {
    transform: `translate(${mouseX.value * 20}px, ${mouseY.value * 20}px)`,
  }
})

const garnish2Style = computed(() => {
  if (prefersReducedMotion.value) return {}
  return {
    transform: `translate(${mouseX.value * -15}px, ${mouseY.value * -15}px)`,
  }
})

const garnish3Style = computed(() => {
  if (prefersReducedMotion.value) return {}
  return {
    transform: `translate(${mouseX.value * 10}px, ${mouseY.value * 25}px)`,
  }
})

function validateEmail() {
  if (!email.value) {
    emailError.value = 'Email is required'
    return false
  }
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(email.value)) {
    emailError.value = 'Please enter a valid email'
    return false
  }
  emailError.value = ''
  return true
}

function validatePassword() {
  if (!password.value) {
    passwordError.value = 'Password is required'
    return false
  }
  if (password.value.length < 1) {
    passwordError.value = 'Password is required'
    return false
  }
  passwordError.value = ''
  return true
}

const isFormValid = computed(() => {
  return email.value && password.value && !emailError.value && !passwordError.value
})

const isLoading = computed(() => authStore.isLoading)

async function handleSubmit() {
  submitError.value = ''
  
  const isEmailValid = validateEmail()
  const isPasswordValid = validatePassword()
  
  if (!isEmailValid || !isPasswordValid) {
    return
  }

  const result = await authStore.login(email.value.toLowerCase(), password.value)
  
  if (result.success) {
    const redirect = (route.query.redirect as string) || '/'
    router.push(redirect)
  } else {
    const errorCode = (result.error?.code as ErrorCode) || 'NETWORK_ERROR'
    submitError.value = getErrorMessage(errorCode)
  }
}
</script>

<style scoped>
.login-view {
  min-height: calc(100vh - 68px);
  display: flex;
  flex-direction: column;
  background-color: #FAF7FD;
}

/* Hero Section (Matching Dashboard Hero Scale) */
.login-view__hero {
  position: relative;
  width: 100%;
  max-width: 100%;
  padding: clamp(2rem, 4vw, 3.5rem) clamp(1.25rem, 3.5vw, 3.5rem);
  background: linear-gradient(135deg, #490982 0%, #350661 50%, #6816B3 100%);
  color: #FFFFFF;
  overflow: hidden;
  box-sizing: border-box;
}

.login-view__hero-container {
  position: relative;
  z-index: 2;
  max-width: 800px;
}

.login-view__hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.35rem 0.85rem;
  background-color: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: var(--radius-full);
  font-size: var(--text-xs);
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: #F3EAFB;
  margin-bottom: var(--space-4);
}

.live-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background-color: #4ADE80;
  box-shadow: 0 0 8px #4ADE80;
}

.login-view__hero-title {
  font-family: var(--font-display);
  font-size: clamp(2rem, 3.5vw, 3rem);
  font-weight: 800;
  color: #FFFFFF;
  line-height: 1.15;
  margin-bottom: var(--space-3);
  letter-spacing: -0.02em;
}

.login-view__hero-subtitle {
  font-size: clamp(1rem, 1.35vw, 1.2rem);
  color: #E6D7F6;
  line-height: 1.5;
  max-width: 640px;
}

/* Floating Garnishes */
.login-view__garnish {
  position: absolute;
  width: 64px;
  height: 64px;
  pointer-events: none;
  transition: transform 0.15s ease-out;
}

.login-view__garnish--1 {
  top: 15%;
  right: 12%;
}

.login-view__garnish--2 {
  bottom: 20%;
  right: 25%;
}

.login-view__garnish--3 {
  top: 40%;
  right: 6%;
}

/* Main Content Container (Full Scale Edge-to-Edge like Dashboard) */
.login-view__main {
  flex: 1;
  width: 100%;
}

.login-view__container {
  width: 100%;
  max-width: 100%;
  margin: 0;
  padding: var(--space-8) clamp(1.25rem, 3.5vw, 3.5rem);
  box-sizing: border-box;
}

.login-view__layout {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-8);
  align-items: start;
}

@media (min-width: 960px) {
  .login-view__layout {
    grid-template-columns: 1.15fr 1fr;
    gap: clamp(2rem, 4vw, 4rem);
  }
}

/* Left Column: Info & Quick Demo */
.info-card {
  background-color: #FFFFFF;
  border: 1px solid #EADBFA;
  border-radius: var(--radius-2xl);
  padding: clamp(1.5rem, 2.5vw, 2.5rem);
  box-shadow: 0 4px 20px rgba(73, 9, 130, 0.05);
}

.info-card__title {
  font-family: var(--font-display);
  font-size: clamp(1.4rem, 2vw, 1.85rem);
  font-weight: 700;
  color: #190B2E;
  margin-bottom: var(--space-2);
}

.info-card__desc {
  font-size: var(--text-sm);
  color: #6C5D82;
  line-height: 1.6;
  margin-bottom: var(--space-6);
}

.feature-pills {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  margin-bottom: var(--space-8);
}

.feature-pill {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1rem;
  background-color: #FAF7FD;
  border: 1px solid #EADBFA;
  border-radius: var(--radius-lg);
  transition: transform var(--transition-fast), border-color var(--transition-fast);
}

.feature-pill:hover {
  transform: translateX(4px);
  border-color: #490982;
}

.feature-pill__icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  flex-shrink: 0;
}

.feature-pill__icon--radar {
  background-color: #F1E8F8;
  color: #490982;
}

.feature-pill__icon--vote {
  background-color: #FEF3C7;
  color: #D97706;
}

.feature-pill__icon--restock {
  background-color: #D1FAE5;
  color: #059669;
}

.feature-pill__icon svg {
  width: 20px;
  height: 20px;
}

.feature-pill__content h4 {
  font-size: var(--text-sm);
  font-weight: 700;
  color: #190B2E;
  margin-bottom: 0.2rem;
}

.feature-pill__content p {
  font-size: 0.8125rem;
  color: #6C5D82;
  line-height: 1.4;
  margin: 0;
}

/* Quick Demo Section */
.quick-demo-section {
  padding-top: var(--space-6);
  border-top: 1px solid #EADBFA;
}

.quick-demo-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-3);
  flex-wrap: wrap;
  gap: 0.5rem;
}

.quick-demo-label {
  font-size: var(--text-xs);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #490982;
}

.quick-demo-hint {
  font-size: 0.75rem;
  color: #6C5D82;
}

.quick-demo-cards {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-3);
}

@media (min-width: 640px) {
  .quick-demo-cards {
    grid-template-columns: 1fr 1fr;
  }
}

.quick-demo-card {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  text-align: left;
  padding: 0.85rem 1rem;
  background-color: #FFFFFF;
  border: 1.5px solid #EADBFA;
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.quick-demo-card:hover {
  border-color: #490982;
  background-color: #FAF5FE;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(73, 9, 130, 0.08);
}

.quick-demo-card--selected {
  border-color: #490982;
  background-color: #F1E8F8;
  box-shadow: 0 0 0 2px rgba(73, 9, 130, 0.2);
}

.demo-card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  margin-bottom: 0.35rem;
}

.demo-role-badge {
  font-size: 0.7rem;
  font-weight: 700;
  padding: 0.15rem 0.5rem;
  border-radius: var(--radius-full);
  text-transform: uppercase;
}

.demo-role-badge--admin {
  background-color: #490982;
  color: #FFFFFF;
}

.demo-role-badge--member {
  background-color: #6816B3;
  color: #FFFFFF;
}

.demo-click-hint {
  font-size: 0.6875rem;
  color: #490982;
  font-weight: 600;
}

.demo-email {
  font-family: monospace;
  font-size: 0.8125rem;
  font-weight: 600;
  color: #190B2E;
  margin-bottom: 0.25rem;
}

.demo-desc {
  font-size: 0.75rem;
  color: #6C5D82;
  line-height: 1.3;
}

/* Right Column: Form Panel */
.login-card {
  background-color: #FFFFFF;
  border: 1px solid #EADBFA;
  border-radius: var(--radius-2xl);
  padding: clamp(1.75rem, 3vw, 2.75rem);
  box-shadow: 0 10px 30px rgba(73, 9, 130, 0.08);
}

.login-card__header {
  margin-bottom: var(--space-6);
}

.login-card__title {
  font-family: var(--font-display);
  font-size: clamp(1.6rem, 2.2vw, 2rem);
  font-weight: 700;
  color: #190B2E;
  margin-bottom: 0.35rem;
}

.login-card__subtitle {
  font-size: var(--text-sm);
  color: #6C5D82;
}

.login-card__form {
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
}

.login-card__field {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.login-card__label-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.login-card__label {
  font-size: var(--text-sm);
  font-weight: 600;
  color: #190B2E;
}

.login-card__demo-tag {
  font-size: 0.7rem;
  color: #6C5D82;
  font-weight: 500;
}

.login-card__input {
  width: 100%;
  height: 48px;
  padding: 0 1rem;
  border: 1.5px solid #EADBFA;
  border-radius: var(--radius-lg);
  font-size: var(--text-base);
  color: #190B2E;
  background-color: #FFFFFF;
  box-sizing: border-box;
  transition: all var(--transition-fast);
}

.login-card__input:focus {
  outline: none;
  border-color: #490982;
  box-shadow: 0 0 0 3px rgba(73, 9, 130, 0.15);
}

.login-card__input--error {
  border-color: #EF4444;
}

.login-card__input--error:focus {
  border-color: #EF4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.15);
}

.login-card__password-wrapper {
  position: relative;
  width: 100%;
}

.login-card__input--password {
  padding-right: 3rem;
}

.login-card__toggle-password {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: none;
  background: transparent;
  color: #6C5D82;
  cursor: pointer;
  border-radius: var(--radius-sm);
}

.login-card__toggle-password:hover {
  color: #490982;
}

.login-card__toggle-password svg {
  width: 20px;
  height: 20px;
}

.login-card__error-text {
  font-size: var(--text-xs);
  color: #EF4444;
  font-weight: 500;
}

.login-card__submit-error {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background-color: #FEE2E2;
  border: 1px solid #FECACA;
  border-radius: var(--radius-md);
  color: #B91C1C;
  font-size: var(--text-sm);
  font-weight: 500;
}

.login-card__submit-error svg {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.login-card__submit-btn {
  width: 100%;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #490982;
  color: #FFFFFF;
  border: none;
  border-radius: var(--radius-lg);
  font-size: var(--text-base);
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 4px 14px rgba(73, 9, 130, 0.25);
  transition: all var(--transition-fast);
}

.login-card__submit-btn:hover:not(:disabled) {
  background-color: #350661;
  transform: translateY(-1px);
  box-shadow: 0 6px 18px rgba(73, 9, 130, 0.35);
}

.login-card__submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  box-shadow: none;
}

.login-card__loading {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.login-card__loading svg {
  width: 20px;
  height: 20px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.login-card__footer {
  margin-top: var(--space-6);
  padding-top: var(--space-4);
  border-top: 1px solid #EADBFA;
}

.security-note {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.45rem;
  font-size: 0.75rem;
  color: #6C5D82;
}

.security-note svg {
  width: 14px;
  height: 14px;
  color: #490982;
}

/* Mobile Enhancements (< 768px) */
@media (max-width: 767px) {
  .login-view__hero {
    padding: 2rem 1rem 1.5rem;
  }

  .login-view__hero-badge {
    margin-bottom: var(--space-2);
    font-size: 0.7rem;
    padding: 0.25rem 0.65rem;
  }

  .login-view__hero-title {
    font-size: 1.75rem;
    line-height: 1.2;
    margin-bottom: 0.5rem;
  }

  .login-view__hero-subtitle {
    font-size: 0.875rem;
    line-height: 1.45;
  }

  .login-view__container {
    padding: 1.25rem 1rem;
  }

  .login-view__layout {
    gap: 1.25rem;
  }

  .info-card {
    padding: 1.25rem;
    border-radius: var(--radius-xl);
  }

  .info-card__title {
    font-size: 1.35rem;
  }

  .info-card__desc {
    font-size: 0.8125rem;
    margin-bottom: 1rem;
  }

  .feature-pills {
    gap: 0.5rem;
    margin-bottom: 1.25rem;
  }

  .feature-pill {
    padding: 0.75rem;
    gap: 0.65rem;
    border-radius: var(--radius-md);
  }

  .feature-pill__icon {
    width: 32px;
    height: 32px;
  }

  .feature-pill__icon svg {
    width: 16px;
    height: 16px;
  }

  .feature-pill__content h4 {
    font-size: 0.8125rem;
  }

  .feature-pill__content p {
    font-size: 0.75rem;
  }

  .quick-demo-section {
    padding-top: 1rem;
  }

  .quick-demo-card {
    padding: 0.75rem;
    border-radius: var(--radius-md);
  }

  .login-card {
    padding: 1.5rem 1.15rem;
    border-radius: var(--radius-xl);
  }

  .login-card__header {
    margin-bottom: var(--space-4);
  }

  .login-card__title {
    font-size: 1.45rem;
  }

  .login-card__subtitle {
    font-size: 0.8125rem;
  }

  .login-card__input {
    height: 44px;
    font-size: 0.9375rem;
  }

  .login-card__submit-btn {
    height: 46px;
    font-size: 0.9375rem;
  }
}
</style>