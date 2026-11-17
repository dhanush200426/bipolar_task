<template>
  <div class="login-view">
    <!-- Hero section with floating garnish layers -->
    <div class="login-view__hero" ref="heroRef">
      <div 
        class="login-view__garnish login-view__garnish--1"
        :style="garnish1Style"
        aria-hidden="true"
      >
        <svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M16 4L18 12L26 14L18 16L16 24L14 16L6 14L14 12L16 4Z" fill="#490982" opacity="0.6"/>
        </svg>
      </div>
      <div 
        class="login-view__garnish login-view__garnish--2"
        :style="garnish2Style"
        aria-hidden="true"
      >
        <svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M16 4L18 12L26 14L18 16L16 24L14 16L6 14L14 12L16 4Z" fill="#9B51E0" opacity="0.5"/>
        </svg>
      </div>
      <div 
        class="login-view__garnish login-view__garnish--3"
        :style="garnish3Style"
        aria-hidden="true"
      >
        <svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M16 4L18 12L26 14L18 16L16 24L14 16L6 14L14 12L16 4Z" fill="#6816B3" opacity="0.4"/>
        </svg>
      </div>
      
      <div class="login-view__hero-content">
        <h1 class="login-view__title">Snack Overflow</h1>
        <p class="login-view__subtitle">Your office pantry, organized</p>
      </div>
    </div>

    <!-- Login card -->
    <div class="login-view__card">
      <form @submit.prevent="handleSubmit" class="login-view__form" novalidate>
        <div class="login-view__field">
          <label for="email" class="login-view__label">Email</label>
          <input
            id="email"
            v-model="email"
            type="email"
            class="login-view__input"
            :class="{ 'login-view__input--error': emailError }"
            placeholder="you@example.com"
            @blur="validateEmail"
            required
          />
          <span v-if="emailError" class="login-view__error-text">{{ emailError }}</span>
        </div>

        <div class="login-view__field">
          <label for="password" class="login-view__label">Password</label>
          <div class="login-view__password-wrapper">
            <input
              id="password"
              v-model="password"
              :type="showPassword ? 'text' : 'password'"
              class="login-view__input login-view__input--password"
              :class="{ 'login-view__input--error': passwordError }"
              placeholder="••••••••"
              @blur="validatePassword"
              required
            />
            <button
              type="button"
              @click="showPassword = !showPassword"
              class="login-view__toggle-password"
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
          <span v-if="passwordError" class="login-view__error-text">{{ passwordError }}</span>
        </div>

        <div v-if="submitError" class="login-view__submit-error">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="8" x2="12" y2="12"/>
            <line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
          {{ submitError }}
        </div>

        <button
          type="submit"
          class="login-view__submit"
          :disabled="isLoading || !isFormValid"
        >
          <span v-if="!isLoading">Sign In</span>
          <span v-else class="login-view__loading">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10" stroke-opacity="0.25"/>
              <path d="M12 2a10 10 0 0 1 10 10" stroke-linecap="round"/>
            </svg>
            Signing in...
          </span>
        </button>
      </form>

      <!-- Demo accounts hint -->
      <div class="login-view__demo">
        <h3 class="login-view__demo-title">Demo Accounts</h3>
        <div class="login-view__demo-accounts">
          <div class="login-view__demo-account">
            <span class="login-view__demo-role badge badge-stocked">Admin</span>
            <span class="login-view__demo-email">admin@snackoverflow.com</span>
          </div>
          <div class="login-view__demo-account">
            <span class="login-view__demo-role badge badge-running-low">Member</span>
            <span class="login-view__demo-email">member@snackoverflow.com</span>
          </div>
        </div>
        <p class="login-view__demo-note">Use any password for demo accounts</p>
      </div>
    </div>
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

// Check for reduced motion preference
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
    // Redirect to the page the user was trying to access, or dashboard
    const redirect = route.query.redirect as string || '/'
    router.push(redirect)
  } else {
    const errorCode = result.error?.code as ErrorCode || 'NETWORK_ERROR'
    submitError.value = getErrorMessage(errorCode)
  }
}
</script>

<style scoped>
.login-view {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #FFFFFF 0%, #F5ECFC 100%);
}

/* Hero section */
.login-view__hero {
  position: relative;
  padding: var(--space-16) var(--space-6);
  text-align: center;
  overflow: hidden;
}

.login-view__garnish {
  position: absolute;
  width: 64px;
  height: 64px;
  pointer-events: none;
  transition: transform 0.1s ease-out;
}

.login-view__garnish--1 {
  top: 20%;
  left: 10%;
}

.login-view__garnish--2 {
  top: 60%;
  right: 15%;
}

.login-view__garnish--3 {
  bottom: 20%;
  left: 20%;
}

.login-view__hero-content {
  position: relative;
  z-index: 1;
}

.login-view__title {
  font-size: var(--text-4xl);
  color: var(--color-tomato);
  margin-bottom: var(--space-2);
}

.login-view__subtitle {
  font-size: var(--text-lg);
  color: var(--color-muted);
}

/* Login card */
.login-view__card {
  flex: 1;
  max-width: 400px;
  width: 100%;
  margin: 0 auto var(--space-12);
  padding: var(--space-8);
  background: white;
  border-radius: var(--radius-2xl);
  box-shadow: var(--shadow-xl);
}

.login-view__form {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

.login-view__field {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.login-view__label {
  font-size: var(--text-sm);
  font-weight: 600;
  color: var(--color-charcoal);
}

.login-view__input {
  padding: var(--space-3) var(--space-4);
  border: 2px solid var(--color-peach);
  border-radius: var(--radius-md);
  font-size: var(--text-base);
  font-family: inherit;
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
}

.login-view__input:focus {
  outline: none;
  border-color: #490982;
  box-shadow: 0 0 0 3px rgba(73, 9, 130, 0.15);
}

.login-view__input--error {
  border-color: var(--color-danger);
}

.login-view__input--error:focus {
  border-color: var(--color-danger);
  box-shadow: 0 0 0 3px rgba(211, 47, 47, 0.1);
}

.login-view__password-wrapper {
  position: relative;
}

.login-view__input--password {
  padding-right: var(--space-12);
}

.login-view__toggle-password {
  position: absolute;
  right: var(--space-3);
  top: 50%;
  transform: translateY(-50%);
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-muted);
  transition: color var(--transition-fast);
}

.login-view__toggle-password:hover {
  color: var(--color-charcoal);
}

.login-view__toggle-password svg {
  width: 20px;
  height: 20px;
}

.login-view__error-text {
  font-size: var(--text-xs);
  color: var(--color-danger);
}

.login-view__submit-error {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-4);
  background-color: rgba(211, 47, 47, 0.1);
  border-radius: var(--radius-md);
  color: var(--color-danger);
  font-size: var(--text-sm);
}

.login-view__submit-error svg {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.login-view__submit {
  padding: var(--space-4);
  background-color: var(--color-tomato);
  color: white;
  font-size: var(--text-base);
  font-weight: 600;
  border-radius: var(--radius-md);
  transition: background-color var(--transition-fast), opacity var(--transition-fast);
}

.login-view__submit:hover:not(:disabled) {
  background-color: var(--color-chili);
}

.login-view__submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.login-view__loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
}

.login-view__loading svg {
  width: 20px;
  height: 20px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* Demo accounts */
.login-view__demo {
  margin-top: var(--space-8);
  padding-top: var(--space-6);
  border-top: 1px solid var(--color-peach);
}

.login-view__demo-title {
  font-size: var(--text-sm);
  font-weight: 600;
  color: var(--color-muted);
  margin-bottom: var(--space-4);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.login-view__demo-accounts {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  margin-bottom: var(--space-4);
}

.login-view__demo-account {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3);
  background-color: var(--color-cream);
  border-radius: var(--radius-md);
}

.login-view__demo-email {
  font-size: var(--text-sm);
  color: var(--color-charcoal);
  font-family: monospace;
}

.login-view__demo-note {
  font-size: var(--text-xs);
  color: var(--color-muted);
  text-align: center;
}

@media (prefers-reduced-motion: reduce) {
  .login-view__garnish {
    transition: none;
  }
  
  .login-view__loading svg {
    animation: none;
  }
}

@media (min-width: 768px) {
  .login-view {
    flex-direction: row;
    align-items: center;
    justify-content: center;
    padding: var(--space-12);
  }
  
  .login-view__hero {
    flex: 1;
    padding: var(--space-12);
    text-align: left;
  }
  
  .login-view__card {
    margin: 0;
    margin-left: var(--space-12);
  }
}
</style>
