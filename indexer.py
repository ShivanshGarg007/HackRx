import chromadb
from chromadb.config import Settings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from ingest import extract_text_from_pdfs
from dotenv import load_dotenv
load_dotenv()
import os
print("Gemini API Key from test_env.py:", os.getenv("GEMINI_API_KEY"))

CHROMA_DIR = "chroma_db"

# Initialize ChromaDB client
client = chromadb.Client(Settings(persist_directory=CHROMA_DIR))
collection = client.get_or_create_collection("policy_docs")

def chunk_and_index():
    docs = extract_text_from_pdfs()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    for doc in docs:
        chunks = splitter.split_text(doc["text"])
        for i, chunk in enumerate(chunks):
            metadata = {"filename": doc["filename"], "chunk_id": i}
            collection.add(
                documents=[chunk],
                metadatas=[metadata],
                ids=[f"{doc['filename']}_chunk_{i}"]
            )
    print(f"Indexed {len(docs)} documents into ChromaDB.")

if __name__ == "__main__":
    chunk_and_index() 