
from fastapi import APIRouter, HTTPException, Depends
from app.schema import ChatRequest, ChatResponse
from app.services.vector_store import VectorStore
from app.services.llm_service import LLMService
from app.middleware.auth_middleware import get_current_user

router = APIRouter(
    prefix="/api/chat",
    tags=["chat"]
)

# Service instances
vector_store = VectorStore()
llm_service = LLMService()


@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user)
):
    """Chat with documents"""

    try:
        # 1️ Retrieve relevant chunks
        results = vector_store.search(
            collection_id=request.collection_id,
            query=request.question,
            k=3
        )

        if not results:
            raise HTTPException(status_code=404, detail="No relevant content found")

        # 2️ Generate answer using LLM service
        answer = llm_service.generate_answer(
            question=request.question,
            context_chunks=results
        )

        return ChatResponse(
            answer=answer,
            sources=results
        )

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Collection not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/summarize/{collection_id}")
async def summarize(
    collection_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Summarize entire document"""

    try:
        # Retrieve more chunks for summarization
        results = vector_store.search(
            collection_id=collection_id,
            query="Summarize this document",
            k=5
        )

        if not results:
            raise HTTPException(status_code=404, detail="No content found")

        summary = llm_service.generate_answer(
            question="Summarize this document",
            context_chunks=results
        )

        return {"summary": summary}

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Collection not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
