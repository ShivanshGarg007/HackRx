import os
from PyPDF2 import PdfReader

PDF_DIR = "HackRxHackathon"

def extract_text_from_pdfs(pdf_dir=PDF_DIR):
    documents = []
    for filename in os.listdir(pdf_dir):
        if filename.lower().endswith(".pdf"):
            path = os.path.join(pdf_dir, filename)
            try:
                reader = PdfReader(path)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""
                documents.append({"filename": filename, "text": text})
            except Exception as e:
                print(f"Error reading {filename}: {e}")
    return documents

if __name__ == "__main__":
    docs = extract_text_from_pdfs()
    print(f"Extracted {len(docs)} documents.")
    for doc in docs:
        print(f"{doc['filename']}: {len(doc['text'])} characters") 