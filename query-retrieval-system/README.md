# HackRx 6.0: LLM-Powered Intelligent Query–Retrieval System

## 1. Problem Statement

The challenge was to design a high-performance, intelligent system to process large policy documents and answer complex, contextual questions about their content. The system needed to be accurate, fast, efficient, and explainable.

## 2. Our Solution

We have built a complete, asynchronous Retrieval-Augmented Generation (RAG) API using FastAPI. Our system processes PDF documents from a URL, creates a searchable vector index, and can answer multiple natural language questions concurrently.

Our key strategic decision was to build a system that is **entirely free to run** by using a local, open-source LLM, which gives us a massive advantage in cost-efficiency.

## 3. Tech Stack

- **Backend:** FastAPI
- **LLM:** Ollama (running Meta's Llama 3 8B model)
- **Vector Search:** ChromaDB (persistent)
- **Embeddings:** Hugging Face `all-MiniLM-L6-v2` (local)
- **Core Logic:** LangChain

## 4. Key Optimizations & Features

- **Zero Cost (Maximum Token Efficiency):** By using a locally-hosted Ollama model, our API has zero operational cost.
- **High-Speed Concurrent Processing (Low Latency):** The API uses `asyncio` to process all user questions simultaneously.
- **Persistent Knowledge Base:** The system uses ChromaDB to create a persistent, multi-document knowledge base, so document processing is a one-time task.
- **High Explainability:** The API returns the answer, the reasoning, and the specific source chunks from the document used to generate the answer.

## 5. How to Run

1.  Ensure Ollama is installed and running.
2.  Download the required model: `ollama run llama3:8b`
3.  Install Python dependencies from `requirements.txt`.
4.  **Terminal 1:** Run the API server: `uvicorn main:app`
5.  **Terminal 2:** Expose the local server to the internet using `ngrok http 8000` to get the public submission URL.