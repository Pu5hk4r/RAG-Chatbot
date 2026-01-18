# apps/chat/admin.py
from django.contrib import admin
from .models import Conversation, Message, SourceReference


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'collection', 'llm_model', 'created_at', 'message_count']
    list_filter = ['is_archived', 'llm_model', 'created_at']
    search_fields = ['title', 'user__username', 'collection__name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = 'Messages'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'role', 'content_preview', 'created_at', 'processing_time']
    list_filter = ['role', 'created_at']
    search_fields = ['content', 'conversation__title']
    readonly_fields = ['id', 'created_at']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'


@admin.register(SourceReference)
class SourceReferenceAdmin(admin.ModelAdmin):
    list_display = ['message', 'document', 'page_number', 'relevance_score']
    list_filter = ['page_number']
    search_fields = ['chunk_content', 'document__filename']
    readonly_fields = ['id']