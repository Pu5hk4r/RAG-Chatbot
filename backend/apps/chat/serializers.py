# apps/chat/serializers.py
from rest_framework import serializers
from .models import Conversation, Message, SourceReference


class SourceReferenceSerializer(serializers.ModelSerializer):
    document_name = serializers.CharField(source='document.filename', read_only=True)
    
    class Meta:
        model = SourceReference
        fields = [
            'id', 'document_name', 'chunk_content', 
            'page_number', 'relevance_score'
        ]


class MessageSerializer(serializers.ModelSerializer):
    sources = SourceReferenceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Message
        fields = [
            'id', 'role', 'content', 'created_at',
            'tokens_used', 'processing_time', 'sources'
        ]
        read_only_fields = [
            'id', 'created_at', 'tokens_used', 'processing_time'
        ]


class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    message_count = serializers.IntegerField(read_only=True)
    collection_name = serializers.CharField(source='collection.name', read_only=True)
    
    class Meta:
        model = Conversation
        fields = [
            'id', 'collection', 'collection_name', 'title',
            'llm_model', 'temperature', 'max_tokens', 'top_k',
            'created_at', 'updated_at', 'is_archived',
            'messages', 'message_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']