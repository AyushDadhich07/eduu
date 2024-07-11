def process_pdf(pdf_reader):
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def chunk_text(text, chunk_size=400, overlap=100):
    chunks = []
    start = 0
    end = chunk_size
    
    while start < len(text):
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
        end = start + chunk_size
    
    return chunks