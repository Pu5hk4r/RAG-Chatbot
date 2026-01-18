export interface DocumentCollection {
  id: string;
  name: string;
  description?: string;
  is_public: boolean;
  created_at: string;
  updated_at: string;
  documents: Document[];
  document_count: number;
  total_pages: number;
  has_vectordb: boolean;
}

export interface Document {
  id: string;
  collection: string;
  filename: string;
  file_size: number;
  page_count?: number;
  status: 'uploading' | 'processing' | 'ready' | 'failed';
  error_message?: string;
  uploaded_at: string;
  processed_at?: string;
  chunk_count: number;
}

export interface CollectionStatistics {
  total_documents: number;
  ready_documents: number;
  processing_documents: number;
  failed_documents: number;
  total_conversations: number;
  total_pages: number;
}

