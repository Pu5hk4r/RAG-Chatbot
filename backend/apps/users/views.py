# apps/users/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from .models import UserProfile
from .serializers import UserSerializer, UserProfileSerializer


class UserViewSet(viewsets.ModelViewSet):
    """API endpoint for users"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user info"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Get user dashboard data"""
        user = request.user
        profile = user.profile
        
        data = {
            'user': UserSerializer(user).data,
            'profile': UserProfileSerializer(profile).data,
            'recent_collections': user.collections.all()[:5].values('id', 'name', 'created_at'),
            'recent_conversations': user.conversations.all()[:5].values('id', 'title', 'updated_at')
        }
        
        return Response(data)