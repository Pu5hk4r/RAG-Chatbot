# apps/documents/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .models import DocumentCollection, Document
from .serializers import DocumentCollectionSerializer, DocumentSerializer
from .services import DocumentProcessingService
from .tasks import process_document_task, create_vectordb_task


class DocumentCollectionViewSet(viewsets.ModelViewSet):
    """API endpoint for document collections"""
    serializer_class = DocumentCollectionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return DocumentCollection.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def create_vectordb(self, request, pk=None):
        """Create vector database for collection"""
        collection = self.get_object()
        
        # Check if documents are ready
        ready_docs = collection.documents.filter(status='ready').count()
        if ready_docs == 0:
            return Response(
                {'error': 'No documents ready for processing'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Trigger async task
        create_vectordb_task.delay(str(collection.id))
        
        return Response({
            'message': 'Vector database creation started',
            'collection_id': str(collection.id)
        })
    
    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Get collection statistics"""
        collection = self.get_object()
        
        stats = {
            'total_documents': collection.documents.count(),
            'ready_documents': collection.documents.filter(status='ready').count(),
            'processing_documents': collection.documents.filter(status='processing').count(),
            'failed_documents': collection.documents.filter(status='failed').count(),
            'total_conversations': collection.conversations.count(),
            'total_pages': sum(
                doc.page_count or 0 
                for doc in collection.documents.filter(status='ready')
            )
        }
        
        return Response(stats)


class DocumentViewSet(viewsets.ModelViewSet):
    """API endpoint for documents"""
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Document.objects.filter(
            collection__user=self.request.user
        )
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Upload and process document"""
        collection_id = request.data.get('collection')
        
        try:
            collection = DocumentCollection.objects.get(
                id=collection_id,
                user=request.user
            )
        except DocumentCollection.DoesNotExist:
            return Response(
                {'error': 'Collection not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        file = request.FILES.get('file')
        if not file:
            return Response(
                {'error': 'No file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create document
        document = Document.objects.create(
            collection=collection,
            file=file,
            filename=file.name,
            file_size=file.size,
            status='uploading'
        )
        
        # Trigger async processing
        process_document_task.delay(str(document.id))
        
        serializer = self.get_serializer(document)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def reprocess(self, request, pk=None):
        """Reprocess a failed document"""
        document = self.get_object()
        
        if document.status != 'failed':
            return Response(
                {'error': 'Only failed documents can be reprocessed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        document.status = 'uploading'
        document.error_message = ''
        document.save()
        
        process_document_task.delay(str(document.id))
        
        return Response({'message': 'Document reprocessing started'})