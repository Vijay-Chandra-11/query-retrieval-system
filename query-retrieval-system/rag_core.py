import json
import asyncio
from typing import List, Dict
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from document_processor import download_pdf, extract_text_from_pdf

EMBEDDING_FUNCTION = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

async def process_document_and_get_answers(doc_url: str, questions: List[str]) -> List[Dict]:
    """
    A single, stateless function that handles document ingestion and querying.
    """
    print(f"Processing document from {doc_url}...")
    pdf_bytes = download_pdf(doc_url)
    document_text = extract_text_from_pdf(pdf_bytes)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = text_splitter.split_text(document_text)

    # We create a temporary, in-memory vector store for each request.
    vector_store = Chroma.from_texts(texts=chunks, embedding=EMBEDDING_FUNCTION)

    llm = ChatOllama(model="llama3:8b")
    prompt = ChatPromptTemplate.from_template(
        "Based only on the provided context, answer the user's question. Your response must be a JSON object with two keys: 'reasoning' and 'answer'.\n\n"
        "The 'answer' field must be a string that directly answers the question.\n"
        "Do not include any other text, markdown formatting, or explanations outside of the JSON object.\n\n"
        "<context>\n{context}\n</context>\n\n"
        "Question: {input}"
    )

    document_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(vector_store.as_retriever(), document_chain)
    print("RAG chain is ready. Generating all answers concurrently...")

    async def get_structured_answer(question: str) -> Dict:
        result = await retrieval_chain.ainvoke({"input": question})
        sources = []
        for doc in result.get('context', []):
            sources.append({
                "content": doc.page_content,
                "page": doc.metadata.get('page', 0) + 1 
            })
        
        llm_response_text = result['answer']
        try:
            json_start_index = llm_response_text.find('{')
            json_end_index = llm_response_text.rfind('}') + 1
            if json_start_index != -1 and json_end_index != 0:
                json_string = llm_response_text[json_start_index:json_end_index]
                llm_output = json.loads(json_string)
                answer_value = llm_output.get('answer', "No answer found.")
                final_answer = json.dumps(answer_value) if isinstance(answer_value, dict) else str(answer_value)
                reasoning = llm_output.get('reasoning', "No reasoning provided.")
            else:
                raise ValueError("No JSON object found in response.")
        except (json.JSONDecodeError, ValueError):
            final_answer = llm_response_text
            reasoning = "Could not parse structured reasoning from LLM output."
        return {"answer": final_answer, "reasoning": reasoning, "sources": sources}

    tasks = [get_structured_answer(q) for q in questions]
    final_results = await asyncio.gather(*tasks)

    print("All answers generated.")
    return final_results