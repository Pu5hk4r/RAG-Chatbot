// ============================================
// src/app/core/models/chat.model.ts
// ============================================
export interface Conversation {
  id: string;
  collection: string;
  collection_name: string;
  title: string;
  llm_model: string;
  temperature: number;
  max_tokens: number;
  top_k: number;
  created_at: string;
  updated_at: string;
  is_archived: boolean;
  messages: Message[];
  message_count: number;
}

export interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  created_at: string;
  tokens_used?: number;
  processing_time?: number;
  sources?: SourceReference[];
}

export interface SourceReference {
  id: string;
  document_name: string;
  chunk_content: string;
  page_number: number;
  relevance_score: number;
}

export interface SendMessageRequest {
  message: string;
}

export interface SendMessageResponse {
  response: string;
  sources: SourceReference[];
  message_id: string;
}