

// ============================================
// src/app/core/services/document.service.ts
// ============================================
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';
import { DocumentCollection, Document, CollectionStatistics } from '../models/document.model';

interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

@Injectable({
  providedIn: 'root'
})
export class DocumentService {
  constructor(private api: ApiService) {}

  // Collections
  getCollections(): Observable<PaginatedResponse<DocumentCollection>> {
    return this.api.get<PaginatedResponse<DocumentCollection>>('/collections/');
  }

  getCollection(id: string): Observable<DocumentCollection> {
    return this.api.get<DocumentCollection>(`/collections/${id}/`);
  }

  createCollection(data: Partial<DocumentCollection>): Observable<DocumentCollection> {
    return this.api.post<DocumentCollection>('/collections/', data);
  }

  updateCollection(id: string, data: Partial<DocumentCollection>): Observable<DocumentCollection> {
    return this.api.put<DocumentCollection>(`/collections/${id}/`, data);
  }

  deleteCollection(id: string): Observable<void> {
    return this.api.delete<void>(`/collections/${id}/`);
  }

  createVectorDB(id: string): Observable<any> {
    return this.api.post(`/collections/${id}/create_vectordb/`, {});
  }

  getCollectionStatistics(id: string): Observable<CollectionStatistics> {
    return this.api.get<CollectionStatistics>(`/collections/${id}/statistics/`);
  }

  // Documents
  uploadDocument(collectionId: string, file: File): Observable<Document> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('collection', collectionId);
    return this.api.upload<Document>('/documents/', formData);
  }

  getDocuments(collectionId?: string): Observable<PaginatedResponse<Document>> {
    const url = collectionId 
      ? `/documents/?collection=${collectionId}` 
      : '/documents/';
    return this.api.get<PaginatedResponse<Document>>(url);
  }

  deleteDocument(id: string): Observable<void> {
    return this.api.delete<void>(`/documents/${id}/`);
  }

  reprocessDocument(id: string): Observable<any> {
    return this.api.post(`/documents/${id}/reprocess/`, {});
  }
}