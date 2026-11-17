<template>
  <article
    :id="`snack-card-${snack.id}`"
    class="snack-card"
    :class="{
      'snack-card--running-low': snack.status === 'running_low',
      'snack-card--gone': snack.status === 'gone',
      'snack-card--shake': isShaking,
    }"
    tabindex="0"
    :aria-label="`${snack.name}, category ${snack.category}, ${snack.quantity} in stock, status ${snack.status}`"
  >
    <!-- Running Low Ribbon Badge -->
    <div v-if="snack.status === 'running_low'" class="snack-card__ribbon" aria-hidden="true">
      Low stock
    </div>

    <!-- Card Header / Illustration -->
    <div class="snack-card__media">
      <div class="snack-card__illustration-wrap">
        <SnackIllustration :category="snack.category" />
      </div>
      <!-- Category Chip -->
      <span class="snack-card__category-chip" :class="`snack-card__category-chip--${snack.category}`">
        {{ formatCategory(snack.category) }}
      </span>
    </div>

    <!-- Card Body -->
    <div class="snack-card__body">
      <div class="snack-card__headline">
        <h3 class="snack-card__title" :title="snack.name">{{ snack.name }}</h3>

        <!-- Vote Button -->
        <button
          type="button"
          class="snack-card__vote-btn"
          :class="{
            'snack-card__vote-btn--voted': snack.voted_by_me,
            'snack-card__vote-btn--pop': isVotePopping,
          }"
          :disabled="isVoting"
          :aria-label="snack.voted_by_me ? `Remove vote for ${snack.name}` : `Vote for ${snack.name}`"
          :title="snack.voted_by_me ? 'You voted for this! Click to remove vote' : 'Vote for this snack'"
          @click="handleVoteToggle"
        >
          <svg
            class="snack-card__vote-icon"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            aria-hidden="true"
          >
            <path
              d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"
            />
          </svg>
          <span class="snack-card__vote-count">{{ snack.vote_count }}</span>
        </button>
      </div>

      <!-- Quantity & Status Row -->
      <div class="snack-card__meta-row">
        <!-- Stock Quantity -->
        <div class="snack-card__stock-info">
          <span class="snack-card__quantity-num" :class="quantityAnimClass">{{ displayQuantity }}</span>
          <span class="snack-card__quantity-label">
            {{ snack.quantity === 1 ? 'packet left' : snack.quantity === 0 ? 'in stock' : 'in stock' }}
          </span>
        </div>

        <!-- Status Badge -->
        <div
          class="snack-card__status-badge"
          :class="`snack-card__status-badge--${snack.status}`"
        >
          <!-- Stocked: Check icon -->
          <svg
            v-if="snack.status === 'stocked'"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2.5"
            stroke-linecap="round"
            stroke-linejoin="round"
            class="snack-card__status-icon"
            aria-hidden="true"
          >
            <polyline points="20 6 9 17 4 12" />
          </svg>
          <!-- Running low: Alert triangle -->
          <svg
            v-else-if="snack.status === 'running_low'"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2.5"
            stroke-linecap="round"
            stroke-linejoin="round"
            class="snack-card__status-icon"
            aria-hidden="true"
          >
            <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
            <line x1="12" y1="9" x2="12" y2="13" />
            <line x1="12" y1="17" x2="12.01" y2="17" />
          </svg>
          <!-- Gone: Circle slash -->
          <svg
            v-else
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2.5"
            stroke-linecap="round"
            stroke-linejoin="round"
            class="snack-card__status-icon"
            aria-hidden="true"
          >
            <circle cx="12" cy="12" r="10" />
            <line x1="4.93" y1="4.93" x2="19.07" y2="19.07" />
          </svg>
          <span>{{ formatStatus(snack.status) }}</span>
        </div>
      </div>
    </div>

    <!-- Card Action / Consume Controls -->
    <div class="snack-card__actions">
      <!-- Stepper: 1 to min(quantity, 10) -->
      <div class="snack-card__stepper" :class="{ 'snack-card__stepper--disabled': isGone || isConsuming }">
        <button
          type="button"
          class="snack-card__stepper-btn"
          :disabled="isGone || isConsuming || consumeAmount <= 1"
          aria-label="Decrease consume amount"
          title="Decrease amount"
          @click="decrementAmount"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
            <line x1="5" y1="12" x2="19" y2="12" />
          </svg>
        </button>
        <span class="snack-card__stepper-value" aria-live="polite" :aria-label="`Consume quantity: ${consumeAmount}`">
          {{ isGone ? 0 : consumeAmount }}
        </span>
        <button
          type="button"
          class="snack-card__stepper-btn"
          :disabled="isGone || isConsuming || consumeAmount >= maxConsume"
          aria-label="Increase consume amount"
          title="Increase amount"
          @click="incrementAmount"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
            <line x1="12" y1="5" x2="12" y2="19" />
            <line x1="5" y1="12" x2="19" y2="12" />
          </svg>
        </button>
      </div>

      <!-- Consume Button with micro-interaction states -->
      <button
        type="button"
        class="snack-card__consume-btn"
        :class="{
          'snack-card__consume-btn--consuming': isConsuming,
          'snack-card__consume-btn--success': isConsumeSuccess,
          'snack-card__consume-btn--disabled': isGone,
        }"
        :disabled="isGone || isConsuming"
        :title="isGone ? 'Out of stock' : `Consume ${consumeAmount} of ${snack.name}`"
        :aria-label="isGone ? 'Out of stock' : `Consume ${consumeAmount} of ${snack.name}`"
        @click="handleConsume"
      >
        <!-- Success State: Morph Checkmark -->
        <span v-if="isConsumeSuccess" class="snack-card__consume-success-content">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" class="snack-card__btn-icon">
            <polyline points="20 6 9 17 4 12" />
          </svg>
          Enjoy!
        </span>

        <!-- Loading State: Spinner -->
        <span v-else-if="isConsuming" class="snack-card__consume-loading-content">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="snack-card__spinner">
            <circle cx="12" cy="12" r="10" stroke-opacity="0.25" />
            <path d="M12 2a10 10 0 0 1 10 10" />
          </svg>
          Grabbing...
        </span>

        <!-- Gone State -->
        <span v-else-if="isGone" class="snack-card__consume-idle-content">
          Out of stock
        </span>

        <!-- Normal Idle State -->
        <span v-else class="snack-card__consume-idle-content">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="snack-card__btn-icon">
            <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z" />
            <line x1="3" y1="6" x2="21" y2="6" />
            <path d="M16 10a4 4 0 0 1-8 0" />
          </svg>
          Consume
        </span>
      </button>
    </div>
  </article>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import type { Snack, SnackCategoryType, SnackStatus } from '../api/types';
import SnackIllustration from './SnackIllustration.vue';
import { snacksApi } from '../api/snacks';
import { votesApi } from '../api/votes';
import { useToast } from '../composables/useToast';

const props = defineProps<{
  snack: Snack;
}>();

const emit = defineEmits<{
  (e: 'update:snack', updated: Snack): void;
  (e: 'consumed', snack: Snack, amount: number): void;
  (e: 'voted', snack: Snack): void;
}>();

const { success: toastSuccess, error: toastError, warning: toastWarning } = useToast();

// Local UI states
const consumeAmount = ref(1);
const isConsuming = ref(false);
const isConsumeSuccess = ref(false);
const isVoting = ref(false);
const isVotePopping = ref(false);
const isShaking = ref(false);
const quantityAnimClass = ref('');

// Computed
const isGone = computed(() => props.snack.quantity <= 0 || props.snack.status === 'gone');
const maxConsume = computed(() => Math.max(1, Math.min(props.snack.quantity, 10)));
const displayQuantity = computed(() => props.snack.quantity);

// Adjust stepper if max changes or snack is gone
watch(
  () => props.snack.quantity,
  (newQty, oldQty) => {
    if (newQty <= 0) {
      consumeAmount.value = 1;
    } else if (consumeAmount.value > maxConsume.value) {
      consumeAmount.value = maxConsume.value;
    }

    if (oldQty !== undefined && newQty < oldQty) {
      quantityAnimClass.value = 'snack-card__quantity-num--tick';
      setTimeout(() => {
        quantityAnimClass.value = '';
      }, 500);
    }
  }
);

function decrementAmount() {
  if (consumeAmount.value > 1) {
    consumeAmount.value--;
  }
}

function incrementAmount() {
  if (consumeAmount.value < maxConsume.value) {
    consumeAmount.value++;
  }
}

function formatCategory(category: SnackCategoryType | string): string {
  switch (category) {
    case 'sweet':
      return 'Sweet';
    case 'savoury':
      return 'Savoury';
    case 'drink':
      return 'Drink';
    case 'healthy-ish':
      return 'Healthy-ish';
    default:
      return category;
  }
}

function formatStatus(status: SnackStatus | string): string {
  switch (status) {
    case 'stocked':
      return 'Stocked';
    case 'running_low':
      return 'Running low';
    case 'gone':
      return 'Gone';
    default:
      return status;
  }
}

function triggerShake() {
  isShaking.value = true;
  setTimeout(() => {
    isShaking.value = false;
  }, 600);
}

// ---------------------------------------------------------------------------
// CONSUME ACTION
// ---------------------------------------------------------------------------
async function handleConsume() {
  if (isGone.value || isConsuming.value) return;

  isConsuming.value = true;
  const amountToConsume = consumeAmount.value;

  try {
    const updatedSnack = await snacksApi.consume(props.snack.id, { amount: amountToConsume });

    // Success micro-interaction
    isConsumeSuccess.value = true;
    toastSuccess(`Consumed ${amountToConsume} ${props.snack.name}! Enjoy your snack.`);

    // Emit updated snack with fresh quantity/status
    emit('update:snack', updatedSnack);
    emit('consumed', updatedSnack, amountToConsume);

    // Keep checkmark morph for 1.2s
    setTimeout(() => {
      isConsumeSuccess.value = false;
    }, 1200);
  } catch (err: any) {
    // Check if error is 409 INSUFFICIENT_STOCK
    if (err?.code === 'INSUFFICIENT_STOCK' || err?.status === 409) {
      toastWarning('Someone beat you to the last packet!');
      triggerShake();

      // REFRESH this card with the server's current data
      try {
        const freshSnack = await snacksApi.get(props.snack.id);
        emit('update:snack', freshSnack);
      } catch {
        // If 404 or server unreachable, mark as gone locally
        const goneSnack: Snack = {
          ...props.snack,
          quantity: 0,
          status: 'gone',
        };
        emit('update:snack', goneSnack);
      }
    } else {
      toastError(err?.message || 'Could not consume snack. Please try again.');
    }
  } finally {
    isConsuming.value = false;
  }
}

// ---------------------------------------------------------------------------
// VOTE ACTION
// ---------------------------------------------------------------------------
async function handleVoteToggle() {
  if (isVoting.value) return;

  isVoting.value = true;
  isVotePopping.value = true;
  setTimeout(() => {
    isVotePopping.value = false;
  }, 450);

  const wasVoted = props.snack.voted_by_me;

  try {
    if (wasVoted) {
      // Unvote
      const res = await votesApi.unvote(props.snack.id);
      const updated: Snack = {
        ...props.snack,
        vote_count: res.vote_count,
        voted_by_me: res.voted_by_me,
      };
      emit('update:snack', updated);
      emit('voted', updated);
    } else {
      // Vote
      const res = await votesApi.vote(props.snack.id);
      const updated: Snack = {
        ...props.snack,
        vote_count: res.vote_count,
        voted_by_me: res.voted_by_me,
      };
      emit('update:snack', updated);
      emit('voted', updated);
    }
  } catch (err: any) {
    // Concurrency / Out-of-sync error handling
    if (err?.code === 'ALREADY_VOTED' || err?.code === 'VOTE_NOT_FOUND') {
      try {
        const freshSnack = await snacksApi.get(props.snack.id);
        emit('update:snack', freshSnack);
        toastWarning(
          err.code === 'ALREADY_VOTED'
            ? 'Your vote was already registered on the server.'
            : 'Vote was already cleared on the server.'
        );
      } catch {
        toastError('Failed to synchronize vote with server.');
      }
    } else {
      toastError(err?.message || 'Could not update vote. Please try again.');
    }
  } finally {
    isVoting.value = false;
  }
}
</script>

<style scoped>
.snack-card {
  position: relative;
  display: flex;
  flex-direction: column;
  background-color: #ffffff;
  border-radius: var(--radius-xl);
  border: 1.5px solid rgba(31, 27, 24, 0.08);
  box-shadow: var(--shadow-sm);
  padding: var(--space-5);
  transition: transform var(--transition-base), box-shadow var(--transition-base), border-color var(--transition-base), opacity var(--transition-base), filter var(--transition-base);
  overflow: hidden;
}

.snack-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
  border-color: rgba(228, 71, 43, 0.25);
}

.snack-card:focus-visible {
  outline: 2px solid var(--color-tomato);
  outline-offset: 2px;
}

/* Running Low Accent */
.snack-card--running-low {
  border: 2px solid var(--color-warning);
  box-shadow: 0 4px 12px rgba(245, 124, 0, 0.15);
}

.snack-card__ribbon {
  position: absolute;
  top: 14px;
  right: -32px;
  transform: rotate(45deg);
  background-color: var(--color-warning);
  color: #ffffff;
  font-size: var(--text-xs);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 3px 36px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
  z-index: 5;
  pointer-events: none;
}

/* Gone Muted State */
.snack-card--gone {
  opacity: 0.72;
  filter: grayscale(0.4);
  background-color: #faf8f5;
  border-color: rgba(31, 27, 24, 0.12);
}

.snack-card--gone:hover {
  transform: none;
  box-shadow: var(--shadow-sm);
}

/* Card Shake Animation */
.snack-card--shake {
  animation: cardShake 0.55s ease-in-out;
}

@keyframes cardShake {
  0%, 100% { transform: translateX(0); }
  15%, 45%, 75% { transform: translateX(-7px); }
  30%, 60%, 90% { transform: translateX(7px); }
}

/* Media / Illustration area */
.snack-card__media {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--color-cream);
  border-radius: var(--radius-lg);
  height: 140px;
  margin-bottom: var(--space-4);
  overflow: hidden;
}

.snack-card__illustration-wrap {
  width: 90px;
  height: 90px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Category Chip */
.snack-card__category-chip {
  position: absolute;
  bottom: var(--space-2);
  left: var(--space-2);
  font-size: var(--text-xs);
  font-weight: 600;
  padding: 2px 10px;
  border-radius: var(--radius-full);
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(4px);
  color: var(--color-charcoal);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.snack-card__category-chip--sweet {
  color: #B25E00;
  border-left: 3px solid var(--color-golden);
}

.snack-card__category-chip--savoury {
  color: var(--color-chili);
  border-left: 3px solid var(--color-orange);
}

.snack-card__category-chip--drink {
  color: #8C2412;
  border-left: 3px solid var(--color-tomato);
}

.snack-card__category-chip--healthy-ish {
  color: #196944;
  border-left: 3px solid var(--color-success);
}

/* Body */
.snack-card__body {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.snack-card__headline {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-2);
  margin-bottom: var(--space-3);
}

.snack-card__title {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: 700;
  color: var(--color-charcoal);
  line-height: 1.25;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Vote Button */
.snack-card__vote-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: var(--color-cream);
  border: 1px solid rgba(31, 27, 24, 0.1);
  border-radius: var(--radius-full);
  padding: 4px 10px;
  color: var(--color-muted);
  cursor: pointer;
  transition: all var(--transition-fast);
  flex-shrink: 0;
  min-height: 32px;
}

.snack-card__vote-btn:hover:not(:disabled) {
  background: var(--color-peach);
  color: var(--color-tomato);
  border-color: rgba(228, 71, 43, 0.3);
}

.snack-card__vote-btn--voted {
  background: #FFE8E5;
  color: var(--color-tomato);
  border-color: rgba(228, 71, 43, 0.4);
}

.snack-card__vote-btn--voted .snack-card__vote-icon {
  fill: var(--color-tomato);
  stroke: var(--color-chili);
}

.snack-card__vote-icon {
  width: 16px;
  height: 16px;
  transition: transform var(--transition-fast);
}

.snack-card__vote-count {
  font-size: var(--text-xs);
  font-weight: 700;
}

.snack-card__vote-btn--pop .snack-card__vote-icon {
  animation: votePop 0.45s ease-out;
}

@keyframes votePop {
  0% { transform: scale(1); }
  50% { transform: scale(1.45); }
  100% { transform: scale(1); }
}

/* Meta Row (Stock + Status) */
.snack-card__meta-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: auto;
  padding-bottom: var(--space-4);
  border-bottom: 1px dashed rgba(31, 27, 24, 0.12);
}

.snack-card__stock-info {
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.snack-card__quantity-num {
  font-size: var(--text-xl);
  font-weight: 800;
  color: var(--color-charcoal);
  font-feature-settings: 'tnum';
  transition: transform 0.2s ease;
}

.snack-card__quantity-num--tick {
  animation: numberTick 0.4s ease-out;
  color: var(--color-tomato);
}

@keyframes numberTick {
  0% { transform: translateY(-4px) scale(1.15); }
  100% { transform: translateY(0) scale(1); }
}

.snack-card__quantity-label {
  font-size: var(--text-xs);
  color: var(--color-muted);
}

/* Status Badge */
.snack-card__status-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: var(--text-xs);
  font-weight: 700;
  padding: 3px 8px;
  border-radius: var(--radius-sm);
  letter-spacing: 0.02em;
}

.snack-card__status-icon {
  width: 13px;
  height: 13px;
}

/* Stocked Badge */
.snack-card__status-badge--stocked {
  background-color: rgba(46, 158, 107, 0.12);
  color: var(--color-stocked);
}

/* Running Low Badge with Pulse */
.snack-card__status-badge--running_low {
  background-color: rgba(245, 124, 0, 0.15);
  color: var(--color-running-low);
  animation: pulseBadge 2s infinite ease-in-out;
}

@keyframes pulseBadge {
  0%, 100% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(245, 124, 0, 0.4);
  }
  50% {
    transform: scale(1.05);
    box-shadow: 0 0 0 4px rgba(245, 124, 0, 0);
  }
}

/* Gone Badge */
.snack-card__status-badge--gone {
  background-color: rgba(107, 98, 91, 0.14);
  color: var(--color-muted);
}

/* Actions Row (Stepper + Consume) */
.snack-card__actions {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin-top: var(--space-4);
}

/* Stepper */
.snack-card__stepper {
  display: inline-flex;
  align-items: center;
  background-color: var(--color-cream);
  border: 1px solid rgba(31, 27, 24, 0.12);
  border-radius: var(--radius-md);
  padding: 2px;
  height: 42px;
}

.snack-card__stepper--disabled {
  opacity: 0.5;
  pointer-events: none;
}

.snack-card__stepper-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 36px;
  background: transparent;
  border: none;
  border-radius: var(--radius-sm);
  color: var(--color-charcoal);
  cursor: pointer;
  transition: background-color var(--transition-fast);
}

.snack-card__stepper-btn:hover:not(:disabled) {
  background-color: rgba(31, 27, 24, 0.08);
}

.snack-card__stepper-btn:disabled {
  opacity: 0.35;
  cursor: not-allowed;
}

.snack-card__stepper-btn svg {
  width: 14px;
  height: 14px;
}

.snack-card__stepper-value {
  display: inline-block;
  min-width: 28px;
  text-align: center;
  font-size: var(--text-sm);
  font-weight: 700;
  font-feature-settings: 'tnum';
  color: var(--color-charcoal);
}

/* Consume Button */
.snack-card__consume-btn {
  flex: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 42px;
  padding: 0 var(--space-4);
  background-color: var(--color-tomato);
  color: #ffffff;
  border: none;
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(228, 71, 43, 0.25);
  transition: transform var(--transition-fast), background-color var(--transition-fast), box-shadow var(--transition-fast);
  user-select: none;
}

.snack-card__consume-btn:hover:not(:disabled) {
  background-color: var(--color-chili);
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(228, 71, 43, 0.35);
}

.snack-card__consume-btn:active:not(:disabled) {
  transform: scale(0.95);
  box-shadow: 0 1px 2px rgba(228, 71, 43, 0.2);
}

.snack-card__consume-btn--consuming {
  background-color: var(--color-orange);
  cursor: wait;
}

.snack-card__consume-btn--success {
  background-color: var(--color-success) !important;
  box-shadow: 0 2px 6px rgba(46, 158, 107, 0.35) !important;
  animation: buttonBounce 0.4s ease-out;
}

@keyframes buttonBounce {
  0% { transform: scale(0.95); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

.snack-card__consume-btn--disabled {
  background-color: #E2DDD9;
  color: var(--color-muted);
  box-shadow: none;
  cursor: not-allowed;
}

.snack-card__btn-icon {
  width: 16px;
  height: 16px;
  margin-right: 6px;
}

.snack-card__consume-idle-content,
.snack-card__consume-loading-content,
.snack-card__consume-success-content {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.snack-card__spinner {
  width: 16px;
  height: 16px;
  margin-right: 6px;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  100% { transform: rotate(360deg); }
}

@media (prefers-reduced-motion: reduce) {
  .snack-card:hover {
    transform: none;
  }
  .snack-card--running-low .snack-card__status-badge--running_low {
    animation: none;
  }
  .snack-card--shake {
    animation: none;
  }
  .snack-card__vote-btn--pop .snack-card__vote-icon {
    animation: none;
  }
  .snack-card__consume-btn--success {
    animation: none;
  }
}
</style>
