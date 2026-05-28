from rag.embedder import model, collection

def retrieve(query, top_k=5, filenames=None):  # 🎯 Change: Set top_k back to 5
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

    # 3. Pure semantic search over the collection (optionally filtered)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
        where=where_clause
    )

    formatted_results = []
    
    # 3. Process results and print debugging scores
    if results and results["documents"] and results["documents"][0]:
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        # --- STEP 6: Loop through results, print debug logs, and append ---
        for doc, meta, dist in zip(documents, metadatas, distances):
            
            # Keep your cleanup filter to protect the context window from bibliography trash
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

            print(f"\nDistance: {dist:.4f}")
            print(f"Page: {meta['page_number']}")
            print(doc[:200] + "...") 

            formatted_results.append({
                "text": doc,
                "filename": meta["filename"],
                "page_number": meta["page_number"]
            })

    return formatted_results