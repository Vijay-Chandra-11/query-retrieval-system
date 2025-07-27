from fastapi import FastAPI, Depends, HTTPException, status, Header
from pydantic import BaseModel, Field
from typing import List, Optional

from document_processor import download_pdf, extract_text_from_pdf
from rag_core import create_vector_store, get_answers_from_llm

# --- 1. Create an in-memory cache ---
vector_store_cache = {}

# --- Configuration ---
EXPECTED_TOKEN = "8c2123a098ae17e61c519f9c84b0eb4fa35074d106c68f2bc8afc44ab837c0a1"

# --- Pydantic Models for Richer Output ---
class Source(BaseModel):
    content: str
    page: int

class AnswerWithSources(BaseModel):
    answer: str
    sources: List[Source]

class QueryRequest(BaseModel):
    documents: str = Field(..., example="https://hackrx.in/policies/BAJHLIP23020V012223.pdf")
    questions: List[str] = Field(..., example=["What is the grace period?"])

class QueryResponse(BaseModel):
    answers: List[AnswerWithSources]

# --- FastAPI Application ---
app = FastAPI(
    title="Intelligent Query–Retrieval System",
    description="An LLM-powered system using a local Ollama model with caching and explainability.",
    version="1.2.0"
)

# --- Authentication Dependency ---
async def verify_token(authorization: Optional[str] = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header is missing")
    token_type, _, token = authorization.partition(' ')
    if token_type.lower() != 'bearer' or token != EXPECTED_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

# --- API Endpoint ---
@app.post("/hackrx/run", response_model=QueryResponse, summary="Run Submissions")
async def run_submission(request: QueryRequest, _=Depends(verify_token)):
    doc_url = request.documents
    vector_store = None

    if doc_url in vector_store_cache:
        print("Found vector store in cache. Skipping setup.")
        vector_store = vector_store_cache[doc_url]
    else:
        print("Vector store not in cache. Processing document...")
        try:
            pdf_bytes = download_pdf(doc_url)
            document_text = extract_text_from_pdf(pdf_bytes)
            vector_store = create_vector_store(document_text)
            vector_store_cache[doc_url] = vector_store
        except Exception as e:
            print(f"An error occurred during processing: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to process document: {e}")

    try:
        final_answers = await get_answers_from_llm(vector_store, request.questions)
        return QueryResponse(answers=final_answers)
    except Exception as e:
        print(f"An error occurred during LLM call: {e}")
        raise HTTPException(status_code=500, detail=f"An internal error occurred during generation: {e}")