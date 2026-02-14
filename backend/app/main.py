from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import documents, chat, users

app = FastAPI(title="RAG Chatbot API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents.router)
app.include_router(chat.router)
app.include_router(users.router)


@app.get("/")
async def root():
    return {"message": "RAG Chatbot API", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}



