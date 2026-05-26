from langchain_text_splitters import RecursiveCharacterTextSplitter
import re

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

def is_good_chunk(text):
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

    # Regex that finds headings like "1. Introduction" even if newlines are missing
    # Looks for a digit, a period, spaces, and an uppercase starting word
    section_pattern = r'(\b\d+\.\s+[A-Z][A-Za-z\s]{3,30}(?=\s))'

    for page in pages:
        page_text = page["text"]
        
        # Split the text by the section headers
        parts = re.split(section_pattern, page_text)
        
        current_section = "Abstract/Introduction"
        
        # If the page doesn't start with a header, the first element is text
        # re.split returns [text_before, heading, text_after, heading, text_after...]
        for item in parts:
            item = item.strip()
            if not item:
                continue
                
            # Check if this item is a section heading match
            if re.match(section_pattern, item):
                current_section = item
            else:
                # This item is the text block inside the current section
                split_texts = splitter.split_text(item)
                
                for idx, chunk in enumerate(split_texts):
                    if is_good_chunk(chunk):
                        chunks.append({
                            "chunk_text": chunk,
                            "page_number": page["page_number"],
                            "chunk_index": idx,
                            "section": current_section  # Inject section tracking metadata!
                        })

    return chunks