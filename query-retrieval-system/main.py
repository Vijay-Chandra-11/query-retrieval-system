# from fastapi import FastAPI, Depends, HTTPException, status, Header
# from pydantic import BaseModel, Field
# from typing import List, Dict

# # Import the new functions from our refactored rag_core
# from rag_core import add_document_to_kb, get_answers_from_kb

# EXPECTED_TOKEN = "8c2123a098ae17e61c519f9c84b0eb4fa35074d106c68f2bc8afc44ab837c0a1"

# # --- Pydantic Models ---
# class UploadRequest(BaseModel):
#     document_url: str = Field(..., example="https://hackrx.in/policies/BAJHLIP23020V012223.pdf")

# class QueryRequest(BaseModel):
#     questions: List[str] = Field(..., example=["What is the grace period?"])

# class QueryResponse(BaseModel):
#     # This structure is designed to be extended with sources if you re-add that feature
#     answers: List[Dict] 

# # --- FastAPI Application ---
# app = FastAPI(
#     title="Multi-Document Knowledge Base API",
#     description="Upload documents and ask questions against a persistent knowledge base.",
#     version="2.0.0"
# )

# # --- Authentication Dependency (This was missing) ---
# async def verify_token(authorization: str = Header(...)):
#     if authorization is None:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header is missing")
#     token_type, _, token = authorization.partition(' ')
#     if token_type.lower() != 'bearer' or token != EXPECTED_TOKEN:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

# # --- NEW: Endpoint for uploading documents (now async) ---
# @app.post("/upload", summary="Upload a document")
# async def upload_document(request: UploadRequest, _=Depends(verify_token)):
#     try:
#         # FastAPI will run this sync function in a background thread
#         add_document_to_kb(request.document_url)
#         return {"message": f"Document from {request.document_url} processed and added successfully."}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# # --- UPDATED: Endpoint for querying the knowledge base ---
# @app.post("/query", response_model=QueryResponse, summary="Query the knowledge base")
# async def query_knowledge_base(request: QueryRequest, _=Depends(verify_token)):
#     try:
#         final_answers = await get_answers_from_kb(request.questions)
#         return QueryResponse(answers=final_answers)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

from fastapi import FastAPI, Depends, HTTPException, status, Header
from pydantic import BaseModel, Field
from typing import List, Dict

from rag_core import add_document_to_kb, get_answers_from_kb

EXPECTED_TOKEN = "8c2123a098ae17e61c519f9c84b0eb4fa35074d106c68f2bc8afc44ab837c0a1"

# --- Pydantic Models for a Rich and Explainable Output ---
class Source(BaseModel):
    content: str
    page: int

class AnswerWithSources(BaseModel):
    answer: str
    reasoning: str
    sources: List[Source]

class UploadRequest(BaseModel):
    document_url: str = Field(..., example="https://hackrx.in/policies/BAJHLIP23020V012223.pdf")

class QueryRequest(BaseModel):
    questions: List[str] = Field(..., example=["What is the grace period?"])

class QueryResponse(BaseModel):
    answers: List[AnswerWithSources]

# --- FastAPI Application ---
app = FastAPI(
    title="Multi-Document Knowledge Base API",
    description="Upload documents and ask questions against a persistent knowledge base.",
    version="2.0.0"
)

# --- Authentication Dependency ---
async def verify_token(authorization: str = Header(...)):
    if authorization is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header is missing")
    token_type, _, token = authorization.partition(' ')
    if token_type.lower() != 'bearer' or token != EXPECTED_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

# --- API Endpoints ---
@app.post("/upload", summary="Upload a document to the knowledge base")
async def upload_document(request: UploadRequest, _=Depends(verify_token)):
    try:
        add_document_to_kb(request.document_url)
        return {"message": f"Document from {request.document_url} processed and added successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse, summary="Query the knowledge base")
async def query_knowledge_base(request: QueryRequest, _=Depends(verify_token)):
    try:
        final_answers = await get_answers_from_kb(request.questions)
        return QueryResponse(answers=final_answers)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))