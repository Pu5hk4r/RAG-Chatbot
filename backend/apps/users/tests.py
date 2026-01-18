# apps/users/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import UserProfile


class UserTestCase(APITestCase):
    def test_user_registration(self):
        """Test user registration"""
        data = {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password': 'testpass123'
        }
        
        response = self.client.post('/api/v1/users/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        
        # Check profile was created
        user = User.objects.first()
        self.assertTrue(hasattr(user, 'profile'))
    
    def test_user_login(self):
        """Test user login"""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        
        response = self.client.post('/api/v1/auth/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)