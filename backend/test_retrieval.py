# backend/test_retrieval.py
from rag.retriever import retrieve

# Define a question related to whatever your sample.pdf is about
question = "LLM?"

print(f"Searching for: '{question}'...\n")

# Run the retrieval (fetching the top 3 closest matches)
results = retrieve(question, top_k=3)

# Print out the results cleanly
for idx, doc in enumerate(results['documents'][0]):
    print(f"--- Match #{idx + 1} ---")
    print(doc)
    print("\n")