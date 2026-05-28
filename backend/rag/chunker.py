import re
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1024,
    chunk_overlap=100
)

def is_good_chunk(text):
    """Filters out malformed text, OCR noise, and citation-heavy blocks."""
    if len(text.split()) < 40:
        return False

    citation_count = len(re.findall(r'et al\.', text))
    if citation_count > 5:
        return False

    alnum_ratio = sum(c.isalnum() for c in text) / max(len(text), 1)
    if alnum_ratio < 0.45:
        return False

    return True


def chunk_pages(pages):
    chunks = []

    for page in pages:
        # Blindly split the full page text cleanly
        split_texts = splitter.split_text(page["text"])
        
        for idx, chunk in enumerate(split_texts):
            if is_good_chunk(chunk):
                chunks.append({
                    "chunk_text": chunk,
                    "page_number": page["page_number"],
                    "chunk_index": idx
                    # 'section' metadata has been completely removed!
                })

    return chunks