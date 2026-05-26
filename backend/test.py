from services.extractor import extract_text

pages = extract_text("sample.pdf")

print(pages[0])