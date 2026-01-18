

// ============================================
// src/app/core/services/auth.service.ts
// ============================================
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, tap } from 'rxjs';
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
        this.loadCurrentUser();
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
      error: () => this.logout()
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