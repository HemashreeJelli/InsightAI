import re
from rag.embedder import model, collection

def determine_sections(query: str):
    """
    Maps user search intents directly to the exact classifier targets.
    """
    query_lower = query.lower()
    
    if any(word in query_lower for word in ["method", "approach", "framework", "model", "algorithm", "equation", "loss"]):
        return "methodology"
        
    if any(word in query_lower for word in ["result", "performance", "experiment", "accuracy", "baseline", "table", "dataset", "evaluation"]):
        return "results"
        
    if any(word in query_lower for word in ["summary", "abstract", "overview", "introduction", "conclude", "conclusion", "paper about"]):
        return "summary"
        
    return None


def retrieve(query, top_k=5):
    query_embedding = model.encode(query).tolist()
    target_section = determine_sections(query)
    
    # Simple exact-match metadata filtering
    where_filter = None
    if target_section:
        where_filter = {"section": target_section}

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where=where_filter
    )

    # Fallback to general vector search if strict filter zeroes out
    if not results or not results["documents"] or not results["documents"][0]:
        if where_filter:
            print(f"⚠️ Metadata filter '{target_section}' returned 0 results. Falling back to global search.")
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )

    formatted_results = []
    
    if results and results["documents"] and results["documents"][0]:
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]

        for doc, meta in zip(documents, metadatas):
            formatted_results.append({
                "text": doc,
                "filename": meta["filename"],
                "page_number": meta["page_number"],
                "section": meta.get("section", "Unknown")
            })
    return formatted_results