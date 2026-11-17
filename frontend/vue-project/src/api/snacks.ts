import { api } from './client';
import type {
  Snack,
  CreateSnackRequest,
  UpdateSnackRequest,
  ConsumeRequest,
  RestockRequest,
  SnackListParams,
  SnackListResponse,
  SnackSummary,
} from './types';

export const snacksApi = {
  list: async (params?: SnackListParams, options?: { signal?: AbortSignal }) => {
    const queryParams = new URLSearchParams();
    if (params?.page) queryParams.append('page', params.page.toString());
    if (params?.page_size) queryParams.append('page_size', params.page_size.toString());
    if (params?.category) queryParams.append('category', params.category);
    if (params?.status) queryParams.append('status', params.status);
    if (params?.q) queryParams.append('q', params.q);
    else if (params?.search) queryParams.append('q', params.search);
    if (params?.sort_by) queryParams.append('sort_by', params.sort_by);
    if (params?.order) queryParams.append('order', params.order);
    const queryString = queryParams.toString();
    const data = await api.get<SnackListResponse>(`/snacks${queryString ? `?${queryString}` : ''}`, options);
    // Ensure backwards compatibility with older components expecting .snacks
    if (data && data.items && !data.snacks) {
      data.snacks = data.items;
    }
    return data;
  },
  create: (data: CreateSnackRequest) => api.post<Snack>('/snacks', data),
  get: (id: string, options?: { signal?: AbortSignal }) => api.get<Snack>(`/snacks/${id}`, options),
  update: (id: string, data: UpdateSnackRequest) => api.patch<Snack>(`/snacks/${id}`, data),
  delete: (id: string) => api.delete<void>(`/snacks/${id}`),
  consume: (id: string, data: ConsumeRequest) => api.post<Snack>(`/snacks/${id}/consume`, data),
  restock: (id: string, data: RestockRequest) => api.post<Snack>(`/snacks/${id}/restock`, data),
  summary: () => api.get<SnackSummary>('/snacks/summary'),
};
