# In rag_core.py
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from typing import List
from langchain_community.chat_models import ChatOllama
from langchain_huggingface import HuggingFaceEmbeddings
import asyncio # Import asyncio

def create_vector_store(text: str):
    # This function does not change
    print("Starting vector store creation...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = text_splitter.split_text(text)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = FAISS.from_texts(texts=chunks, embedding=embeddings)
    return vector_store

async def get_answers_from_llm(vector_store, questions: List[str]) -> List[str]:
    # This function is now an async function
    print("Setting up the RAG chain with local Ollama...")
    llm = ChatOllama(model="llama3:8b")

    prompt = ChatPromptTemplate.from_template(
        "Answer the following question based only on the provided context.\n\n"
        "If the answer is not in the context, say \"The answer is not available in the provided document.\"\n\n"
        "<context>\n{context}\n</context>\n\n"
        "Question: {input}"
    )

    document_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(vector_store.as_retriever(), document_chain)

    print("RAG chain is ready. Generating all answers concurrently...")
    
    # Create a list of asynchronous tasks
    tasks = [retrieval_chain.ainvoke({"input": q}) for q in questions]
    
    # Run all tasks at the same time
    results = await asyncio.gather(*tasks)
    
    # Extract the 'answer' from each result dictionary
    final_answers = [res['answer'] for res in results]

    print("All answers generated.")
    return final_answers