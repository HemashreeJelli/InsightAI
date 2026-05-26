import pdfplumber

def extract_text(pdf_path):
    pages = []

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()

            if text:
                pages.append({
                    "page_number": i + 1,
                    "text": text
                })

    return pages