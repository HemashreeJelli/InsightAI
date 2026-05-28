import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from typing import List

from services.extractor import extract_text
from rag.chunker import chunk_pages
from rag.embedder import embed_and_store, collection
from models.schemas import UploadResponse, DocumentInfo

router = APIRouter(
    prefix="/documents",
    tags=["documents"]
)

# Robust path setup relative to the root backend folder
UPLOAD_DIR = "uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a research paper PDF, process it, extract text, chunk it,
    and generate semantic embeddings to store in ChromaDB.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF documents are supported."
        )

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        # Save the uploaded file to disk
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 1. Extract text from the PDF pages
        pages = extract_text(file_path)
        if not pages:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Could not extract any text from the uploaded PDF document."
            )

        # 2. Split pages into clean character chunks
        chunks = chunk_pages(pages)
        if not chunks:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="No chunks passed the text quality/filtering criteria."
            )

        # 3. Generate embeddings and load into persistent ChromaDB
        embed_and_store(chunks, file.filename)

        return UploadResponse(
            message="Document uploaded and processed successfully.",
            filename=file.filename,
            pages_processed=len(pages),
            chunks_created=len(chunks)
        )

    except HTTPException as he:
        # Remove bad file if upload/processing failed
        if os.path.exists(file_path):
            os.remove(file_path)
        raise he
    except Exception as e:
        # Cleanup file on generic failure
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during processing: {str(e)}"
        )

@router.get("", response_model=List[DocumentInfo])
async def list_documents():
    """
    List all uploaded and processed PDF documents available in the system.
    """
    documents = []
    if os.path.exists(UPLOAD_DIR):
        for filename in os.listdir(UPLOAD_DIR):
            if filename.endswith(".pdf"):
                file_path = os.path.join(UPLOAD_DIR, filename)
                size_bytes = os.path.getsize(file_path)
                documents.append(
                    DocumentInfo(
                        filename=filename,
                        size_bytes=size_bytes,
                        status="processed"
                    )
                )
    return documents

@router.delete("/{filename}", status_code=status.HTTP_200_OK)
async def delete_document(filename: str):
    """
    Delete a document from disk and purge all its chunk embeddings from ChromaDB.
    """
    if not filename.endswith(".pdf"):
        filename = f"{filename}.pdf"

    file_path = os.path.join(UPLOAD_DIR, filename)
    file_deleted = False

    # 1. Delete from disk
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            file_deleted = True
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete file from storage: {str(e)}"
            )
    
    # 2. Purge from ChromaDB
    try:
        # ChromaDB delete deletes chunks matching the where filter
        collection.delete(where={"filename": filename})
        chunks_purged = True
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to purge chunks from vector database: {str(e)}"
        )

    if not file_deleted:
        # If the file wasn't on disk, check if it was at least in ChromaDB.
        # If not, throw 404
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document '{filename}' not found on server storage."
        )

    return {
        "message": f"Document '{filename}' and all its corresponding vector chunks were successfully deleted.",
        "filename": filename
    }
