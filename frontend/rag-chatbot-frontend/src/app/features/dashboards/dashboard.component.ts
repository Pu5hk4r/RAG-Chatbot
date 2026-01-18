// ============================================
// src/app/features/dashboard/dashboard.component.ts
// ============================================
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { NavbarComponent } from '../../shared/components/navbars/navbar.component';
import { LoadingComponent } from '../../shared/components/loading/loading.component';
import { AuthService } from '../../core/services/auth.service';
import { DocumentService } from '../../core/services/document.service';
import { ChatService } from '../../core/services/chat.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule, NavbarComponent, LoadingComponent],
  template: `
    <app-navbar></app-navbar>
    
    <div class="container">
      <h1>Dashboard</h1>

      <app-loading *ngIf="loading"></app-loading>

      <div class="stats-grid" *ngIf="!loading && dashboardData">
        <div class="stat-card">
          <div class="stat-icon">📚</div>
          <div class="stat-content">
            <h3>{{ dashboardData.profile?.total_documents_uploaded || 0 }}</h3>
            <p>Documents Uploaded</p>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">💬</div>
          <div class="stat-content">
            <h3>{{ dashboardData.profile?.total_conversations || 0 }}</h3>
            <p>Conversations</p>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">✉️</div>
          <div class="stat-content">
            <h3>{{ dashboardData.profile?.total_messages || 0 }}</h3>
            <p>Total Messages</p>
          </div>
        </div>
      </div>

      <div class="actions">
        <button routerLink="/collections" class="btn-primary">
          📁 Manage Collections
        </button>
        <button routerLink="/chat" class="btn-secondary">
          💬 Start Chatting
        </button>
      </div>
    </div>
  `,
  styles: [`
    .container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 2rem;
    }
    h1 {
      margin-bottom: 2rem;
    }
    .stats-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 1.5rem;
      margin-bottom: 2rem;
    }
    .stat-card {
      background: white;
      padding: 2rem;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      display: flex;
      align-items: center;
      gap: 1rem;
    }
    .stat-icon {
      font-size: 3rem;
    }
    .stat-content h3 {
      font-size: 2rem;
      margin: 0;
      color: #333;
    }
    .stat-content p {
      margin: 0;
      color: #666;
    }
    .actions {
      display: flex;
      gap: 1rem;
      margin-top: 2rem;
    }
    .btn-primary, .btn-secondary {
      padding: 1rem 2rem;
      border: none;
      border-radius: 4px;
      font-size: 1rem;
      cursor: pointer;
      transition: all 0.3s;
    }
    .btn-primary {
      background: #667eea;
      color: white;
    }
    .btn-secondary {
      background: #48bb78;
      color: white;
    }
  `]
})
export class DashboardComponent implements OnInit {
  loading = true;
  dashboardData: any = null;

  constructor(private authService: AuthService) {}

  ngOnInit() {
    this.authService.getDashboard().subscribe({
      next: (data) => {
        this.dashboardData = data;
        this.loading = false;
      },
      error: () => {
        this.loading = false;
      }
    });
  }
}