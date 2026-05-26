from rag.embedder import model, collection


def retrieve(query, top_k=10):

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    formatted_results = []

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    for doc, meta in zip(documents, metadatas):

        formatted_results.append({
            "text": doc,
            "filename": meta["filename"],
            "page_number": meta["page_number"]
        })

    return formatted_results