# apps/chat/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Conversation
from .tasks import update_conversation_statistics, generate_conversation_summary


@receiver(post_save, sender=Message)
def update_stats_on_message(sender, instance, created, **kwargs):
    """Update statistics when message is created"""
    if created:
        update_conversation_statistics.delay(str(instance.conversation.id))


@receiver(post_save, sender=Conversation)
def auto_generate_title(sender, instance, created, **kwargs):
    """Auto-generate conversation title from first message"""
    if created:
        generate_conversation_summary.delay(str(instance.id))