# HackRx 6.0: LLM-Powered Intelligent Query–Retrieval System

## 1. Problem Statement

The challenge was to design a high-performance, intelligent system to process large policy documents and answer complex, contextual questions about their content. The system needed to be accurate, fast, efficient, and explainable.

## 2. Our Solution

We have built a complete, asynchronous, and stateless Retrieval-Augmented Generation (RAG) API using FastAPI. Our system is designed to meet the hackathon's specific requirements, processing a PDF document from a URL and concurrently answering multiple questions in a single API call.

Our key strategic decision was to build a system that is **entirely free to run** by using a local, open-source LLM, which gives us a massive advantage in cost-efficiency and performance.

## 3. Tech Stack

- **Backend:** FastAPI
- **LLM:** Ollama (running Meta's Llama 3 8B model)
- **Vector Search:** ChromaDB (in-memory per-request)
- **Embeddings:** Hugging Face `all-MiniLM-L6-v2` (local)
- **Core Logic:** LangChain

## 4. Key Optimizations & Features

- **Zero Cost (Maximum Token Efficiency):** By using a locally-hosted Ollama model, our API has zero operational cost and is not dependent on external API quotas or billing.
- **High-Speed Concurrent Processing (Low Latency):** The API uses `asyncio` to process all user questions simultaneously, not one-by-one. This dramatically reduces the total response time to meet the < 30s requirement.
- **High Explainability:** The API returns not just an answer, but also the reasoning and the specific source chunks from the document used to generate the answer, providing full traceability.
- **Stateless & Compliant:** The architecture is fully stateless, creating an in-memory index for each request to perfectly match the hackathon's API specification.

## 5. How to Run

1.  Ensure Ollama is installed and running.
2.  Download the required model: `ollama run llama3:8b`
3.  Install Python dependencies from `requirements.txt`.
4.  **Terminal 1:** Run the API server: `uvicorn main:app`
5.  **Terminal 2:** Test the server locally with the provided test script: `python test_api.py`
6.  **Terminal 3 (for Submission):** Expose the local server to the internet using `ngrok http 8000` to get the public webhook URL.