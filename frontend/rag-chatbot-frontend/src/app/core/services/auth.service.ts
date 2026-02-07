
// ============================================
// src/app/core/services/auth.service.ts
// ============================================
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, tap } from 'rxjs';
import { HttpErrorResponse } from '@angular/common/http';
import { ApiService } from './api.service';
import { User, LoginRequest, RegisterRequest, AuthResponse } from '../models/user.model';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private currentUserSubject = new BehaviorSubject<User | null>(null);
  public currentUser$ = this.currentUserSubject.asObservable();
  
  private tokenKey = 'auth_token';

  constructor(private api: ApiService) {
    this.loadStoredUser();
  }

  login(credentials: LoginRequest): Observable<AuthResponse> {
    return this.api.post<AuthResponse>('/auth/login/', credentials).pipe(
      tap(response => {
        this.setToken(response.token);
      })
    );
  }

  register(userData: RegisterRequest): Observable<User> {
    return this.api.post<User>('/users/', userData);
  }

  logout(): void {
    localStorage.removeItem(this.tokenKey);
    this.currentUserSubject.next(null);
  }

  getToken(): string | null {
    return localStorage.getItem(this.tokenKey);
  }

  setToken(token: string): void {
    localStorage.setItem(this.tokenKey, token);
  }

  isAuthenticated(): boolean {
    return !!this.getToken();
  }

  loadCurrentUser(): void {
    this.api.get<User>('/users/me/').subscribe({
      next: user => this.currentUserSubject.next(user),
      error: (error: HttpErrorResponse) => {
        // Only clear token on auth failures; keep it for transient/network errors.
        if (error?.status === 401 || error?.status === 403) {
          this.logout();
        } else {
          this.currentUserSubject.next(null);
        }
      }
    });
  }

  private loadStoredUser(): void {
    if (this.isAuthenticated()) {
      this.loadCurrentUser();
    }
  }

  getDashboard(): Observable<any> {
    return this.api.get('/users/dashboard/');
  }
}
