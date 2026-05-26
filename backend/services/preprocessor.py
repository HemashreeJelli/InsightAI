import re


def clean_text(text):

    # Remove excessive newlines
    text = re.sub(r'\n+', '\n', text)

    # Remove weird unicode artifacts
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)

    # Remove repeated spaces
    text = re.sub(r'\s+', ' ', text)

    # Remove citation-like garbage
    text = re.sub(r'\(\w+\s+et al\.,\s+\d{4}\)', '', text)

    # Remove standalone page numbers
    text = re.sub(r'^\d+$', '', text, flags=re.MULTILINE)

    # Remove references section
    if "references" in text.lower():

        text = text.split("References")[0]
    return text.strip()