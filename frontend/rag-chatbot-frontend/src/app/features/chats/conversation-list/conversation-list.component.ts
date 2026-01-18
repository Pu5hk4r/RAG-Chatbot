import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { NavbarComponent } from '../../../shared/components/navbars/navbar.component';
import { ChatService } from '../../../core/services/chat.service';
import { DocumentService } from '../../../core/services/document.service';
import { Conversation } from '../../../core/models/chat.model';
import { DocumentCollection } from '../../../core/models/document.model';

@Component({
  selector: 'app-conversation-list',
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule, NavbarComponent],
  template: `
    <app-navbar></app-navbar>
    
    <div class="container">
      <div class="header">
        <h1>Conversations</h1>
        <button (click)="showCreateModal = true" class="btn-primary">
          ➕ New Conversation
        </button>
      </div>

      <div class="conversations-list">
        <div class="conversation-item" *ngFor="let conv of conversations"
             [routerLink]="['/chat', conv.id]">
          <div class="conv-info">
            <h3>{{ conv.title }}</h3>
            <p>{{ conv.collection_name }} · {{ conv.message_count }} messages</p>
          </div>
          <div class="conv-meta">
            <small>{{ conv.updated_at | date:'short' }}</small>
          </div>
        </div>

        <div class="empty-state" *ngIf="conversations.length === 0">
          <p>No conversations yet. Start chatting with your documents!</p>
        </div>
      </div>

      <!-- Create Conversation Modal -->
      <div class="modal" *ngIf="showCreateModal" (click)="showCreateModal = false">
        <div class="modal-content" (click)="$event.stopPropagation()">
          <h2>New Conversation</h2>
          <form (ngSubmit)="createConversation()">
            <div class="form-group">
              <label>Collection</label>
              <select [(ngModel)]="newConversation.collection" name="collection" required>
                <option value="">Select a collection</option>
                <option *ngFor="let col of collections" [value]="col.id">
                  {{ col.name }}
                </option>
              </select>
            </div>
            <div class="form-group">
              <label>Title</label>
              <input type="text" [(ngModel)]="newConversation.title" name="title" required />
            </div>
            <div class="modal-actions">
              <button type="button" (click)="showCreateModal = false" class="btn-secondary">Cancel</button>
              <button type="submit" class="btn-primary">Create</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 2rem;
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 2rem;
    }
    .conversations-list {
      background: white;
      border-radius: 8px;
      overflow: hidden;
    }
    .conversation-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1.5rem;
      border-bottom: 1px solid #eee;
      cursor: pointer;
      transition: background 0.3s;
    }
    .conversation-item:hover {
      background: #f8f9fa;
    }
    .conv-info h3 {
      margin: 0 0 0.5rem 0;
      font-size: 1.1rem;
    }
    .conv-info p {
      margin: 0;
      color: #666;
      font-size: 0.875rem;
    }
    .conv-meta small {
      color: #999;
    }
    .modal {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0,0,0,0.5);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 1000;
    }
    .modal-content {
      background: white;
      padding: 2rem;
      border-radius: 8px;
      width: 90%;
      max-width: 500px;
    }
    .form-group {
      margin-bottom: 1rem;
    }
    label {
      display: block;
      margin-bottom: 0.5rem;
      font-weight: 500;
    }
    input, select {
      width: 100%;
      padding: 0.75rem;
      border: 1px solid #ddd;
      border-radius: 4px;
      box-sizing: border-box;
    }
    .modal-actions {
      display: flex;
      gap: 1rem;
      justify-content: flex-end;
      margin-top: 1.5rem;
    }
    .btn-primary, .btn-secondary {
      padding: 0.75rem 1.5rem;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }
    .btn-primary {
      background: #667eea;
      color: white;
    }
    .btn-secondary {
      background: #e2e8f0;
      color: #333;
    }
  `]
})
export class ConversationListComponent implements OnInit {
  conversations: Conversation[] = [];
  collections: DocumentCollection[] = [];
  showCreateModal = false;
  newConversation = { collection: '', title: 'New Conversation' };

  constructor(
    private chatService: ChatService,
    private documentService: DocumentService
  ) {}

  ngOnInit() {
    this.loadConversations();
    this.loadCollections();
  }

  loadConversations() {
    this.chatService.getConversations().subscribe({
      next: (response) => {
        this.conversations = response.results;
      }
    });
  }

  loadCollections() {
    this.documentService.getCollections().subscribe({
      next: (response) => {
        this.collections = response.results.filter(c => c.has_vectordb);
      }
    });
  }

  createConversation() {
    this.chatService.createConversation(this.newConversation).subscribe({
      next: () => {
        this.showCreateModal = false;
        this.newConversation = { collection: '', title: 'New Conversation' };
        this.loadConversations();
      }
    });
  }
}
