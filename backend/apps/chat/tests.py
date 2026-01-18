# apps/chat/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from apps.documents.models import DocumentCollection
from .models import Conversation, Message


class ConversationTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        self.collection = DocumentCollection.objects.create(
            user=self.user,
            name='Test Collection'
        )
    
    def test_create_conversation(self):
        """Test creating a conversation"""
        data = {
            'collection': str(self.collection.id),
            'title': 'Test Conversation',
            'llm_model': 'meta-llama/Meta-Llama-3-8B-Instruct'
        }
        
        response = self.client.post('/api/v1/conversations/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Conversation.objects.count(), 1)
    
    def test_list_conversations(self):
        """Test listing conversations"""
        Conversation.objects.create(
            user=self.user,
            collection=self.collection,
            title='Conv 1'
        )
        Conversation.objects.create(
            user=self.user,
            collection=self.collection,
            title='Conv 2'
        )
        
        response = self.client.get('/api/v1/conversations/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)