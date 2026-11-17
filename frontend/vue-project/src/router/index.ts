import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      meta: { requiresGuest: true },
    },
    {
      path: '/',
      name: 'dashboard',
      component: () => import('../views/DashboardView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/snacks',
      name: 'snacks',
      component: () => import('../views/SnacksView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/forbidden',
      name: 'forbidden',
      component: () => import('../views/ForbiddenView.vue'),
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('../views/NotFoundView.vue'),
    },
  ],
})

// Navigation guards
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // If we have a token but no user data, fetch the user
  if (authStore.token && !authStore.user) {
    await authStore.fetchMe()
  }

  const isAuthenticated = authStore.isAuthenticated
  const requiresAuth = to.meta.requiresAuth
  const requiresGuest = to.meta.requiresGuest

  // Redirect authenticated users away from login
  if (requiresGuest && isAuthenticated) {
    return next('/')
  }

  // Redirect unauthenticated users to login (preserve redirect target)
  if (requiresAuth && !isAuthenticated) {
    return next({
      name: 'login',
      query: { redirect: to.fullPath },
    })
  }

  next()
})

// Global error handler for route loading failures
router.onError((error) => {
  console.error('Router error:', error);
  // In production, you might want to show a global error state
})

export default router
