# apps/users/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'bio', 'avatar', 'total_documents_uploaded',
            'total_conversations', 'total_messages',
            'default_llm_model', 'default_temperature',
            'default_max_tokens', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'total_documents_uploaded', 'total_conversations',
            'total_messages', 'created_at', 'updated_at'
        ]


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name',
            'last_name', 'password', 'profile', 'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        
        # Create profile
        UserProfile.objects.create(user=user)
        
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance