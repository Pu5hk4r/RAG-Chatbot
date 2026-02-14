from typing import List, Dict
from app.config import HUGGINGFACE_TOKEN

class LLMService:
    def __init__(self):
        self.api_token = HUGGINGFACE_TOKEN

    def generate_answer(self, question:str, context_chunks: List[dict])-> str:
        """ Generate answer using HuggingFace Inference API """
        # For simplicity, we will just concatenate the context chunks and question
        # In a real implementation, you would call the HuggingFace API here

        context = "\n\n".join([f"[Page {chunk['page']}]: {chunk['content'][:500]}" for chunk in context_chunks])

        #for demo: Simple extraction-based answer
        #in production , HuggingFace APi here

        if not context.strip():
            return "Sorry, I couldn't find relevant information in the document."

        #simple  answer : return most relevent chunk content with page number
        top_chunk = context_chunks[0]
        answer = f"Based on the document, here is the most relevant information:\n\n(Page {top_chunk['page']}) : {top_chunk['content'][:300]}.."

        return answer