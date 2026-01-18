export interface SignupResponse {
  success: boolean;
  message: string;
  user_id: number;
  email: string;
}

export interface SigninResponse {
  success: boolean;
  message: string;
  user_id: number;
  email: string;
  similarity_score?: number;
}

export interface ErrorResponse {
  detail: string;
}
