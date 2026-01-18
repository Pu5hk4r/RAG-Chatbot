# apps/users/models.py
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """Extended user profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    # Usage tracking
    total_documents_uploaded = models.IntegerField(default=0)
    total_conversations = models.IntegerField(default=0)
    total_messages = models.IntegerField(default=0)
    
    # Preferences
    default_llm_model = models.CharField(max_length=100, default='meta-llama/Meta-Llama-3-8B-Instruct')
    default_temperature = models.FloatField(default=0.5)
    default_max_tokens = models.IntegerField(default=4096)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Profile: {self.user.username}"