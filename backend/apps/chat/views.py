# apps/chat/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .services import ChatService
from apps.documents.models import DocumentCollection


class ConversationViewSet(viewsets.ModelViewSet):
    """API endpoint for conversations"""
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Conversation.objects.filter(user=self.request.user)
        
        # Filter by collection
        collection_id = self.request.query_params.get('collection')
        if collection_id:
            queryset = queryset.filter(collection_id=collection_id)
        
        # Filter archived
        is_archived = self.request.query_params.get('archived')
        if is_archived is not None:
            queryset = queryset.filter(is_archived=is_archived.lower() == 'true')
        
        return queryset.annotate(message_count=Count('messages'))
    
    def perform_create(self, serializer):
        # Auto-generate title from first message if not provided
        title = serializer.validated_data.get('title', 'New Conversation')
        serializer.save(user=self.request.user, title=title)
    
    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        """Send a message in the conversation"""
        conversation = self.get_object()
        message_content = request.data.get('message')
        
        if not message_content:
            return Response(
                {'error': 'Message content required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if vector DB is ready
        if not conversation.collection.vector_db_path:
            return Response(
                {'error': 'Vector database not initialized for this collection'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Process message
        chat_service = ChatService()
        try:
            response_text, sources = chat_service.process_message(
                conversation,
                message_content
            )
            
            return Response({
                'response': response_text,
                'sources': sources,
                'message_id': str(conversation.messages.filter(role='assistant').last().id)
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        """Get conversation history"""
        conversation = self.get_object()
        chat_service = ChatService()
        history = chat_service.get_conversation_history(conversation)
        
        return Response({'history': history})
    
    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        """Archive/unarchive conversation"""
        conversation = self.get_object()
        conversation.is_archived = not conversation.is_archived
        conversation.save()
        
        return Response({
            'is_archived': conversation.is_archived,
            'message': 'Conversation archived' if conversation.is_archived else 'Conversation unarchived'
        })
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get user's conversation statistics"""
        user = request.user
        
        stats = {
            'total_conversations': Conversation.objects.filter(user=user).count(),
            'active_conversations': Conversation.objects.filter(
                user=user,
                is_archived=False
            ).count(),
            'archived_conversations': Conversation.objects.filter(
                user=user,
                is_archived=True
            ).count(),
            'total_messages': Message.objects.filter(
                conversation__user=user
            ).count(),
            'user_messages': Message.objects.filter(
                conversation__user=user,
                role='user'
            ).count(),
            'assistant_messages': Message.objects.filter(
                conversation__user=user,
                role='assistant'
            ).count()
        }
        
        return Response(stats)


class MessageViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for messages (read-only)"""
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Message.objects.filter(
            conversation__user=self.request.user
        )
