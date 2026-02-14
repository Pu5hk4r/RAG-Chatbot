#Business logic for processing PDF files and extracting text content
from PyPDF2 import PdfReader
from typing import List, Optional
from pathlib import Path

class PDFProcessor:
    def __init__(self):
        self.chunk_size = 1000
        self.chunk_overlap = 200

    def extract_text(self, Pdf_path: Path) -> List[dict]:
        """ Extract text from PDF with page numbers """
        try:
            reader = PdfReader(Pdf_path)
            documents = []

            for page_num , page in enumerate(reader.pages):
                text = page.extract_text()
                if text and text.strip():
                    documents.append({
                        "content": text,
                        "page": page_num + 1
                    })
            
            return documents
        except Exception as e:
            print(f"Error processing PDF: {e}")
            return []
    
    def chunk_text(self, text:str, page : int)-> List[dict]:
        """ Chunk text into smaller pieces with overlap """
        chunks = []
        start = 0
        text_length = len(text)

        while start < text_length:
            end = start + self.chunk_size
            chunk = text[start:end]
            chunks.append({
                "content": chunk,
                "page": page
            })
            start += self.chunk_size - self.chunk_overlap
        
        return chunks
    
    def process_document(self, pdf_path: Path)-> List[dict]:
        """ Extract and chunk text from PDF document """
        extracted_docs = self.extract_text(pdf_path)
        all_chunks = []

        for doc in extracted_docs:
            chunks = self.chunk_text(doc["content"], doc["page"])
            all_chunks.extend(chunks)
        
        return all_chunks