from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
)

def chunk_pages(pages):
    chunks = []

    for page in pages:
        split_texts = splitter.split_text(page["text"])

        for idx, chunk in enumerate(split_texts):
            chunks.append({
                "chunk_text": chunk,
                "page_number": page["page_number"],
                "chunk_index": idx
            })

    return chunks