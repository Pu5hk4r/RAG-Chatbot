from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import documents, chat, users

# Create app
app = FastAPI(
    title="RAG Chatbot API",
    version="2.0.0",
    description="AI-powered document Q&A system"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(documents.router)
app.include_router(chat.router)
app.include_router(users.router)

# Root endpoints
@app.get("/")
async def root():
    return {
        "message": "RAG Chatbot API",
        "version": "2.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}


