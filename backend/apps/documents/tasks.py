# apps/documents/tasks.py
from celery import shared_task
from .models import Document, DocumentCollection
from .services import DocumentProcessingService
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def process_document_task(self, document_id: str):
    """Async task to process uploaded document"""
    try:
        document = Document.objects.get(id=document_id)
        service = DocumentProcessingService()
        
        logger.info(f"Processing document: {document.filename}")
        service.process_document(document)
        
        document.processed_at = timezone.now()
        document.save()
        
        logger.info(f"Document processed successfully: {document.filename}")
        
        # Update user profile statistics
        profile = document.collection.user.profile
        profile.total_documents_uploaded += 1
        profile.save()
        
        return {
            'status': 'success',
            'document_id': str(document.id),
            'filename': document.filename
        }
        
    except Document.DoesNotExist:
        logger.error(f"Document not found: {document_id}")
        raise
    
    except Exception as e:
        logger.error(f"Error processing document {document_id}: {str(e)}")
        
        # Retry with exponential backoff
        raise self.retry(exc=e, countdown=60 * (2 ** self.request.retries))


@shared_task(bind=True, max_retries=2)
def create_vectordb_task(self, collection_id: str):
    """Async task to create vector database for collection"""
    try:
        collection = DocumentCollection.objects.get(id=collection_id)
        service = DocumentProcessingService()
        
        logger.info(f"Creating vector database for collection: {collection.name}")
        service.create_vector_database(collection)
        
        logger.info(f"Vector database created successfully for: {collection.name}")
        
        return {
            'status': 'success',
            'collection_id': str(collection.id),
            'collection_name': collection.name
        }
        
    except DocumentCollection.DoesNotExist:
        logger.error(f"Collection not found: {collection_id}")
        raise
    
    except Exception as e:
        logger.error(f"Error creating vector DB for {collection_id}: {str(e)}")
        raise self.retry(exc=e, countdown=120 * (2 ** self.request.retries))


@shared_task
def cleanup_old_documents():
    """Periodic task to cleanup old/unused documents"""
    from datetime import timedelta
    from django.utils import timezone
    
    # Delete failed documents older than 7 days
    threshold_date = timezone.now() - timedelta(days=7)
    deleted_count = Document.objects.filter(
        status='failed',
        uploaded_at__lt=threshold_date
    ).delete()[0]
    
    logger.info(f"Cleaned up {deleted_count} old failed documents")
    return {'deleted_count': deleted_count}