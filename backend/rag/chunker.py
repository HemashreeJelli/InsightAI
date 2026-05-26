from langchain_text_splitters import RecursiveCharacterTextSplitter
import re

# Per your previous discussion, changing to 500/100 gives cleaner semantic focus for dense research papers
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

def is_good_chunk(text):
    # Reject tiny chunks
    if len(text.split()) < 40:
        return False

    # Too many citations
    citation_count = len(re.findall(r'et al\.', text))
    if citation_count > 5:
        return False

    # Too many weird symbols
    alnum_ratio = sum(c.isalnum() for c in text) / max(len(text), 1)
    if alnum_ratio < 0.45:
        return False

    return True

def chunk_pages(pages):
    chunks = []
    
    for page in pages:
        split_texts = splitter.split_text(page["text"])
        
        for idx, chunk in enumerate(split_texts):
            # FIX: Only append if it passes your quality check!
            if is_good_chunk(chunk):
                chunks.append({
                    "chunk_text": chunk,
                    "page_number": page["page_number"],
                    "chunk_index": idx
                })
                
    return chunks