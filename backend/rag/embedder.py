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
    documents = []
    embeddings = []
    metadatas = []
    ids = []

    # Batch encode is MUCH faster
    chunk_texts = [chunk["chunk_text"] for chunk in chunks]

    encoded_embeddings = model.encode(chunk_texts)

    for i, chunk in enumerate(chunks):

        documents.append(chunk["chunk_text"])

        embeddings.append(
            encoded_embeddings[i].tolist()
        )

        metadatas.append({
            "filename": filename,
            "page_number": chunk["page_number"],
            "chunk_index": chunk["chunk_index"]
        })

        ids.append(str(uuid.uuid4()))

    collection.add(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )

    print(f"Stored {len(chunks)} chunks.")