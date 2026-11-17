import type { ErrorResponse, ErrorCode } from './types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export class ApiError extends Error {
  code: ErrorCode;
  details?: any;

  constructor(code: ErrorCode, message: string, details?: any) {
    super(message);
    this.name = 'ApiError';
    this.code = code;
    this.details = details;
  }
}

let authToken: string | null = null;

export function setAuthToken(token: string | null) {
  authToken = token;
}

export function getAuthToken(): string | null {
  return authToken;
}

export function clearAuthToken() {
  authToken = null;
}

async function handleResponse(response: Response): Promise<any> {
  if (response.status === 204) {
    return null;
  }

  const contentType = response.headers.get('content-type');
  
  if (!contentType || !contentType.includes('application/json')) {
    throw new ApiError('NETWORK_ERROR', 'Invalid response from server');
  }

  const data = await response.json();

  if (!response.ok) {
    const errorData = data as ErrorResponse;
    throw new ApiError(
      errorData.error.code as ErrorCode,
      errorData.error.message,
      errorData.error.details
    );
  }

  return data;
}

export async function request<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string> || {}),
  };

  if (authToken) {
    headers['Authorization'] = `Bearer ${authToken}`;
  }

  try {
    const response = await fetch(url, {
      ...options,
      headers,
    });

    // Handle 401 - clear auth and redirect to login
    if (response.status === 401) {
      clearAuthToken();
      if (typeof window !== 'undefined') {
        window.location.href = '/login?session=expired';
      }
      throw new ApiError('UNAUTHENTICATED', 'Session expired. Please log in again.');
    }

    return await handleResponse(response);
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    if ((error as any)?.name === 'AbortError') {
      throw error;
    }

    // Network errors (backend down, timeout, etc.)
    throw new ApiError(
      'NETWORK_ERROR',
      'We can\'t reach the pantry server. Check your connection and try again.'
    );
  }
}

export const api = {
  get: <T>(endpoint: string, options?: RequestInit) => request<T>(endpoint, { method: 'GET', ...options }),
  post: <T>(endpoint: string, body: any, options?: RequestInit) =>
    request<T>(endpoint, { method: 'POST', body: JSON.stringify(body), ...options }),
  patch: <T>(endpoint: string, body: any, options?: RequestInit) =>
    request<T>(endpoint, { method: 'PATCH', body: JSON.stringify(body), ...options }),
  delete: <T>(endpoint: string, options?: RequestInit) => request<T>(endpoint, { method: 'DELETE', ...options }),
};
