// ============================================
// src/app/core/services/chat.service.ts
// ============================================
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';
import { Conversation, Message, SendMessageRequest, SendMessageResponse } from '../models/chat.model';

interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  constructor(private api: ApiService) {}

  getConversations(collectionId?: string): Observable<PaginatedResponse<Conversation>> {
    const url = collectionId 
      ? `/conversations/?collection=${collectionId}` 
      : '/conversations/';
    return this.api.get<PaginatedResponse<Conversation>>(url);
  }

  getConversation(id: string): Observable<Conversation> {
    return this.api.get<Conversation>(`/conversations/${id}/`);
  }

  createConversation(data: Partial<Conversation>): Observable<Conversation> {
    return this.api.post<Conversation>('/conversations/', data);
  }

  deleteConversation(id: string): Observable<void> {
    return this.api.delete<void>(`/conversations/${id}/`);
  }

  sendMessage(conversationId: string, message: string): Observable<SendMessageResponse> {
    const data: SendMessageRequest = { message };
    return this.api.post<SendMessageResponse>(
      `/conversations/${conversationId}/send_message/`,
      data
    );
  }

  getHistory(conversationId: string): Observable<{ history: Message[] }> {
    return this.api.get<{ history: Message[] }>(
      `/conversations/${conversationId}/history/`
    );
  }

  archiveConversation(id: string): Observable<any> {
    return this.api.post(`/conversations/${id}/archive/`, {});
  }

  getStatistics(): Observable<any> {
    return this.api.get('/conversations/statistics/');
  }
}