from services.extractor import extract_text
from rag.chunker import chunk_pages
from rag.embedder import embed_and_store

pages = extract_text("sample.pdf")

chunks = chunk_pages(pages)

embed_and_store(chunks, "sample.pdf")

print("DONE")