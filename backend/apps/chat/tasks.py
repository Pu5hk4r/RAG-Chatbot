# apps/chat/tasks.py
from celery import shared_task
from .models import Conversation, Message
import logging

logger = logging.getLogger(__name__)


@shared_task
def update_conversation_statistics(conversation_id: str):
    """Update conversation-related statistics"""
    try:
        conversation = Conversation.objects.get(id=conversation_id)
        user = conversation.user
        profile = user.profile
        
        # Update profile statistics
        profile.total_conversations = user.conversations.count()
        profile.total_messages = Message.objects.filter(
            conversation__user=user
        ).count()
        profile.save()
        
        logger.info(f"Updated statistics for user: {user.username}")
        
        return {
            'status': 'success',
            'user': user.username
        }
        
    except Conversation.DoesNotExist:
        logger.error(f"Conversation not found: {conversation_id}")
        raise


@shared_task
def generate_conversation_summary(conversation_id: str):
    """Generate a summary of conversation for better titles"""
    try:
        conversation = Conversation.objects.get(id=conversation_id)
        
        # Get first few messages
        messages = conversation.messages.filter(role='user')[:3]
        
        if messages.exists():
            # Create simple summary from first message
            first_message = messages.first().content
            summary = first_message[:50] + "..." if len(first_message) > 50 else first_message
            
            if conversation.title == "New Conversation":
                conversation.title = summary
                conversation.save()
        
        return {
            'status': 'success',
            'conversation_id': str(conversation.id),
            'title': conversation.title
        }
        
    except Conversation.DoesNotExist:
        logger.error(f"Conversation not found: {conversation_id}")
        raise