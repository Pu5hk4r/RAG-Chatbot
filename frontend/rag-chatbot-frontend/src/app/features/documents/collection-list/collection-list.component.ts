import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { NavbarComponent } from '../../../shared/components/navbars/navbar.component';
import { LoadingComponent } from '../../../shared/components/loading/loading.component';
import { DocumentService } from '../../../core/services/document.service';
import { DocumentCollection } from '../../../core/models/document.model';

@Component({
  selector: 'app-collection-list',
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule, NavbarComponent, LoadingComponent],
  template: `
    <app-navbar></app-navbar>
    
    <div class="container">
      <div class="header">
        <h1>Document Collections</h1>
        <button (click)="showCreateModal = true" class="btn-primary">
          ➕ New Collection
        </button>
      </div>

      <app-loading *ngIf="loading"></app-loading>

      <div class="collections-grid" *ngIf="!loading">
        <div class="collection-card" *ngFor="let collection of collections" 
             [routerLink]="['/collections', collection.id]">
          <div class="card-header">
            <h3>{{ collection.name }}</h3>
            <span class="badge" [class.ready]="collection.has_vectordb">
              {{ collection.has_vectordb ? '✓ Ready' : 'Setup Required' }}
            </span>
          </div>
          <p class="description">{{ collection.description || 'No description' }}</p>
          <div class="card-stats">
            <span>📄 {{ collection.document_count }} documents</span>
            <span>📖 {{ collection.total_pages }} pages</span>
          </div>
          <div class="card-footer">
            <small>Created {{ collection.created_at | date:'short' }}</small>
          </div>
        </div>

        <div class="empty-state" *ngIf="collections.length === 0">
          <p>No collections yet. Create your first one!</p>
        </div>
      </div>

      <!-- Create Collection Modal -->
      <div class="modal" *ngIf="showCreateModal" (click)="showCreateModal = false">
        <div class="modal-content" (click)="$event.stopPropagation()">
          <h2>Create New Collection</h2>
          <form (ngSubmit)="createCollection()">
            <div class="form-group">
              <label>Name</label>
              <input type="text" [(ngModel)]="newCollection.name" name="name" required />
            </div>
            <div class="form-group">
              <label>Description</label>
              <textarea [(ngModel)]="newCollection.description" name="description" rows="3"></textarea>
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
    .collections-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 1.5rem;
    }
    .collection-card {
      background: white;
      padding: 1.5rem;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      cursor: pointer;
      transition: transform 0.3s, box-shadow 0.3s;
    }
    .collection-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: start;
      margin-bottom: 1rem;
    }
    .card-header h3 {
      margin: 0;
      font-size: 1.25rem;
    }
    .badge {
      padding: 0.25rem 0.75rem;
      border-radius: 12px;
      font-size: 0.875rem;
      background: #ffc107;
      color: white;
    }
    .badge.ready {
      background: #48bb78;
    }
    .description {
      color: #666;
      margin-bottom: 1rem;
    }
    .card-stats {
      display: flex;
      gap: 1rem;
      margin-bottom: 1rem;
      color: #666;
      font-size: 0.875rem;
    }
    .card-footer small {
      color: #999;
      font-size: 0.75rem;
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
    input, textarea {
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
    .empty-state {
      text-align: center;
      padding: 3rem;
      color: #999;
    }
  `]
})
export class CollectionListComponent implements OnInit {
  collections: DocumentCollection[] = [];
  loading = true;
  showCreateModal = false;
  newCollection = { name: '', description: '' };

  constructor(private documentService: DocumentService) {}

  ngOnInit() {
    this.loadCollections();
  }

  loadCollections() {
    this.documentService.getCollections().subscribe({
      next: (response) => {
        this.collections = response.results;
        this.loading = false;
      },
      error: () => {
        this.loading = false;
      }
    });
  }

  createCollection() {
    this.documentService.createCollection(this.newCollection).subscribe({
      next: () => {
        this.showCreateModal = false;
        this.newCollection = { name: '', description: '' };
        this.loadCollections();
      }
    });
  }
}