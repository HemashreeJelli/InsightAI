from rag.embedder import model, collection
from sentence_transformers import CrossEncoder

# Load Cross-Encoder reranking model ONCE at startup (extremely fast 90MB model)
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def retrieve(query, top_k=5, filenames=None):
    # 1. Generate semantic embedding for the rewritten standalone query
    query_embedding = model.encode(query).tolist()
    
    # --- STEP 6: Print Query Details ---
    print("\n====================")
    print("QUERY:", query)
    if filenames:
        print("FILTERS:", filenames)
    print("====================")

    # 2. Setup dynamic metadata filter for specific documents
    where_clause = None
    if filenames:
        if len(filenames) == 1:
            where_clause = {"filename": filenames[0]}
        else:
            where_clause = {"filename": {"$in": filenames}}

    # 3. Retrieve a larger set of candidates (15 results) for Phase 2 reranking
    candidate_limit = max(top_k * 3, 15)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=candidate_limit,
        include=["documents", "metadatas", "distances"],
        where=where_clause
    )

    candidates = []
    
    # 4. Extract and filter initial candidate chunks from ChromaDB
    if results and results["documents"] and results["documents"][0]:
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for doc, meta, dist in zip(documents, metadatas, distances):
            # Cleanup filter to protect context window from bibliography/metadata noise
            text_lower = doc.lower()
            bad_patterns = [
                "all rights reserved",
                "received",
                "accepted",
                "author contributions",
                "references",
                "funding",
                "acknowledgment",
                "doi.org",
                "@",
            ]
            
            if any(pattern in text_lower for pattern in bad_patterns):
                continue

            candidates.append({
                "text": doc,
                "filename": meta["filename"],
                "page_number": meta["page_number"],
                "distance": dist
            })

    formatted_results = []

    # 5. Phase 2: Compute relevance scores using Cross-Encoder attention
    if candidates:
        # Prepare pairs of (query, document)
        pairs = [[query, c["text"]] for c in candidates]
        
        # Calculate logits scores
        scores = reranker.predict(pairs)
        
        # Attach scores to candidate structures
        for idx, score in enumerate(scores):
            candidates[idx]["score"] = float(score)
            
        # Sort candidates strictly by Cross-Encoder score descending
        candidates.sort(key=lambda x: x["score"], reverse=True)
        
        # Pick the top_k (usually 5) highest scoring chunks
        formatted_results = candidates[:top_k]
        
        # Print debug reranking logs for traceability
        print("\n==================================================")
        print(f"=== RERANKED TOP {len(formatted_results)} CHUNKS ===")
        for idx, c in enumerate(formatted_results):
            print(f"\nRank [{idx+1}] | Rerank Score: {c['score']:.4f} | Chroma Distance: {c['distance']:.4f}")
            print(f"Page: {c['page_number']} | File: {c['filename']}")
            print(c['text'][:180] + "...")
        print("==================================================\n")

    return formatted_results