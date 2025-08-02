# HackRx 6.0 GenAI Document Reasoning System

## Overview
This project is an AI-powered system that processes natural language queries and retrieves relevant information from large unstructured documents (PDFs, Word files, emails) using semantic search and LLM-based reasoning. Built for the HackRx 6.0 hackathon.

## Features
- Ingest and index policy documents (PDFs) for semantic search
- Accept natural language queries and extract structured information
- Retrieve relevant clauses using vector search (ChromaDB)
- Use LLMs (Gemini/OpenAI) for decision making and justification
- API endpoints for ingestion and querying

## Setup
1. **Clone the repo and install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Place your policy documents in the `HackRxHackathon/` folder.**

3. **Run the FastAPI server:**
   ```bash
   uvicorn main:app --reload
   ```

## API Endpoints
- `POST /ingest` – Ingest and index all documents in the background
- `POST /query` – Query the indexed documents (JSON: `{ "query": "your question" }`)

## Next Steps
- Integrate LLM for query parsing and decision logic
- Enhance explainability and clause referencing
- Add support for DOCX and email files

---

*Built for HackRx 6.0 – Ideate • Co-create • Impact* 