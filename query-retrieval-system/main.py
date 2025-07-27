from fastapi import FastAPI, Depends, HTTPException, status, Header
from pydantic import BaseModel, Field
from typing import List, Dict

# This now imports the final, all-in-one RAG function
from rag_core import process_document_and_get_answers

EXPECTED_TOKEN = "8c2123a098ae17e61c519f9c84b0eb4fa35074d106c68f2bc8afc44ab837c0a1"

# --- Pydantic Models for the Hackathon Spec ---
class QueryRequest(BaseModel):
    documents: str = Field(..., example="https://hackrx.in/policies/BAJHLIP23020V012223.pdf")
    questions: List[str]

class Source(BaseModel):
    content: str
    page: int

class AnswerWithSources(BaseModel):
    answer: str
    reasoning: str
    sources: List[Source]

class QueryResponse(BaseModel):
    answers: List[AnswerWithSources]

app = FastAPI(
    title="Submission-Ready Intelligent Query System",
    description="A compliant API that processes documents and answers questions.",
    version="FINAL"
)

async def verify_token(authorization: str = Header(...)):
    if authorization is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header is missing")
    token_type, _, token = authorization.partition(' ')
    if token_type.lower() != 'bearer' or token != EXPECTED_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

@app.post("/hackrx/run", response_model=QueryResponse, summary="Run Submissions")
async def run_submission(request: QueryRequest, _=Depends(verify_token)):
    """
    This single endpoint performs the entire RAG process as required by the hackathon.
    """
    try:
        final_answers = await process_document_and_get_answers(request.documents, request.questions)
        return QueryResponse(answers=final_answers)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))