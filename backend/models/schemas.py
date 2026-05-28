from pydantic import BaseModel, Field
from typing import List, Optional

# --- Document API Schemas ---

class DocumentInfo(BaseModel):
    filename: str = Field(..., description="The name of the uploaded document file")
    size_bytes: int = Field(..., description="The size of the file in bytes")
    status: str = Field("processed", description="The processing status of the document")

class UploadResponse(BaseModel):
    message: str = Field(..., description="Success or error status message")
    filename: str = Field(..., description="The name of the uploaded and processed file")
    pages_processed: int = Field(..., description="The number of pages extracted from the PDF")
    chunks_created: int = Field(..., description="The number of valid vector chunks stored in ChromaDB")


# --- Chat API Schemas ---

class ChatMessage(BaseModel):
    role: str = Field(..., description="The role of the message author (user or assistant)")
    content: str = Field(..., description="The textual content of the message")

class ChatRequest(BaseModel):
    message: str = Field(..., description="The current user question or query")
    history: List[ChatMessage] = Field(default=[], description="The recent conversation history")
    filenames: Optional[List[str]] = Field(default=None, description="Optional list of document filenames to search within. If omitted, queries all documents.")

class Citation(BaseModel):
    filename: str = Field(..., description="The source document filename")
    page_number: int = Field(..., description="The page number where the context was found")

class ChatResponse(BaseModel):
    answer: str = Field(..., description="The generated textual answer from the LLM model")
    standalone_query: str = Field(..., description="The rewritten standalone version of the query")
    citations: List[Citation] = Field(..., description="Structured citation objects extracted from retrieved context")
