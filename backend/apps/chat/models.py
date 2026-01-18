# apps/chat/models.py
from django.db import models
from django.contrib.auth.models import User
from apps.documents.models import DocumentCollection
import uuid

class Conversation(models.Model):
    """Chat conversation sessions"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    collection = models.ForeignKey(DocumentCollection, on_delete=models.CASCADE, related_name='conversations')
    title = models.CharField(max_length=255)
    llm_model = models.CharField(max_length=100, default='meta-llama/Meta-Llama-3-8B-Instruct')
    temperature = models.FloatField(default=0.5)
    max_tokens = models.IntegerField(default=4096)
    top_k = models.IntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_archived = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['user', '-updated_at']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"


class Message(models.Model):
    """Individual messages in conversations"""
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
        ('system', 'System'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Metadata
    tokens_used = models.IntegerField(null=True, blank=True)
    processing_time = models.FloatField(null=True, blank=True)
    
    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['conversation', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.role}: {self.content[:50]}..."


class SourceReference(models.Model):
    """References to source documents for message responses"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='sources')
    document = models.ForeignKey('documents.Document', on_delete=models.CASCADE)
    chunk_content = models.TextField()
    page_number = models.IntegerField()
    relevance_score = models.FloatField()
    
    class Meta:
        ordering = ['-relevance_score']
    
    def __str__(self):
        return f"Source for {self.message.id} - Page {self.page_number}"
