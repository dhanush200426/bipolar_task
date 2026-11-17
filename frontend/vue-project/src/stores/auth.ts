import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '../api/auth'
import { setAuthToken, clearAuthToken, getAuthToken } from '../api/client'
import type { User } from '../api/types'

/**
 * AUTH STORE SECURITY NOTE:
 * 
 * We store the JWT token in localStorage for simplicity in this assignment.
 * 
 * Trade-offs:
 * - localStorage: Vulnerable to XSS attacks. If malicious JS runs on the page,
 *   it can read the token and make API requests on behalf of the user.
 * - httpOnly cookies: More secure against XSS (JS cannot read them), but
 *   require CSRF protection and are harder to implement with SPA refresh tokens.
 * 
 * For a production app, consider:
 * 1. httpOnly cookies for the token
 * 2. CSRF tokens for state-changing requests
 * 3. Short-lived tokens with refresh token rotation
 * 4. Content Security Policy (CSP) headers to mitigate XSS
 * 
 * For this assignment, localStorage is acceptable given the scope and the fact
 * that we're building a controlled internal office pantry app.
 */

const TOKEN_KEY = 'snack_overflow_token'
const USER_KEY = 'snack_overflow_user'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(getAuthToken())
  const user = ref<User | null>(null)
  const isLoading = ref(false)

  // Initialize from localStorage
  function initFromStorage() {
    const storedToken = localStorage.getItem(TOKEN_KEY)
    const storedUser = localStorage.getItem(USER_KEY)
    
    if (storedToken) {
      token.value = storedToken
      setAuthToken(storedToken)
    }
    
    if (storedUser) {
      try {
        user.value = JSON.parse(storedUser)
      } catch {
        // Invalid stored user, clear it
        localStorage.removeItem(USER_KEY)
      }
    }
  }

  // Persist to localStorage
  function persist() {
    if (token.value) {
      localStorage.setItem(TOKEN_KEY, token.value)
    } else {
      localStorage.removeItem(TOKEN_KEY)
    }
    
    if (user.value) {
      localStorage.setItem(USER_KEY, JSON.stringify(user.value))
    } else {
      localStorage.removeItem(USER_KEY)
    }
  }

  // Computed
  const isAuthenticated = computed(() => !!token.value && !!user.value)
  const isAdmin = computed(() => user.value?.role === 'ADMIN')
  const isMember = computed(() => user.value?.role === 'MEMBER')

  // Actions
  async function login(email: string, password: string) {
    isLoading.value = true
    try {
      const response = await authApi.login({ email, password })
      token.value = response.access_token
      user.value = response.user
      setAuthToken(response.access_token)
      persist()
      return { success: true }
    } catch (error: any) {
      return { success: false, error }
    } finally {
      isLoading.value = false
    }
  }

  async function fetchMe() {
    if (!token.value) {
      return
    }

    isLoading.value = true
    try {
      const userData = await authApi.getMe()
      user.value = userData
      persist()
    } catch (error) {
      // Token is invalid or expired, clear session
      logout()
    } finally {
      isLoading.value = false
    }
  }

  function logout() {
    token.value = null
    user.value = null
    clearAuthToken()
    persist()
  }

  // Initialize on store creation
  initFromStorage()

  return {
    token,
    user,
    isLoading,
    isAuthenticated,
    isAdmin,
    isMember,
    login,
    fetchMe,
    logout,
  }
})
