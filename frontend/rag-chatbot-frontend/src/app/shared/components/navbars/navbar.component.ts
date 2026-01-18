// ============================================
// src/app/shared/components/navbar/navbar.component.ts
// ============================================
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Router } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';
import { User } from '../../../core/models/user.model';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <nav class="navbar">
      <div class="container">
        <div class="navbar-brand">
          <a routerLink="/dashboard" class="logo">
            📚 RAG Chatbot
          </a>
        </div>

        <div class="navbar-menu">
          <a routerLink="/dashboard" routerLinkActive="active">Dashboard</a>
          <a routerLink="/collections" routerLinkActive="active">Collections</a>
          <a routerLink="/chat" routerLinkActive="active">Chat</a>
        </div>

        <div class="navbar-user" *ngIf="currentUser">
          <span class="username">{{ currentUser.username }}</span>
          <button (click)="logout()" class="btn-logout">Logout</button>
        </div>
      </div>
    </nav>
  `,
  styles: [`
    .navbar {
      background: #1a1a2e;
      color: white;
      padding: 1rem 0;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 0 1rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .logo {
      font-size: 1.5rem;
      font-weight: bold;
      color: white;
      text-decoration: none;
    }
    .navbar-menu {
      display: flex;
      gap: 2rem;
    }
    .navbar-menu a {
      color: white;
      text-decoration: none;
      padding: 0.5rem 1rem;
      border-radius: 4px;
      transition: background 0.3s;
    }
    .navbar-menu a:hover,
    .navbar-menu a.active {
      background: rgba(255,255,255,0.1);
    }
    .navbar-user {
      display: flex;
      align-items: center;
      gap: 1rem;
    }
    .btn-logout {
      background: #e74c3c;
      color: white;
      border: none;
      padding: 0.5rem 1rem;
      border-radius: 4px;
      cursor: pointer;
    }
    .btn-logout:hover {
      background: #c0392b;
    }
  `]
})
export class NavbarComponent implements OnInit {
  currentUser: User | null = null;

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit() {
    this.authService.currentUser$.subscribe(user => {
      this.currentUser = user;
    });
  }

  logout() {
    this.authService.logout();
    this.router.navigate(['/auth/login']);
  }
}