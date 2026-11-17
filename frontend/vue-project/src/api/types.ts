// Backend response types matching the API schemas

export interface User {
  id: string;
  name: string;
  email: string;
  role: 'ADMIN' | 'MEMBER';
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: 'bearer';
  user: User;
}

export type SnackCategoryType = 'sweet' | 'savoury' | 'drink' | 'healthy-ish';
export type SnackStatus = 'stocked' | 'running_low' | 'gone';

export interface SnackCategory {
  SWEET: 'sweet';
  SAVOURY: 'savoury';
  DRINK: 'drink';
  HEALTHYISH: 'healthy-ish';
}

export interface Snack {
  id: string;
  name: string;
  category: SnackCategoryType;
  quantity: number;
  low_stock_threshold: number;
  status: SnackStatus;
  vote_count: number;
  voted_by_me: boolean;
  created_at: string;
  updated_at: string;
}

export interface CreateSnackRequest {
  name: string;
  category: SnackCategoryType;
  quantity: number;
  low_stock_threshold?: number;
}

export interface UpdateSnackRequest {
  name?: string;
  category?: SnackCategoryType;
  low_stock_threshold?: number;
}

export interface ConsumeRequest {
  amount: number;
}

export interface RestockRequest {
  amount: number;
}

export interface Activity {
  id: string;
  user_id: string | null;
  snack_id: string | null;
  snack_name: string;
  action: 'RESTOCKED' | 'CONSUMED';
  amount: number;
  created_at: string;
}

export interface Vote {
  id: string;
  user_id: string;
  snack_id: string;
  created_at: string;
}

export interface VoteResponse {
  vote_count: number;
  voted_by_me: boolean;
}

export interface SnackListParams {
  category?: string;
  status?: string;
  q?: string;
  search?: string;
  page?: number;
  page_size?: number;
  sort_by?: 'name' | 'quantity' | 'votes' | 'created_at';
  order?: 'asc' | 'desc';
  sort?: string;
}

export interface SnackListResponse {
  items: Snack[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
  snacks?: Snack[];
}

export interface SnackSummary {
  total: number;
  stocked: number;
  running_low: number;
  gone: number;
  snack_of_the_week: {
    id: string;
    name: string;
    category: string;
    vote_count: number;
  };
}

export interface ErrorResponse {
  error: {
    code: string;
    message: string;
    details?: any;
  };
}

export type ErrorCode =
  | 'INVALID_CREDENTIALS'
  | 'UNAUTHENTICATED'
  | 'FORBIDDEN'
  | 'NOT_FOUND'
  | 'VALIDATION_ERROR'
  | 'INSUFFICIENT_STOCK'
  | 'ALREADY_VOTED'
  | 'VOTE_NOT_FOUND'
  | 'SNACK_NOT_FOUND'
  | 'SNACK_NAME_TAKEN'
  | 'DUPLICATE_NAME'
  | 'NETWORK_ERROR';
