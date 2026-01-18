export interface User {
  id: number;
  username: string;
  email: string;
  first_name?: string;
  last_name?: string;
  profile?: UserProfile;
}

export interface UserProfile {
  bio?: string;
  avatar?: string;
  total_documents_uploaded: number;
  total_conversations: number;
  total_messages: number;
  default_llm_model: string;
  default_temperature: number;
  default_max_tokens: number;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  first_name?: string;
  last_name?: string;
}

export interface AuthResponse {
  token: string;
}