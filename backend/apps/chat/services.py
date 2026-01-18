 #apps/chat/services.py
from typing import List, Dict, Tuple
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.llms import HuggingFaceEndpoint
from django.conf import settings
from .models import Conversation, Message, SourceReference
from apps.documents.services import DocumentProcessingService
import time


class ChatService:
    """Service for handling chat operations"""
    
    def __init__(self):
        self.doc_service = DocumentProcessingService()
    
    def initialize_llm(
        self,
        model_name: str,
        temperature: float,
        max_tokens: int,
        top_k: int
    ):
        """Initialize LLM with parameters"""
        llm = HuggingFaceEndpoint(
            repo_id=model_name,
            huggingfacehub_api_token=settings.HF_TOKEN,
            temperature=temperature,
            max_new_tokens=max_tokens,
            top_k=top_k,
        )
        return llm
    
    def create_qa_chain(self, conversation: Conversation):
        """Create QA chain for a conversation"""
        # Load vector database
        vectordb = self.doc_service.load_vector_database(conversation.collection)
        
        # Initialize LLM
        llm = self.initialize_llm(
            conversation.llm_model,
            conversation.temperature,
            conversation.max_tokens,
            conversation.top_k
        )
        
        # Create memory
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            output_key='answer',
            return_messages=True
        )
        
        # Load conversation history into memory
        messages = conversation.messages.all()
        for msg in messages:
            if msg.role == 'user':
                memory.chat_memory.add_user_message(msg.content)
            elif msg.role == 'assistant':
                memory.chat_memory.add_ai_message(msg.content)
        
        # Create QA chain
        retriever = vectordb.as_retriever()
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm,
            retriever=retriever,
            chain_type="stuff",
            memory=memory,
            return_source_documents=True,
            verbose=False,
        )
        
        return qa_chain
    
    def process_message(
        self,
        conversation: Conversation,
        user_message: str
    ) -> Tuple[str, List[Dict]]:
        """Process a user message and return response"""
        start_time = time.time()
        
        # Save user message
        user_msg = Message.objects.create(
            conversation=conversation,
            role='user',
            content=user_message
        )
        
        # Create QA chain
        qa_chain = self.create_qa_chain(conversation)
        
        # Format chat history
        chat_history = []
        for msg in conversation.messages.filter(created_at__lt=user_msg.created_at):
            chat_history.append((msg.content, ''))
        
        # Generate response
        response = qa_chain.invoke({
            "question": user_message,
            "chat_history": chat_history
        })
        
        # Extract answer
        response_answer = response["answer"]
        if "Helpful Answer:" in response_answer:
            response_answer = response_answer.split("Helpful Answer:")[-1].strip()
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Save assistant message
        assistant_msg = Message.objects.create(
            conversation=conversation,
            role='assistant',
            content=response_answer,
            processing_time=processing_time
        )
        
        # Save source references
        sources = []
        for idx, source_doc in enumerate(response["source_documents"][:3]):
            source_ref = SourceReference.objects.create(
                message=assistant_msg,
                document=conversation.collection.documents.first(),  # Find matching doc
                chunk_content=source_doc.page_content.strip(),
                page_number=source_doc.metadata.get("page", 0) + 1,
                relevance_score=1.0 - (idx * 0.1)  # Simple relevance scoring
            )
            sources.append({
                'content': source_ref.chunk_content,
                'page': source_ref.page_number,
                'relevance_score': source_ref.relevance_score
            })
        
        # Update conversation timestamp
        conversation.save()
        
        return response_answer, sources
    
    def get_conversation_history(self, conversation: Conversation) -> List[Dict]:
        """Get formatted conversation history"""
        messages = conversation.messages.all()
        history = []
        
        for msg in messages:
            history.append({
                'id': str(msg.id),
                'role': msg.role,
                'content': msg.content,
                'created_at': msg.created_at.isoformat(),
                'sources': [
                    {
                        'content': src.chunk_content,
                        'page': src.page_number,
                        'relevance_score': src.relevance_score
                    }
                    for src in msg.sources.all()
                ] if msg.role == 'assistant' else []
            })
        
        return history