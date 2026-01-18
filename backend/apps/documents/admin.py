# apps/documents/admin.py
from django.contrib import admin
from .models import DocumentCollection, Document, DocumentChunk


@admin.register(DocumentCollection)
class DocumentCollectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'is_public', 'created_at', 'document_count']
    list_filter = ['is_public', 'created_at']
    search_fields = ['name', 'description', 'user__username']
    readonly_fields = ['id', 'created_at', 'updated_at', 'vector_db_path']
    
    def document_count(self, obj):
        return obj.documents.count()
    document_count.short_description = 'Documents'


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['filename', 'collection', 'status', 'page_count', 'uploaded_at']
    list_filter = ['status', 'uploaded_at']
    search_fields = ['filename', 'collection__name']
    readonly_fields = ['id', 'file_size', 'page_count', 'uploaded_at', 'processed_at']


@admin.register(DocumentChunk)
class DocumentChunkAdmin(admin.ModelAdmin):
    list_display = ['document', 'page_number', 'chunk_index']
    list_filter = ['document']
    search_fields = ['content']
    readonly_fields = ['id']