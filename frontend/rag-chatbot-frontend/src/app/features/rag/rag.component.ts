import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { NavbarComponent } from '../../shared/components/navbars/navbar.component';
import { DocumentService } from '../../core/services/document.service';
import { ChatService } from '../../core/services/chat.service';

@Component({
  selector: 'app-rag',
  standalone: true,
  imports: [CommonModule, FormsModule, NavbarComponent],
  template: `
    <app-navbar></app-navbar>

    <div class="container">
      <h1>RAG — Upload & Chat</h1>

      <div class="panel">
        <h2>1. Create Collection</h2>
        <div class="form-row">
          <input placeholder="Collection name" [(ngModel)]="collectionName" />
          <input placeholder="Description" [(ngModel)]="collectionDescription" />
          <button class="btn-primary" (click)="createCollection()" [disabled]="creatingCollection">{{ creatingCollection ? 'Creating...' : 'Create Collection' }}</button>
        </div>
        <div *ngIf="collection" class="info">Created: {{ collection.name }} ({{ collection.id }})</div>
      </div>

      <div class="panel" *ngIf="collection">
        <h2>2. Upload PDFs</h2>
        <label class="btn-primary">
          Select files
          <input #fileInput type="file" (change)="onFilesSelected($event)" accept=".pdf" multiple hidden />
        </label>
        <button class="btn-primary" (click)="startUpload()" [disabled]="!selectedFiles.length || uploading">{{ uploading ? 'Uploading...' : 'Upload Files' }}</button>

        <div class="documents-list">
          <div *ngFor="let d of documents">
            <strong>{{ d.filename }}</strong> — <span>{{ d.status }}</span>
          </div>
          <div *ngIf="!documents.length">No documents yet.</div>
        </div>
      </div>

      <div class="panel" *ngIf="collection">
        <h2>3. Create Vector DB</h2>
        <button class="btn-secondary" (click)="createVectorDB()" [disabled]="creatingVector">{{ creatingVector ? 'Starting...' : 'Create Vector DB' }}</button>
        <div *ngIf="vectorMessage" class="info">{{ vectorMessage }}</div>
      </div>

      <div class="panel" *ngIf="collection">
        <h2>4. Initialize Conversation & Chat</h2>
        <div class="form-row">
          <label>LLM Model</label>
          <select [(ngModel)]="llmModel">
            <option value="meta-llama/Meta-Llama-3-8B-Instruct">meta-llama/Meta-Llama-3-8B-Instruct</option>
            <option value="mistralai/Mistral-7B-Instruct-v0.2">mistralai/Mistral-7B-Instruct-v0.2</option>
          </select>
          <label>Temp</label>
          <input type="number" step="0.01" min="0" max="1" [(ngModel)]="temperature" />
          <label>Max tokens</label>
          <input type="number" [(ngModel)]="maxTokens" />
          <label>top_k</label>
          <input type="number" [(ngModel)]="topK" />
          <button class="btn-primary" (click)="createConversation()" [disabled]="creatingConversation">{{ creatingConversation ? 'Creating...' : 'Create Conversation' }}</button>
        </div>

        <div *ngIf="conversation">
          <h3>Conversation</h3>
          <div class="chat-box">
            <div *ngFor="let m of messages">
              <div [class.user]="m.role === 'user'">{{ m.role }}: {{ m.content }}</div>
              <div *ngIf="m.sources?.length">
                <small>Sources:</small>
                <ul>
                  <li *ngFor="let s of m.sources">{{ s.document_name }} (Page {{ s.page_number }}): {{ s.chunk_content | slice:0:120 }}...</li>
                </ul>
              </div>
            </div>
          </div>

          <div class="form-row">
            <input placeholder="Ask a question" [(ngModel)]="messageText" />
            <button class="btn-primary" (click)="sendMessage()" [disabled]="!messageText || sending">{{ sending ? 'Sending...' : 'Send' }}</button>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [
    `.container{max-width:1100px;margin:0 auto;padding:1rem}.panel{background:#fff;padding:1rem;margin:1rem 0;border-radius:8px}.form-row{display:flex;gap:8px;align-items:center}.btn-primary{background:#667eea;color:#fff;padding:8px 12px;border-radius:6px;border:none}.btn-secondary{background:#48bb78;color:#fff;padding:8px 12px;border-radius:6px;border:none}.chat-box{background:#f7f7fb;padding:12px;border-radius:6px;max-height:300px;overflow:auto}`
  ]
})
export class RagComponent implements OnInit {
  @ViewChild('fileInput') fileInput!: ElementRef<HTMLInputElement>;

  collectionName = '';
  collectionDescription = '';
  collection: any = null;

  selectedFiles: File[] = [];
  documents: any[] = [];
  uploading = false;
  creatingCollection = false;
  creatingVector = false;
  vectorMessage = '';
  errorMessage = '';

  // LLM params
  llmModel = 'meta-llama/Meta-Llama-3-8B-Instruct';
  temperature = 0.5;
  maxTokens = 4096;
  topK = 3;

  conversation: any = null;
  messages: any[] = [];
  messageText = '';
  creatingConversation = false;
  sending = false;

  constructor(private documentService: DocumentService, private chatService: ChatService) {}

  ngOnInit(): void {
    // nothing
  }

  createCollection() {
    if (!this.collectionName.trim()) return;
    this.creatingCollection = true;
    this.documentService.createCollection({ name: this.collectionName, description: this.collectionDescription }).subscribe({
      next: (c) => {
        this.collection = c as any;
        this.creatingCollection = false;
        this.selectedFiles = [];
        this.documents = [];
      },
      error: () => { this.creatingCollection = false; }
    });
  }

  onFilesSelected(e: any) {
    this.selectedFiles = Array.from(e.target.files || []);
  }

  startUpload() {
    if (!this.collection || !this.selectedFiles.length) return;
    this.uploading = true;
    const uploads = this.selectedFiles.map(file => {
      return new Promise<void>((resolve) => {
        this.documentService.uploadDocument(this.collection.id, file).subscribe({
          next: (doc) => { this.documents.push(doc); resolve(); },
          error: () => { resolve(); }
        });
      });
    });
    Promise.all(uploads).then(() => { this.uploading = false; });
  }

  createVectorDB() {
    if (!this.collection) return;
    this.creatingVector = true;
    this.documentService.createVectorDB(this.collection.id).subscribe({
      next: (res: any) => { this.vectorMessage = res.message || 'Started'; this.creatingVector = false; },
      error: (err) => { this.vectorMessage = err?.error?.error || 'Failed to start'; this.errorMessage = this.vectorMessage; console.error('createVectorDB error', err); this.creatingVector = false; }
    });
  }

  createConversation() {
    if (!this.collection) return;
    this.creatingConversation = true;
    this.chatService.createConversation({
      collection: this.collection.id,
      title: 'RAG Chat',
      llm_model: this.llmModel,
      temperature: this.temperature,
      max_tokens: this.maxTokens,
      top_k: this.topK
    }).subscribe({
      next: (c) => { this.conversation = c; this.messages = []; this.creatingConversation = false; },
      error: (err) => { this.creatingConversation = false; this.errorMessage = err?.error?.detail || err?.message || 'Failed to create conversation'; console.error('createConversation error', err); }
    });
  }

  sendMessage() {
    if (!this.conversation || !this.messageText.trim()) return;
    this.sending = true;
    const userMsg = { role: 'user', content: this.messageText };
    this.messages.push(userMsg);
    this.chatService.sendMessage(this.conversation.id, this.messageText).subscribe({
      next: (res) => {
        const assistant = { role: 'assistant', content: res.response, sources: res.sources };
        this.messages.push(assistant);
        this.messageText = '';
        this.sending = false;
      },
      error: (err) => { this.sending = false; this.errorMessage = err?.error?.error || err?.error?.detail || 'Failed to send message'; console.error('sendMessage error', err); }
    });
  }
}
