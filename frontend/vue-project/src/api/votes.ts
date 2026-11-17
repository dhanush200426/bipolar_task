import { api } from './client';
import type { VoteResponse } from './types';

export const votesApi = {
  vote: (snackId: string) => api.post<VoteResponse>(`/snacks/${snackId}/vote`, {}),
  unvote: (snackId: string) => api.delete<VoteResponse>(`/snacks/${snackId}/vote`),
};
