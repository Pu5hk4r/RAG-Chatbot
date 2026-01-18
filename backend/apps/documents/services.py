# apps/documents/services.py
import os
from typing import List, Tuple
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from django.conf import settings
from .models import Document, DocumentCollection, DocumentChunk
from  pypdf import PdfReader


class DocumentProcessingService:
    """Service for processing PDF documents"""
    
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1024,
            chunk_overlap=64
        )
        self.embeddings = HuggingFaceEmbeddings()
    
    def process_document(self, document: Document) -> None:
        """Process a single document"""
        try:
            document.status = 'processing'
            document.save()
            
            # Extract text and create chunks
            loader = PyPDFLoader(document.file.path)
            pages = loader.load()
            
            # Get page count
            with open(document.file.path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                document.page_count = len(pdf_reader.pages)
            
            # Split into chunks
            doc_splits = self.text_splitter.split_documents(pages)
            
            # Save chunks to database
            for idx, split in enumerate(doc_splits):
                DocumentChunk.objects.create(
                    document=document,
                    content=split.page_content,
                    page_number=split.metadata.get('page', 0) + 1,
                    chunk_index=idx
                )
            
            document.status = 'ready'
            document.save()
            
        except Exception as e:
            document.status = 'failed'
            document.error_message = str(e)
            document.save()
            raise
    
    def create_vector_database(self, collection: DocumentCollection) -> FAISS:
        """Create FAISS vector database for a collection"""
        # Get all ready documents in collection
        documents = collection.documents.filter(status='ready')
        
        if not documents.exists():
            raise ValueError("No ready documents in collection")
        
        # Load all chunks
        all_splits = []
        for doc in documents:
            loader = PyPDFLoader(doc.file.path)
            pages = loader.load()
            splits = self.text_splitter.split_documents(pages)
            all_splits.extend(splits)
        
        # Create vector database
        vectordb = FAISS.from_documents(all_splits, self.embeddings)
        
        # Save to disk
        db_path = os.path.join(settings.MEDIA_ROOT, 'vectordb', str(collection.id))
        os.makedirs(db_path, exist_ok=True)
        vectordb.save_local(db_path)
        
        collection.vector_db_path = db_path
        collection.save()
        
        return vectordb
    
    def load_vector_database(self, collection: DocumentCollection) -> FAISS:
        """Load existing vector database"""
        if not collection.vector_db_path:
            raise ValueError("Vector database not initialized")
        
        vectordb = FAISS.load_local(
            collection.vector_db_path,
            self.embeddings,
            allow_dangerous_deserialization=True
        )
        return vectordb