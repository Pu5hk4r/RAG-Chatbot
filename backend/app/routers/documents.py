from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from app.schema import UploadResponse, IndexRequest, IndexResponse
from app.services.pdf_processor import PDFProcessor
from app.services.vector_store import VectorStore
from app.middleware.auth_middleware import get_current_user
from app.config import UPLOAD_FOLDER
import shutil
import uuid
from PyPDF2 import PdfReader

# Create router
router = APIRouter(
    prefix="/api/documents",
    tags=["documents"]
)

# Inject dependencies
pdf_processor = PDFProcessor()
vector_store = VectorStore()

@router.post("/upload", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    collection_name: str = Form(...),
    current_user: dict = Depends(get_current_user)
):
    """Upload PDF document"""
    # ... upload logic here
    pass

@router.post("/create_index", response_model=IndexResponse)
async def create_index(
    request: IndexRequest,
    current_user: dict = Depends(get_current_user)
):
    """Create vector index"""
    # ... indexing logic here
    pass

@router.get("/collections")
async def list_collections(
    current_user: dict = Depends(get_current_user)
):
    """List user's collections"""
    # ... list logic here
    pass