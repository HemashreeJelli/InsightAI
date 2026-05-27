from rag.query_rewriter import rewrite_query
from rag.retriever import retrieve
from rag.generator import generate_answer

chat_history = []

while True:
    user_input = input("\nYou: ")

    if user_input.lower() == "exit":
        break

    # 1. Rewrite follow-up question
    standalone_query = rewrite_query(
        chat_history,
        user_input
    )

    print("\n====================")
    print("ORIGINAL:", user_input)
    print("STANDALONE:", standalone_query)
    print("====================")

    # 2. Retrieve relevant chunks
    retrieved_chunks = retrieve(
        standalone_query,
        top_k=5
    )

    # 3. Generate the core text response
    answer = generate_answer(
        user_input,
        retrieved_chunks,
        chat_history
    )

    # ==============================================================
    # 🎯 IMPLEMENT CITATIONS: Extract and Format Unique Sources
    # ==============================================================
    unique_sources = set()
    for chunk in retrieved_chunks:
        # Create a clean string identifier for each source page
        source_str = f"- {chunk['filename']} (Page {chunk['page_number']})"
        unique_sources.add(source_str)
    
    # Construct the citation markdown block
    sources_text = "\n\n**Sources:**\n" + "\n".join(sorted(unique_sources))
    
    # Append the citations to the final answer string
    final_answer = answer + sources_text

    # 4. Print the final combined answer with citations
    print("\nAssistant:")
    print(final_answer)

    # 5. Save the complete conversation state to memory
    chat_history.append({
        "role": "user",
        "content": user_input
    })
    chat_history.append({
        "role": "assistant",
        "content": final_answer
    })