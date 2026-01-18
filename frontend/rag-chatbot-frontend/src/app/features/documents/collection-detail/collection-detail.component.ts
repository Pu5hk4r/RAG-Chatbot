import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { NavbarComponent } from '../../../shared/components/navbars/navbar.component';
import { DocumentService } from '../../../core/services/document.service';
import { DocumentCollection, Document } from '../../../core/models/document.model';

@Component({
  selector: 'app-collection-detail',
  standalone: true,
  imports: [CommonModule, RouterModule, NavbarComponent],
  template: `
    <app-navbar></app-navbar>
    
    <div class="container" *ngIf="collection">
      <div class="header">
        <div>
          <h1>{{ collection.name }}</h1>
          <p>{{ collection.description }}</p>
        </div>
        <div class="actions">
          <label class="btn-primary upload-btn">
            📤 Upload PDF
            <input type="file" (change)="onFileSelected($event)" accept=".pdf" hidden />
          </label>
          <button (click)="createVectorDB()" 
                  [disabled]="collection.has_vectordb || uploading"
                  class="btn-secondary">
            {{ collection.has_vectordb ? '✓ Vector DB Ready' : 'Create Vector DB' }}
          </button>
        </div>
      </div>

      <div class="documents-list">
        <h2>Documents ({{ collection.documents?.length || 0 }})</h2>
        
        <div class="document-item" *ngFor="let doc of collection.documents">
          <div class="doc-info">
            <span class="doc-name">📄 {{ doc.filename }}</span>
            <span class="doc-meta">
              {{ (doc.file_size / 1024 / 1024).toFixed(2) }} MB
              <span *ngIf="doc.page_count"> · {{ doc.page_count }} pages</span>
            </span>
          </div>
          <div class="doc-status">
            <span class="status-badge" [class]="doc.status">
              {{ doc.status }}
            </span>
          </div>
        </div>

        <div class="empty-state" *ngIf="!collection.documents?.length">
          <p>No documents uploaded yet</p>
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
      align-items: start;
      margin-bottom: 2rem;
    }
    .actions {
      display: flex;
      gap: 1rem;
    }
    .upload-btn {
      display: inline-block;
      cursor: pointer;
    }
    .documents-list {
      background: white;
      padding: 2rem;
      border-radius: 8px;
    }
    .document-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1rem;
      border-bottom: 1px solid #eee;
    }
    .doc-info {
      display: flex;
      flex-direction: column;
      gap: 0.25rem;
    }
    .doc-name {
      font-weight: 500;
    }
    .doc-meta {
      font-size: 0.875rem;
      color: #666;
    }
    .status-badge {
      padding: 0.25rem 0.75rem;
      border-radius: 12px;
      font-size: 0.875rem;
      text-transform: uppercase;
    }
    .status-badge.ready {
      background: #48bb78;
      color: white;
    }
    .status-badge.processing {
      background: #ffc107;
      color: white;
    }
    .status-badge.failed {
      background: #e74c3c;
      color: white;
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
      background: #48bb78;
      color: white;
    }
    .btn-secondary:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
  `]
})
export class CollectionDetailComponent implements OnInit {
  collection: DocumentCollection | null = null;
  uploading = false;

  constructor(
    private route: ActivatedRoute,
    private documentService: DocumentService
  ) {}

  ngOnInit() {
    const id = this.route.snapshot.paramMap.get('id')!;
    this.loadCollection(id);
  }

  loadCollection(id: string) {
    this.documentService.getCollection(id).subscribe({
      next: (data) => {
        this.collection = data;
      }
    });
  }

  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (file && this.collection) {
      this.uploading = true;
      this.documentService.uploadDocument(this.collection.id, file).subscribe({
        next: () => {
          this.uploading = false;
          this.loadCollection(this.collection!.id);
        },
        error: () => {
          this.uploading = false;
        }
      });
    }
  }

  createVectorDB() {
    if (this.collection) {
      this.documentService.createVectorDB(this.collection.id).subscribe({
        next: () => {
          alert('Vector database creation started!');
          setTimeout(() => this.loadCollection(this.collection!.id), 2000);
        }
      });
    }
  }
}