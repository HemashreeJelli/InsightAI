import uuid
import chromadb
from sentence_transformers import SentenceTransformer

# Initialize ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="research_chunks"
)

# Load embedding model ONCE
model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_and_store(chunks, filename):
    # Defensive check: if no good chunks made it through the filters, stop early!
    if not chunks:
        print("[WARNING] No valid chunks passed the quality filters. Skipping storage.")
        return

    documents = []
    embeddings = []
    metadatas = []
    ids = []

    # Keep your batch encoding logic (it's great!)
    chunk_texts = [chunk["chunk_text"] for chunk in chunks]
    encoded_embeddings = model.encode(chunk_texts)

    for i, chunk in enumerate(chunks):
        documents.append(chunk["chunk_text"])
        embeddings.append(encoded_embeddings[i].tolist())

        metadatas.append({
            "filename": filename,
            "page_number": chunk["page_number"],
            "chunk_index": chunk["chunk_index"],
            # FIX: If 'section' is missing for any weird reason, it falls back gracefully
            "section": chunk.get("section", "Abstract/Introduction")
        })

        ids.append(str(uuid.uuid4()))

    collection.add(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )

    print(f"[SUCCESS] Stored {len(chunks)} chunks successfully.")