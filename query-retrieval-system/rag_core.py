import asyncio
from typing import List, Dict
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain_huggingface import HuggingFaceEmbeddings

def create_vector_store(text: str):
    print("Starting vector store creation...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = text_splitter.split_text(text)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = FAISS.from_texts(texts=chunks, embedding=embeddings)
    return vector_store

async def get_answers_from_llm(vector_store, questions: List[str]) -> List[Dict]:
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

    async def get_answer_and_sources(question: str) -> Dict:
        result = await retrieval_chain.ainvoke({"input": question})
        sources = []
        for doc in result.get('context', []):
            sources.append({
                "content": doc.page_content,
                "page": doc.metadata.get('page', 0) + 1 
            })
        return {"answer": result['answer'], "sources": sources}

    tasks = [get_answer_and_sources(q) for q in questions]
    final_results = await asyncio.gather(*tasks)

    print("All answers generated.")
    return final_results