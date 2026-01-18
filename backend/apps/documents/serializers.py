# apps/documents/serializers.py
from rest_framework import serializers
from .models import DocumentCollection, Document, DocumentChunk


class DocumentChunkSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentChunk
        fields = ['id', 'content', 'page_number', 'chunk_index']


class DocumentSerializer(serializers.ModelSerializer):
    chunk_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = [
            'id', 'collection', 'filename', 'file_size', 
            'page_count', 'status', 'error_message', 
            'uploaded_at', 'processed_at', 'chunk_count'
        ]
        read_only_fields = [
            'id', 'page_count', 'status', 'error_message', 
            'uploaded_at', 'processed_at'
        ]
    
    def get_chunk_count(self, obj):
        return obj.chunks.count()


class DocumentCollectionSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)
    document_count = serializers.SerializerMethodField()
    total_pages = serializers.SerializerMethodField()
    has_vectordb = serializers.SerializerMethodField()
    
    class Meta:
        model = DocumentCollection
        fields = [
            'id', 'name', 'description', 'is_public',
            'created_at', 'updated_at', 'documents',
            'document_count', 'total_pages', 'has_vectordb'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_document_count(self, obj):
        return obj.documents.filter(status='ready').count()
    
    def get_total_pages(self, obj):
        return sum(
            doc.page_count or 0 
            for doc in obj.documents.filter(status='ready')
        )
    
    def get_has_vectordb(self, obj):
        return bool(obj.vector_db_path)