from fastapi import APIRouter, HTTPException

from app.schema import ChatRequest, ChatResponse, Source
from app.services.vector_store import VectorStore
from app.services.llm_service import LLMService

router = APIRouter(prefix="/api", tags=["chat"])

vector_store = VectorStore()
llm_service = LLMService()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        results = vector_store.search(
            request.collection_id,
            request.question,
            k=3
        )

        if not results:
            return ChatResponse(
                answer="I couldn't find relevant information in the documents.",
                sources=[]
            )

        answer = llm_service.generate_answer(request.question, results)

        sources = [
            Source(
                page=r["page"],
                content=r["content"][:200],
                score=r["score"]
            )
            for r in results
        ]

        return ChatResponse(
            answer=answer,
            sources=sources
        )

    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Collection not indexed. Please create index first."
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
