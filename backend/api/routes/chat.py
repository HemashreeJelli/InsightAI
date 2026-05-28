from fastapi import APIRouter, HTTPException, status
from typing import List

from rag.query_rewriter import rewrite_query
from rag.retriever import retrieve
from rag.generator import generate_answer
from models.schemas import ChatRequest, ChatResponse, Citation

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)

@router.post("", response_model=ChatResponse)
async def chat_with_document(request: ChatRequest):
    """
    Stateful conversational QA endpoint. Rewrites queries using chat history,
    performs semantic search on ChromaDB, feeds context into LLM,
    and returns a citation-aware answer.
    """
    try:
        # Convert Pydantic schemas to standard dictionaries for back-compat
        chat_history = [
            {"role": msg.role, "content": msg.content}
            for msg in request.history
        ]

        # 1. Rewrite follow-up question
        standalone_query = rewrite_query(
            chat_history,
            request.message
        )

        # Normalize filenames by appending .pdf if missing (matching ChromaDB metadata)
        filenames = None
        if request.filenames:
            filenames = [
                name if name.lower().endswith(".pdf") else f"{name}.pdf"
                for name in request.filenames
            ]

        # 2. Retrieve relevant chunks from ChromaDB
        try:
            retrieved_chunks = retrieve(
                standalone_query,
                top_k=5,
                filenames=filenames
            )
        except Exception as db_err:
            # If ChromaDB collection doesn't exist yet or failed
            print(f"ChromaDB retrieval error: {db_err}")
            retrieved_chunks = []

        # 3. Generate the answer text via LLM
        if not retrieved_chunks:
            # Fallback when no context exists
            answer = "I couldn't find any relevant context in the uploaded documents to answer your question."
        else:
            answer = generate_answer(
                request.message,
                retrieved_chunks,
                chat_history
            )

        # 4. Extract and format unique source citations
        unique_citations = set()
        citations = []
        for chunk in retrieved_chunks:
            citation_key = (chunk["filename"], chunk["page_number"])
            if citation_key not in unique_citations:
                unique_citations.add(citation_key)
                citations.append(
                    Citation(
                        filename=chunk["filename"],
                        page_number=chunk["page_number"]
                    )
                )

        # Sort citations by page number for clean representation
        citations.sort(key=lambda x: (x.filename, x.page_number))

        return ChatResponse(
            answer=answer,
            standalone_query=standalone_query,
            citations=citations
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during chat generation: {str(e)}"
        )
