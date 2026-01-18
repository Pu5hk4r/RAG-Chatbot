# apps/documents/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Document
from .tasks import process_document_task
import os


@receiver(post_delete, sender=Document)
def delete_document_file(sender, instance, **kwargs):
    """Delete file from filesystem when Document is deleted"""
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)