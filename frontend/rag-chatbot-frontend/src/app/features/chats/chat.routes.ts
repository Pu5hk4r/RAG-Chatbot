import { Routes } from '@angular/router';

export const CHAT_ROUTES: Routes = [
  {
    path: '',
    loadComponent: () => import('./conversation-list/conversation-list.component').then(m => m.ConversationListComponent)
  },
  {
    path: ':id',
    loadComponent: () => import('./chat-room/chat-room.component').then(m => m.ChatRoomComponent)
  }
];