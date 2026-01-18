import {
  Component,
  OnInit,
  ViewChild,
  ElementRef
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { FormsModule } from '@angular/forms';

import { NavbarComponent } from 'app/shared/components/navbars/navbar.component';
import { ChatService } from 'app/core/services/chat.service';
import { Message } from 'app/core/models/chat.model';

@Component({
  selector: 'app-chat-room',
  standalone: true,
  imports: [CommonModule, FormsModule, NavbarComponent],
  template: `
    <app-navbar></app-navbar>

    <div class="chat-container">
      <div class="messages-container" #messagesContainer>
        <div
          class="message"
          *ngFor="let msg of messages"
          [class.user]="msg.role === 'user'"
        >
          <div class="message-bubble">
            <div class="message-header">
              <strong>{{ msg.role === 'user' ? 'You' : 'Assistant' }}</strong>
              <small>{{ msg.created_at | date: 'short' }}</small>
            </div>

            <div class="message-content">
              {{ msg.content }}
            </div>

            <div class="sources" *ngIf="msg.sources?.length">
              <p class="sources-title">📚 Sources:</p>
              <div class="source-item" *ngFor="let source of msg.sources">
                <strong>
                  {{ source.document_name }} (Page {{ source.page_number }})
                </strong>
                <p>{{ source.chunk_content }}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="typing-indicator" *ngIf="sending">
          <span class="dot"></span>
          <span class="dot"></span>
          <span class="dot"></span>
        </div>
      </div>

      <div class="input-container">
        <textarea
          [(ngModel)]="currentMessage"
          (keydown.enter)="onEnter($event)"
          placeholder="Type your message… (Shift+Enter for new line)"
          rows="3"
        ></textarea>

        <button
          class="btn-send"
          (click)="sendMessage()"
          [disabled]="!currentMessage.trim() || sending"
        >
          {{ sending ? '⏳' : '📤 Send' }}
        </button>
      </div>
    </div>
  `
})
export class ChatRoomComponent implements OnInit {
  @ViewChild('messagesContainer')
  messagesContainer!: ElementRef<HTMLDivElement>;

  messages: Message[] = [];
  currentMessage = '';
  sending = false;
  conversationId!: string;

  constructor(
    private route: ActivatedRoute,
    private chatService: ChatService
  ) {}

  ngOnInit(): void {
    this.conversationId = this.route.snapshot.paramMap.get('id')!;
    this.loadHistory();
  }

  onEnter(event: Event): void {
    const keyboardEvent = event as KeyboardEvent;

    if (keyboardEvent.shiftKey) return;

    keyboardEvent.preventDefault();
    this.sendMessage();
  }

  loadHistory(): void {
    this.chatService.getHistory(this.conversationId).subscribe({
      next: (res: any) => {
        this.messages = res.history;
        this.scrollToBottom();
      }
    });
  }

  sendMessage(): void {
    if (!this.currentMessage.trim() || this.sending) return;

    const content = this.currentMessage;
    this.currentMessage = '';
    this.sending = true;

    this.messages.push({
      id: '',
      role: 'user',
      content,
      created_at: new Date().toISOString()
    });

    this.scrollToBottom();

    this.chatService.sendMessage(this.conversationId, content).subscribe({
      next: (res: any) => {
        this.messages.push({
          id: res.message_id,
          role: 'assistant',
          content: res.response,
          created_at: new Date().toISOString(),
          sources: res.sources
        });
        this.sending = false;
        this.scrollToBottom();
      },
      error: () => {
        this.sending = false;
      }
    });
  }

  private scrollToBottom(): void {
    setTimeout(() => {
      const el = this.messagesContainer.nativeElement;
      el.scrollTop = el.scrollHeight;
    }, 100);
  }
}
