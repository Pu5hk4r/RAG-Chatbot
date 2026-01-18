# apps/documents/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import DocumentCollection, Document
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile


class DocumentCollectionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_create_collection(self):
        """Test creating a document collection"""
        data = {
            'name': 'Test Collection',
            'description': 'Test Description'
        }
        response = self.client.post('/api/v1/collections/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DocumentCollection.objects.count(), 1)
        self.assertEqual(DocumentCollection.objects.first().name, 'Test Collection')
    
    def test_list_collections(self):
        """Test listing collections"""
        DocumentCollection.objects.create(
            user=self.user,
            name='Collection 1'
        )
        DocumentCollection.objects.create(
            user=self.user,
            name='Collection 2'
        )
        
        response = self.client.get('/api/v1/collections/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)


class DocumentTestCase(APITestCase):
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
    
    def test_upload_document(self):
        """Test uploading a document"""
        # Create a simple PDF file (mock)
        pdf_file = SimpleUploadedFile(
            "test.pdf",
            b"file_content",
            content_type="application/pdf"
        )
        
        data = {
            'file': pdf_file,
            'collection': str(self.collection.id)
        }
        
        response = self.client.post('/api/v1/documents/', data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)