<template>
  <div class="dashboard-view" ref="dashboardRef">
    <!-- Hero Section -->
    <section class="dashboard-view__hero">
      <div class="dashboard-view__hero-garnishes">
        <div class="dashboard-view__garnish dashboard-view__garnish--1" ref="garnish1Ref" aria-hidden="true">
          <svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M16 4L18 12L26 14L18 16L16 24L14 16L6 14L14 12L16 4Z" fill="#E4472B" opacity="0.6"/>
          </svg>
        </div>
        <div class="dashboard-view__garnish dashboard-view__garnish--2" ref="garnish2Ref" aria-hidden="true">
          <svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M16 4L18 12L26 14L18 16L16 24L14 16L6 14L14 12L16 4Z" fill="#F7B733" opacity="0.5"/>
          </svg>
        </div>
        <div class="dashboard-view__garnish dashboard-view__garnish--3" ref="garnish3Ref" aria-hidden="true">
          <svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M16 4L18 12L26 14L18 16L16 24L14 16L6 14L14 12L16 4Z" fill="#F58A1F" opacity="0.4"/>
          </svg>
        </div>
        <div class="dashboard-view__garnish dashboard-view__garnish--4" ref="garnish4Ref" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="3" fill="#C8321A" opacity="0.5"/>
          </svg>
        </div>
        <div class="dashboard-view__garnish dashboard-view__garnish--5" ref="garnish5Ref" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="2" fill="#F7B733" opacity="0.4"/>
          </svg>
        </div>
      </div>
      
      <div class="dashboard-view__hero-content">
        <h1 class="dashboard-view__headline">Never miss the last packet again</h1>
        <p class="dashboard-view__greeting">Hi, {{ user?.name || 'there' }} 👋</p>
        <div class="dashboard-view__hero-illustration" ref="heroIllustrationRef">
          <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="12" y="8" width="40" height="48" rx="4" fill="#F58A1F" stroke="#C8321A" stroke-width="2"/>
            <rect x="16" y="16" width="32" height="8" rx="2" fill="#FFF8EE"/>
            <rect x="16" y="28" width="32" height="8" rx="2" fill="#FFF8EE"/>
            <rect x="16" y="40" width="32" height="8" rx="2" fill="#FFF8EE"/>
          </svg>
        </div>
      </div>
    </section>

    <!-- Loading State -->
    <div v-if="isLoading" class="dashboard-view__container">
      <div class="dashboard-view__skeleton-cards">
        <div v-for="i in 4" :key="i" class="dashboard-view__skeleton-card"></div>
      </div>
    </div>

    <!-- Error State -->
    <ErrorState
      v-else-if="error"
      title="Couldn't load pantry data"
      :message="error"
      :show-retry="true"
      @retry="fetchData"
    />

    <!-- Empty State -->
    <EmptyState
      v-else-if="!summary"
      title="Pantry is empty"
      message="No snacks have been added yet. Ask an admin to stock up!"
    />

    <!-- Dashboard Content -->
    <template v-else>
      <!-- Summary Cards -->
      <section class="dashboard-view__summary" ref="summaryRef">
        <div class="dashboard-view__container">
          <div class="dashboard-view__cards">
            <div 
              class="dashboard-view__card dashboard-view__card--stocked"
              @click="navigateToSnacks('stocked')"
              ref="cardStockedRef"
            >
              <div class="dashboard-view__card-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                  <polyline points="22 4 12 14.01 9 11.01"/>
                </svg>
              </div>
              <div class="dashboard-view__card-content">
                <span class="dashboard-view__card-label">Stocked</span>
                <span class="dashboard-view__card-value">{{ animatedStocked }}</span>
              </div>
            </div>

            <div 
              class="dashboard-view__card dashboard-view__card--running-low"
              @click="navigateToSnacks('running_low')"
              ref="cardRunningLowRef"
            >
              <div class="dashboard-view__card-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
                  <line x1="12" y1="9" x2="12" y2="13"/>
                  <line x1="12" y1="17" x2="12.01" y2="17"/>
                </svg>
              </div>
              <div class="dashboard-view__card-content">
                <span class="dashboard-view__card-label">Running Low</span>
                <span class="dashboard-view__card-value">{{ animatedRunningLow }}</span>
              </div>
            </div>

            <div 
              class="dashboard-view__card dashboard-view__card--gone"
              @click="navigateToSnacks('gone')"
              ref="cardGoneRef"
            >
              <div class="dashboard-view__card-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"/>
                  <line x1="15" y1="9" x2="9" y2="15"/>
                  <line x1="9" y1="9" x2="15" y2="15"/>
                </svg>
              </div>
              <div class="dashboard-view__card-content">
                <span class="dashboard-view__card-label">Gone</span>
                <span class="dashboard-view__card-value">{{ animatedGone }}</span>
              </div>
            </div>

            <div 
              class="dashboard-view__card dashboard-view__card--total"
              ref="cardTotalRef"
            >
              <div class="dashboard-view__card-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                  <line x1="3" y1="9" x2="21" y2="9"/>
                  <line x1="9" y1="21" x2="9" y2="9"/>
                </svg>
              </div>
              <div class="dashboard-view__card-content">
                <span class="dashboard-view__card-label">Total</span>
                <span class="dashboard-view__card-value">{{ animatedTotal }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Snack of the Week -->
      <section class="dashboard-view__snack-of-week" ref="snackOfWeekRef">
        <div class="dashboard-view__container">
          <EmptyState
            v-if="!summary.snack_of_the_week"
            title="No votes yet"
            message="Be the first to pick a favorite snack!"
          />
          <div v-else class="dashboard-view__sow-content">
            <div class="dashboard-view__sow-illustration" ref="sowIllustrationRef">
              <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="12" y="8" width="40" height="48" rx="4" fill="#F58A1F" stroke="#C8321A" stroke-width="2"/>
                <rect x="16" y="16" width="32" height="8" rx="2" fill="#FFF8EE"/>
                <rect x="16" y="28" width="32" height="8" rx="2" fill="#FFF8EE"/>
                <rect x="16" y="40" width="32" height="8" rx="2" fill="#FFF8EE"/>
              </svg>
            </div>
            <div class="dashboard-view__sow-info">
              <div class="dashboard-view__sow-callout" ref="sowCallout1Ref">
                <h2 class="dashboard-view__sow-name">{{ summary.snack_of_the_week.name }}</h2>
                <span class="dashboard-view__sow-category badge">{{ summary.snack_of_the_week.category }}</span>
              </div>
              <div class="dashboard-view__sow-callout" ref="sowCallout2Ref">
                <div class="dashboard-view__sow-stat">
                  <span class="dashboard-view__sow-stat-label">Votes</span>
                  <span class="dashboard-view__sow-stat-value">{{ summary.snack_of_the_week.vote_count }}</span>
                </div>
              </div>
              <div class="dashboard-view__sow-callout" ref="sowCallout3Ref">
                <button 
                  @click="handleVote"
                  class="dashboard-view__sow-vote"
                  :disabled="isVoting"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-3.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"/>
                  </svg>
                  {{ hasVoted ? 'Unvote' : 'Vote' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Running Low -->
      <section class="dashboard-view__running-low" ref="runningLowRef">
        <div class="dashboard-view__container">
          <div class="dashboard-view__section-header">
            <h2 class="dashboard-view__section-title">Running Low</h2>
            <router-link to="/snacks?status=running_low" class="dashboard-view__section-link">
              View All
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="9 18 15 12 9 6"/>
              </svg>
            </router-link>
          </div>
          
          <EmptyState
            v-if="runningLowSnacks.length === 0"
            title="All stocked up!"
            message="No snacks are running low right now."
          />
          <div v-else class="dashboard-view__scroll-row">
            <button 
              @click="scrollLeft" 
              class="dashboard-view__scroll-arrow dashboard-view__scroll-arrow--left"
              aria-label="Scroll left"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="15 18 9 12 15 6"/>
              </svg>
            </button>
            
            <div class="dashboard-view__scroll-container" ref="scrollContainerRef">
              <div 
                v-for="snack in runningLowSnacks" 
                :key="snack.id"
                class="dashboard-view__scroll-item"
                @click="navigateToSnack(snack.id)"
              >
                <div class="dashboard-view__scroll-item-illustration">
                  <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="12" y="8" width="40" height="48" rx="4" fill="#F58A1F" stroke="#C8321A" stroke-width="2"/>
                    <rect x="16" y="16" width="32" height="8" rx="2" fill="#FFF8EE"/>
                    <rect x="16" y="28" width="32" height="8" rx="2" fill="#FFF8EE"/>
                    <rect x="16" y="40" width="32" height="8" rx="2" fill="#FFF8EE"/>
                  </svg>
                </div>
                <span class="dashboard-view__scroll-item-name">{{ snack.name }}</span>
 <span class="dashboard-view__scroll-item-quantity">{{ snack.quantity }} left</span>
              </div>
            </div>
            
            <button 
              @click="scrollRight" 
              class="dashboard-view__scroll-arrow dashboard-view__scroll-arrow--right"
              aria-label="Scroll right"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="9 18 15 12 9 6"/>
              </svg>
            </button>
          </div>
        </div>
      </section>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { snacksApi } from '../api/snacks'
import { votesApi } from '../api/votes'
import { useToast } from '../composables/useToast'
import ErrorState from '../components/ErrorState.vue'
import EmptyState from '../components/EmptyState.vue'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

gsap.registerPlugin(ScrollTrigger)

const router = useRouter()
const authStore = useAuthStore()
const { success, error: toastError } = useToast()

const user = computed(() => authStore.user)

// Data
const summary = ref<any>(null)
const snacks = ref<any[]>([])
const isLoading = ref(true)
const error = ref('')
const isVoting = ref(false)
const hasVoted = ref(false)

// Animated counts
const animatedStocked = ref(0)
const animatedRunningLow = ref(0)
const animatedGone = ref(0)
const animatedTotal = ref(0)

// Computed
const runningLowSnacks = computed(() => {
  if (!snacks.value) return []
  return snacks.value.filter(s => s.quantity > 0 && s.quantity <= s.low_stock_threshold)
})

// Refs for GSAP
const dashboardRef = ref<HTMLElement>()
const garnish1Ref = ref<HTMLElement>()
const garnish2Ref = ref<HTMLElement>()
const garnish3Ref = ref<HTMLElement>()
const garnish4Ref = ref<HTMLElement>()
const garnish5Ref = ref<HTMLElement>()
const heroIllustrationRef = ref<HTMLElement>()
const summaryRef = ref<HTMLElement>()
const cardStockedRef = ref<HTMLElement>()
const cardRunningLowRef = ref<HTMLElement>()
const cardGoneRef = ref<HTMLElement>()
const cardTotalRef = ref<HTMLElement>()
const snackOfWeekRef = ref<HTMLElement>()
const sowIllustrationRef = ref<HTMLElement>()
const sowCallout1Ref = ref<HTMLElement>()
const sowCallout2Ref = ref<HTMLElement>()
const sowCallout3Ref = ref<HTMLElement>()
const runningLowRef = ref<HTMLElement>()
const scrollContainerRef = ref<HTMLElement>()

let ctx: gsap.Context | null = null
const prefersReducedMotion = ref(false)

async function fetchData() {
  isLoading.value = true
  error.value = ''
  
  try {
    const [summaryData, snacksData] = await Promise.all([
      snacksApi.summary(),
      snacksApi.list({ page_size: 50 })
    ])
    summary.value = summaryData
    snacks.value = snacksData.items || snacksData.snacks || []
    
    // Check if user voted for snack of the week
    if (summary.value?.snack_of_the_week) {
      // This would need a backend endpoint to check if user voted
      // For now, we'll set it to false
      hasVoted.value = false
    }
    
    // Refresh ScrollTrigger after data loads
    setTimeout(() => {
      ScrollTrigger.refresh()
    }, 100)
  } catch (err: any) {
    error.value = err.message || 'Failed to load pantry data'
  } finally {
    isLoading.value = false
  }
}

function animateCounts() {
  if (prefersReducedMotion.value) {
    animatedStocked.value = summary.value?.stocked || 0
    animatedRunningLow.value = summary.value?.running_low || 0
    animatedGone.value = summary.value?.gone || 0
    animatedTotal.value = summary.value?.total || 0
    return
  }

  const duration = 1.5
  const stocked = summary.value?.stocked || 0
  const runningLow = summary.value?.running_low || 0
  const gone = summary.value?.gone || 0
  const total = summary.value?.total || 0

  gsap.to(animatedStocked, { value: stocked, duration, ease: 'power2.out' })
  gsap.to(animatedRunningLow, { value: runningLow, duration, ease: 'power2.out' })
  gsap.to(animatedGone, { value: gone, duration, ease: 'power2.out' })
  gsap.to(animatedTotal, { value: total, duration, ease: 'power2.out' })
}

function setupAnimations() {
  if (!ctx) return
  
  if (prefersReducedMotion.value) return

  // Hero garnish parallax
  if (garnish1Ref.value && garnish2Ref.value && garnish3Ref.value) {
    ctx.to(garnish1Ref.value, {
      y: -50,
      scrollTrigger: {
        trigger: dashboardRef.value,
        start: 'top top',
        end: 'bottom top',
        scrub: true
      }
    })
    
    ctx.to(garnish2Ref.value, {
      y: -30,
      scrollTrigger: {
        trigger: dashboardRef.value,
        start: 'top top',
        end: 'bottom top',
        scrub: true
      }
    })
    
    ctx.to(garnish3Ref.value, {
      y: -40,
      scrollTrigger: {
        trigger: dashboardRef.value,
        start: 'top top',
        end: 'bottom top',
        scrub: true
      }
    })
  }

  // Summary cards stagger
  if (cardStockedRef.value && cardRunningLowRef.value && cardGoneRef.value && cardTotalRef.value) {
    const cards = [cardStockedRef.value, cardRunningLowRef.value, cardGoneRef.value, cardTotalRef.value]
    
    ctx.from(cards, {
      y: 30,
      opacity: 0,
      duration: 0.4,
      stagger: 0.1,
      scrollTrigger: {
        trigger: summaryRef.value,
        start: 'top 80%',
      }
    })
  }

  // Snack of the Week pin (disabled on mobile)
  const isMobile = window.innerWidth < 768
  if (!isMobile && snackOfWeekRef.value && sowIllustrationRef.value) {
    ScrollTrigger.create({
      trigger: snackOfWeekRef.value,
      start: 'top top',
      end: '+=150%',
      pin: sowIllustrationRef.value,
      scrub: true
    })
    
    // Illustration rotation/scale
    ctx.to(sowIllustrationRef.value, {
      rotation: 10,
      scale: 1.1,
      scrollTrigger: {
        trigger: snackOfWeekRef.value,
        start: 'top top',
        end: 'bottom top',
        scrub: true
      }
    })
    
    // Callout fade-ins
    if (sowCallout1Ref.value && sowCallout2Ref.value && sowCallout3Ref.value) {
      const callouts = [sowCallout1Ref.value, sowCallout2Ref.value, sowCallout3Ref.value]
      
      ctx.from(callouts, {
        opacity: 0,
        x: -30,
        duration: 0.4,
        stagger: 0.2,
        scrollTrigger: {
          trigger: snackOfWeekRef.value,
          start: 'top center',
          end: 'bottom center',
          scrub: 1
        }
      })
    }
  }

  // Running low items stagger
  if (runningLowRef.value) {
    const items = document.querySelectorAll('.dashboard-view__scroll-item')
    if (items.length > 0) {
      ctx.from(items, {
        x: 30,
        opacity: 0,
        duration: 0.3,
        stagger: 0.05,
        scrollTrigger: {
          trigger: runningLowRef.value,
          start: 'top 80%',
        }
      })
    }
  }
}

function navigateToSnacks(status?: string) {
  const query = status ? { status } : {}
  router.push({ path: '/snacks', query })
}

function navigateToSnack(id: string) {
  router.push({ path: '/snacks', query: { q: id } })
}

async function handleVote() {
  if (!summary.value?.snack_of_the_week) return
  
  isVoting.value = true
  
  try {
    if (hasVoted.value) {
      await votesApi.unvote(summary.value.snack_of_the_week.id)
      hasVoted.value = false
      success('Vote removed')
    } else {
      await votesApi.vote(summary.value.snack_of_the_week.id)
      hasVoted.value = true
      success('Vote recorded!')
    }
    
    // Refresh data
    await fetchData()
  } catch (err: any) {
    toastError(err.message || 'Failed to vote')
  } finally {
    isVoting.value = false
  }
}

function scrollLeft() {
  if (scrollContainerRef.value) {
    scrollContainerRef.value.scrollBy({ left: -300, behavior: 'smooth' })
  }
}

function scrollRight() {
  if (scrollContainerRef.value) {
    scrollContainerRef.value.scrollBy({ left: 300, behavior: 'smooth' })
  }
}

onMounted(() => {
  prefersReducedMotion.value = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  
  fetchData()
  
  // Wait for fonts to load before setting up animations
  document.fonts.ready.then(() => {
    ctx = gsap.context(() => {
      setupAnimations()
    }, dashboardRef.value)
    
    ScrollTrigger.refresh()
  })
})

onBeforeUnmount(() => {
  if (ctx) {
    ctx.revert()
  }
  ScrollTrigger.getAll().forEach(t => t.kill())
})

watch(summary, () => {
  if (summary.value) {
    animateCounts()
  }
})
</script>

<style scoped>
.dashboard-view {
  min-height: 100vh;
  width: 100%;
  max-width: 100vw;
  overflow-x: hidden;
}

/* Hero Section */
.dashboard-view__hero {
  position: relative;
  min-height: 55vh;
  background: linear-gradient(135deg, #FFFFFF 0%, #F6EFFC 100%);
  border-bottom: 1px solid #EADBFA;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.dashboard-view__hero-garnishes {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.dashboard-view__garnish {
  position: absolute;
  width: 48px;
  height: 48px;
}

.dashboard-view__garnish--1 {
  top: 20%;
  left: 15%;
}

.dashboard-view__garnish--2 {
  top: 60%;
  right: 20%;
}

.dashboard-view__garnish--3 {
  bottom: 25%;
  left: 25%;
}

.dashboard-view__garnish--4 {
  top: 30%;
  right: 30%;
  width: 24px;
  height: 24px;
}

.dashboard-view__garnish--5 {
  bottom: 40%;
  right: 40%;
  width: 20px;
  height: 20px;
}

.dashboard-view__hero-content {
  position: relative;
  z-index: 1;
  text-align: center;
  padding: var(--space-12) var(--space-6);
}

.dashboard-view__headline {
  font-size: var(--text-4xl);
  color: var(--color-tomato);
  margin-bottom: var(--space-4);
  max-width: 600px;
}

.dashboard-view__greeting {
  font-size: var(--text-xl);
  color: var(--color-muted);
  margin-bottom: var(--space-8);
}

.dashboard-view__hero-illustration {
  width: 120px;
  height: 120px;
  margin: 0 auto;
}

.dashboard-view__hero-illustration svg {
  width: 100%;
  height: 100%;
}

/* Container - Full-scale edge-to-edge on laptop */
.dashboard-view__container {
  width: 100%;
  max-width: 100%;
  margin: 0;
  padding: var(--space-6) clamp(1.25rem, 3.5vw, 3.5rem);
  box-sizing: border-box;
}

/* Summary Cards */
.dashboard-view__summary {
  padding: var(--space-12) 0;
}

.dashboard-view__cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: var(--space-6);
}

.dashboard-view__card {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-6);
  background: white;
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-md);
  cursor: pointer;
  transition: transform var(--transition-fast), box-shadow var(--transition-fast);
}

.dashboard-view__card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.dashboard-view__card--stocked {
  border-left: 4px solid var(--color-success);
}

.dashboard-view__card--running-low {
  border-left: 4px solid var(--color-warning);
}

.dashboard-view__card--gone {
  border-left: 4px solid var(--color-danger);
}

.dashboard-view__card--total {
  border-left: 4px solid var(--color-tomato);
  cursor: default;
}

.dashboard-view__card--total:hover {
  transform: none;
}

.dashboard-view__card-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-md);
  background-color: var(--color-cream);
  color: var(--color-charcoal);
}

.dashboard-view__card--stocked .dashboard-view__card-icon {
  color: var(--color-success);
}

.dashboard-view__card--running-low .dashboard-view__card-icon {
  color: var(--color-warning);
}

.dashboard-view__card--gone .dashboard-view__card-icon {
  color: var(--color-danger);
}

.dashboard-view__card-icon svg {
  width: 24px;
  height: 24px;
}

.dashboard-view__card-content {
  display: flex;
  flex-direction: column;
}

.dashboard-view__card-label {
  font-size: var(--text-sm);
  color: var(--color-muted);
  font-weight: 500;
}

.dashboard-view__card-value {
  font-size: var(--text-2xl);
  font-weight: 700;
  color: var(--color-charcoal);
}

/* Skeleton Cards */
.dashboard-view__skeleton-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: var(--space-6);
}

.dashboard-view__skeleton-card {
  height: 120px;
  background: linear-gradient(90deg, var(--color-peach) 25%, var(--color-cream) 50%, var(--color-peach) 75%);
  background-size: 200% 100%;
  border-radius: var(--radius-xl);
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* Snack of the Week */
.dashboard-view__snack-of-week {
  padding: var(--space-16) 0;
  background-color: var(--color-cream);
}

.dashboard-view__sow-content {
  display: flex;
  align-items: center;
  gap: var(--space-12);
  min-height: 50vh;
}

.dashboard-view__sow-illustration {
  flex-shrink: 0;
  width: 200px;
  height: 200px;
}

.dashboard-view__sow-illustration svg {
  width: 100%;
  height: 100%;
}

.dashboard-view__sow-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

.dashboard-view__sow-callout {
  padding: var(--space-4);
  background: white;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
}

.dashboard-view__sow-name {
  font-size: var(--text-3xl);
  color: var(--color-charcoal);
  margin-bottom: var(--space-2);
}

.dashboard-view__sow-category {
  font-size: var(--text-sm);
  text-transform: uppercase;
}

.dashboard-view__sow-stat {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.dashboard-view__sow-stat-label {
  font-size: var(--text-sm);
  color: var(--color-muted);
}

.dashboard-view__sow-stat-value {
  font-size: var(--text-2xl);
  font-weight: 700;
  color: var(--color-tomato);
}

.dashboard-view__sow-vote {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-4) var(--space-6);
  background-color: var(--color-tomato);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  font-size: var(--text-base);
  font-weight: 600;
  cursor: pointer;
  transition: background-color var(--transition-fast);
}

.dashboard-view__sow-vote:hover:not(:disabled) {
  background-color: var(--color-chili);
}

.dashboard-view__sow-vote:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.dashboard-view__sow-vote svg {
  width: 20px;
  height: 20px;
}

/* Running Low */
.dashboard-view__running-low {
  padding: var(--space-12) 0;
}

.dashboard-view__section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-6);
}

.dashboard-view__section-title {
  font-size: var(--text-2xl);
  color: var(--color-charcoal);
}

.dashboard-view__section-link {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  color: var(--color-tomato);
  text-decoration: none;
  font-weight: 500;
  transition: color var(--transition-fast);
}

.dashboard-view__section-link:hover {
  color: var(--color-chili);
}

.dashboard-view__section-link svg {
  width: 16px;
  height: 16px;
}

.dashboard-view__scroll-row {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.dashboard-view__scroll-arrow {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border: 2px solid var(--color-peach);
  border-radius: var(--radius-full);
  color: var(--color-charcoal);
  cursor: pointer;
  transition: all var(--transition-fast);
  flex-shrink: 0;
}

.dashboard-view__scroll-arrow:hover {
  background-color: var(--color-peach);
  border-color: var(--color-orange);
}

.dashboard-view__scroll-arrow svg {
  width: 20px;
  height: 20px;
}

.dashboard-view__scroll-container {
  flex: 1;
  display: flex;
  gap: var(--space-4);
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  scroll-behavior: smooth;
  -webkit-overflow-scrolling: touch;
  padding: var(--space-2);
}

.dashboard-view__scroll-container::-webkit-scrollbar {
  display: none;
}

.dashboard-view__scroll-item {
  flex-shrink: 0;
  width: 150px;
  padding: var(--space-4);
  background: white;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  cursor: pointer;
  transition: transform var(--transition-fast);
  scroll-snap-align: start;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-3);
}

.dashboard-view__scroll-item:hover {
  transform: translateY(-4px);
}

.dashboard-view__scroll-item-illustration {
  width: 80px;
  height: 80px;
}

.dashboard-view__scroll-item-illustration svg {
  width: 100%;
  height: 100%;
}

.dashboard-view__scroll-item-name {
  font-size: var(--text-sm);
  font-weight: 600;
  color: var(--color-charcoal);
  text-align: center;
}

.dashboard-view__scroll-item-quantity {
  font-size: var(--text-xs);
  color: var(--color-warning);
  font-weight: 500;
}

/* Mobile */
@media (max-width: 767px) {
  .dashboard-view__hero {
    min-height: auto;
    padding: 2.5rem 1rem 2rem;
  }

  .dashboard-view__hero-content {
    padding: 0;
  }

  .dashboard-view__headline {
    font-size: clamp(1.75rem, 6.5vw, 2.25rem);
    line-height: 1.18;
    margin-bottom: var(--space-3);
  }

  .dashboard-view__greeting {
    font-size: var(--text-base);
    margin-bottom: var(--space-5);
  }

  .dashboard-view__hero-illustration {
    width: 80px;
    height: 80px;
  }

  .dashboard-view__container {
    padding: 0 1rem;
  }

  .dashboard-view__summary {
    padding: 1.5rem 0;
  }

  .dashboard-view__cards {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.75rem;
  }

  .dashboard-view__card {
    padding: 0.85rem 0.75rem;
    gap: 0.65rem;
    flex-direction: column;
    align-items: flex-start;
    border-radius: var(--radius-lg);
  }

  .dashboard-view__card-icon {
    width: 36px;
    height: 36px;
  }

  .dashboard-view__card-icon svg {
    width: 18px;
    height: 18px;
  }

  .dashboard-view__card-label {
    font-size: 0.75rem;
  }

  .dashboard-view__card-value {
    font-size: 1.35rem;
  }

  .dashboard-view__skeleton-cards {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.75rem;
  }

  .dashboard-view__skeleton-card {
    height: 95px;
  }

  .dashboard-view__snack-of-week {
    padding: 2rem 0;
  }

  .dashboard-view__sow-content {
    min-height: auto;
    flex-direction: column;
    text-align: center;
    gap: 1.25rem;
  }

  .dashboard-view__sow-illustration {
    width: 120px;
    height: 120px;
    margin: 0 auto;
  }

  .dashboard-view__sow-info {
    width: 100%;
    gap: var(--space-3);
  }

  .dashboard-view__sow-callout {
    padding: 0.85rem 1rem;
  }

  .dashboard-view__sow-name {
    font-size: 1.5rem;
  }

  .dashboard-view__sow-stat {
    justify-content: center;
  }

  .dashboard-view__sow-vote {
    width: 100%;
    justify-content: center;
    height: 46px;
    border-radius: var(--radius-full);
  }

  .dashboard-view__running-low {
    padding: 1.75rem 0;
  }

  .dashboard-view__section-header {
    margin-bottom: var(--space-4);
  }

  .dashboard-view__section-title {
    font-size: var(--text-xl);
  }

  .dashboard-view__scroll-arrow {
    display: none;
  }

  .dashboard-view__scroll-container {
    padding: 0.35rem 0.25rem 0.75rem;
    gap: 0.75rem;
  }

  .dashboard-view__scroll-item {
    width: 125px;
    padding: 0.85rem 0.5rem;
    gap: 0.5rem;
  }

  .dashboard-view__scroll-item-illustration {
    width: 55px;
    height: 55px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .dashboard-view__skeleton-card {
    animation: none;
    background-color: var(--color-peach);
  }
  
  .dashboard-view__card:hover {
    transform: none;
  }
  
  .dashboard-view__scroll-item:hover {
    transform: none;
  }
}
</style>
