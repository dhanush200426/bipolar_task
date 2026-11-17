import type { ErrorCode } from '../api/types';

export const getErrorMessage = (code: ErrorCode, fallbackMessage?: string): string => {
  const messages: Record<ErrorCode, string> = {
    INVALID_CREDENTIALS: 'Invalid email or password.',
    UNAUTHENTICATED: 'You need to log in to do that.',
    FORBIDDEN: 'You don\'t have permission to do that.',
    NOT_FOUND: 'We couldn\'t find what you\'re looking for.',
    VALIDATION_ERROR: 'Please check your input and try again.',
    INSUFFICIENT_STOCK: 'Someone beat you to the last packet!',
    ALREADY_VOTED: 'You\'ve already voted for this one.',
    VOTE_NOT_FOUND: 'Vote not found.',
    SNACK_NOT_FOUND: 'Snack not found.',
    SNACK_NAME_TAKEN: 'A snack with this name already exists.',
    DUPLICATE_NAME: 'A snack with this name already exists.',
    NETWORK_ERROR: 'We can\'t reach the pantry server. Check your connection and try again.',
  };

  return messages[code] || fallbackMessage || 'Something went wrong. Please try again.';
};
