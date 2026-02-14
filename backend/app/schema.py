from pydantic import BaseModel
from typing import List, Optional

class UploadResponse(BaseModel):
    collection_id: str
    filename: str
    page_count :int
    message : str

class IndexRequest(BaseModel):
    collection_id: str
    
class IndexResponse(BaseModel):
    collection_id: str
    status :str
    chunk_count : int

class ChatRequest(BaseModel):
    collection_id: str
    question: str

class Source(BaseModel):
    page : int
    content: str
    score : float

class ChatResponse(BaseModel):
    answer: str
    sources: List[Source]

class CollectionInfo(BaseModel):
    id: str
    name: str
    document_count: int
    indexed: bool






# 1️⃣ Client sends JSON
# {
#   "collection_id": "abc123",
#   "question": "What is FastAPI?"
# }
# 2️⃣ Backend must:

# Understand that JSON
# Validate it
# Convert it into Python object
# Process it
# Send JSON back

# 🔹 Where does schema.py (Pydantic models) help?
# It acts like a:
# 📦 Shape checker + translator
# It says:
# “I expect this JSON to look like THIS structure.”

# 🔁 Full Flow (Simple)
# Client (JSON)
#    ↓
# FastAPI
#    ↓
# Pydantic Model (validates + converts)
#    ↓
# Your Python function
#    ↓
# Return Python object
#    ↓
# Pydantic Model (formats response)
#    ↓
# Client (JSON)


# Schema.py makes it:

# Safe
# Validated
# Structured
# Auto-documented
# Type-checked