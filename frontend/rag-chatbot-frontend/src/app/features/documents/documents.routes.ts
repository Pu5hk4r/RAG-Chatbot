import { Routes } from '@angular/router';

export const DOCUMENTS_ROUTES: Routes = [
  {
    path: '',
    loadComponent: () => import('./collection-list/collection-list.component').then(m => m.CollectionListComponent)
  },
  {
    path: ':id',
    loadComponent: () => import('./collection-detail/collection-detail.component').then(m => m.CollectionDetailComponent)
  }
];