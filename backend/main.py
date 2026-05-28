from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import document, chat
from dotenv import load_dotenv

# Ensure environment variables are loaded
load_dotenv()

app = FastAPI(
    title="InsightAI RAG API",
    description="A high-performance semantic search and conversational RAG API built with FastAPI, ChromaDB, and Groq LLMs.",
    version="1.0.0"
)

# Configure CORS to allow frontend apps (like Next.js, Vite, React, etc.) to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to specific domains in a production deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register application API routers
app.include_router(document.router, prefix="/api")
app.include_router(chat.router, prefix="/api")

@app.get("/")
async def root():
    """
    Root API endpoint providing core system status and docs reference.
    """
    return {
        "message": "Welcome to the InsightAI API",
        "docs_url": "/docs",
        "status": "healthy"
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Launching InsightAI API Server...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
