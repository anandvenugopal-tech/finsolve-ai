import os
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from backend.rabc import get_allowed_permissions
from dotenv import load_dotenv


load_dotenv()

CHROMA_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SYSTEM_PROMPT = """
You are FinSolve AI, a smart internal assistant for FinSolve Technologies.

Your job is to answer employee questions using ONLY the context provided below.
Do not use any outside knowledge.

Rules:
- If the context contains the answer, respond clearly and concisely.
- Always mention which document(s) your answer came from.
- If the context does NOT contains the answer, say exactly: "I don't have that information in your accessible data."
- Never make up numbers, names or facts.

Context: {context}
"""

def format_docs(docs):
    parts = []
    for doc in docs:
        source = doc.metadata.get("source", "unkwown")
        dept = doc.metadata.get('dept', 'unknown')
        chunk = doc.page_content.strip()
        parts.append(f"[Source: {source} | Department: {dept}]\n{chunk}")
    return "\n\n---\n\n".join(parts)

embeddings = HuggingFaceEmbeddings(
        model_name = 'all-MiniLM-L6-v2'
    )

def retrieve_docs(query: str, role: str):
    allowed_collections = get_allowed_permissions(role)
    all_docs = []
    for dept in allowed_collections:
        try:
            vectorstore = Chroma(
                collection_name = f"dept_{dept}",
                embedding_function = embeddings,
                persist_directory=CHROMA_DIR
            )
            retriever = vectorstore.as_retriever(
                search_type = 'similarity',
                search_kwargs = {'k': 3}
            )
            docs = retriever.invoke(query)
            all_docs.extend(docs)
        except Exception as e:
            print(f"Warning: Could not search collection '{dept}': {e}")
            continue
    return all_docs

def build_chain(streaming: bool):
    prompt = ChatPromptTemplate.from_messages([
        ('system', SYSTEM_PROMPT),
        ('human', "{question}")
    ])

    # if ChatGoogleGenerativeAI and GEMINI_API_KEY:
    #     llm = ChatGoogleGenerativeAI(
    #         model="gemini-1.5-flash",
    #         google_api_key=GEMINI_API_KEY,
    #         temperature=0,
    #         convert_system_message_to_human=True,
    #     )
    
    llm = ChatOllama(
        model='llama3.2:1b',
        temperature=0
        )
    return prompt | llm | StrOutputParser()

def get_rag_responce(query: str, role: str) -> dict:
    all_docs = retrieve_docs(query, role)
    
    if not all_docs:
        return {
            "answer": "I don't have any relevant information for your query.",
            "sources": []
        }

    context = format_docs(all_docs)

    source = list({doc.metadata.get("source", "unknown") for doc in all_docs})
    chain = build_chain(streaming = False)

    answer = chain.invoke({
        "context":  context,
        "question": query
    })

    return {
        "answer":  answer,
        "sources": source
    }


