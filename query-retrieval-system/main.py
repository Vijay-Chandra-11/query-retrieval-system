from fastapi import FastAPI, Depends, HTTPException, status, Header
from pydantic import BaseModel, Field
from typing import List, Optional

from document_processor import download_pdf, extract_text_from_pdf
from rag_core import create_vector_store, get_answers_from_llm

EXPECTED_TOKEN = "8c2123a098ae17e61c519f9c84b0eb4fa35074d106c68f2bc8afc44ab837c0a1"

class QueryRequest(BaseModel):
    documents: str = Field(..., example="https://hackrx.in/policies/BAJHLIP23020V012223.pdf")
    questions: List[str] = Field(..., example=["What is the grace period?"])

class QueryResponse(BaseModel):
    answers: List[str]

app = FastAPI(
    title="Intelligent Query–Retrieval System",
    description="An LLM-powered system to process documents and answer questions using a local Ollama model.",
    version="1.0.0"
)

async def verify_token(authorization: Optional[str] = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header is missing")
    token_type, _, token = authorization.partition(' ')
    if token_type.lower() != 'bearer' or token != EXPECTED_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

@app.post("/hackrx/run", response_model=QueryResponse, summary="Run Submissions")
async def run_submission(request: QueryRequest, _=Depends(verify_token)):
    try:
        # 1. Download document from the web
        pdf_bytes = download_pdf(request.documents)
        # 2. Extract text
        document_text = extract_text_from_pdf(pdf_bytes)
        # 3. Create searchable vector store
        vector_store = create_vector_store(document_text)
        
        # 4. Await the asynchronous function to get all answers concurrently
        final_answers = await get_answers_from_llm(vector_store, request.questions)
        
        return QueryResponse(answers=final_answers)
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {e}")