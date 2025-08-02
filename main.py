from fastapi import FastAPI
from fastapi import BackgroundTasks
import indexer
from pydantic import BaseModel
import llm_utils
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb
from chromadb.config import Settings

CHROMA_DIR = "chroma_db"

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "HackRx 6.0 GenAI Document Reasoning System is running!"}

# Placeholder for /ingest and /query endpoints
# Implementation will follow after setting up document ingestion and indexing 

@app.post("/ingest")
def ingest_documents(background_tasks: BackgroundTasks):
    background_tasks.add_task(indexer.chunk_and_index)
    return {"message": "Document ingestion and indexing started in background."} 

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
def query_documents(request: QueryRequest):
    try:
        # Step 1: Parse query into structured info using LLM
        print("Parsing query with LLM...")
        parsed = llm_utils.parse_query_with_llm(request.query)
        print("Parsed query:", parsed)

        # Step 2: Semantic retrieval from ChromaDB
        client = chromadb.Client(Settings(persist_directory=CHROMA_DIR))
        collection = client.get_or_create_collection("policy_docs")
        # Use the raw query for embedding search
        results = collection.query(query_texts=[request.query], n_results=5)
        retrieved_chunks = [doc for doc in results["documents"][0]]
        metadatas = results["metadatas"][0]

        # Step 3: Pass query and retrieved content to LLM for reasoning
        context = "\n---\n".join(retrieved_chunks)
        llm_prompt = f"""
        Given the following insurance policy clauses and the user query, answer the query as an insurance expert. Reference the relevant clauses in your justification.
        
        User Query: {request.query}
        
        Policy Clauses:
        {context}
        
        Respond in JSON with keys: decision (approved/rejected), amount (if any), justification, and clauses (list of referenced clause summaries).
        """
        # Use Gemini or OpenAI for final reasoning
        final_response = llm_utils.parse_query_with_llm(llm_prompt)
        return {
            "parsed_query": parsed,
            "retrieved_clauses": retrieved_chunks,
            "metadatas": metadatas,
            "llm_response": final_response
        }
    except Exception as e:
        import traceback
        print("Exception in /query endpoint:", e)
        traceback.print_exc()
        return {"error": str(e)} 