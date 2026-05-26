from rag.query_rewriter import rewrite_query
from rag.retriever import retrieve
from rag.generator import generate_answer
# 🎯 Removed: import rerank

chat_history = []

while True:
    user_input = input("\nYou: ")

    if user_input.lower() == "exit":
        break

    # Rewrite follow-up question
    standalone_query = rewrite_query(
        chat_history,
        user_input
    )

    print("\n====================")
    print("ORIGINAL:", user_input)
    print("STANDALONE:", standalone_query)
    print("====================")

    # Retrieve relevant chunks directly (top_k handles the count limits now)
    retrieved_chunks = retrieve(
        standalone_query,
        top_k=5
    )

    # 🎯 Removed: The retrieved_chunks = rerank(...) block
    # 🎯 Removed: The ===== RERANKED RESULTS ===== loop print block

    # Generate final response directly using embedding search outputs
    answer = generate_answer(
        user_input,
        retrieved_chunks,
        chat_history
    )

    print("\nAssistant:")
    print(answer)

    # Save conversation
    chat_history.append({
        "role": "user",
        "content": user_input
    })
    chat_history.append({
        "role": "assistant",
        "content": answer
    })