from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import shutil
import uuid
from PyPDF2 import PdfReader

from app.config import UPLOAD_FOLDER
from app.schema import UploadResponse, IndexRequest, IndexResponse
from app.services.pdf_processor import PDFProcessor

from app.services.vector_store import VectorStore

from app.db import collections_db

router = APIRouter(prefix="/api", tags=["documents"])

pdf_processor = PDFProcessor()
vector_store = VectorStore()


@router.post("/upload", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    collection_name: str = Form("Default Collection")
):
    try:
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files allowed")

        collection_id = str(uuid.uuid4())[:8]

        collection_dir = UPLOAD_FOLDER / collection_id
        collection_dir.mkdir(exist_ok=True)

        file_path = collection_dir / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        reader = PdfReader(file_path)
        page_count = len(reader.pages)

        collections_db[collection_id] = {
            "name": collection_name,
            "files": [file.filename],
            "indexed": False
        }

        return UploadResponse(
            collection_id=collection_id,
            filename=file.filename,
            page_count=page_count,
            message="File uploaded successfully"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create_index", response_model=IndexResponse)
async def create_index(request: IndexRequest):
    try:
        collection_id = request.collection_id
        collection_dir = UPLOAD_FOLDER / collection_id

        if not collection_dir.exists():
            raise HTTPException(status_code=404, detail="Collection not found")

        all_chunks = []
        for pdf_file in collection_dir.glob("*.pdf"):
            chunks = pdf_processor.process_document(pdf_file)
            all_chunks.extend(chunks)

        if not all_chunks:
            raise HTTPException(status_code=400, detail="No text extracted")

        chunk_count = vector_store.create_index(all_chunks, collection_id)

        if collection_id in collections_db:
            collections_db[collection_id]["indexed"] = True

        return IndexResponse(
            collection_id=collection_id,
            status="indexed",
            chunk_count=chunk_count
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
