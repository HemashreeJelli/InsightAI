from rag.retriever import retrieve
from rag.generator import generate_answer

question = "What methodology was proposed in the paper?"

retrieved_chunks = retrieve(question)

print("\nRETRIEVED CHUNKS:\n")

for chunk in retrieved_chunks:
    print(chunk)
    print("\n-----------------\n")

answer = generate_answer(
    question,
    retrieved_chunks
)

print("\nANSWER:\n")
print(answer)