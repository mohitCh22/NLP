from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import FastAPI
from pydantic import BaseModel

from src.chatbot.embeddings import get_embedding_model

from src.chatbot.vectorstore import load_vectorstore

from src.chatbot.retriever import get_retriever

from src.chatbot.chain import build_chain

from src.chatbot.config import FAISS_INDEX_PATH

app = FastAPI()

# Load everything once during startup

embeddings = get_embedding_model()

vectorstore = load_vectorstore(
    FAISS_INDEX_PATH,
    embeddings
)

retriever = get_retriever(vectorstore)

chain = build_chain(retriever)


class QueryRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {"status": "ok", "message": "CPA Chatbot API is running. POST to /ask with {\"question\": \"...\"}"}


@app.post("/ask")
async def ask_question(request: QueryRequest):

    result = await chain.ainvoke(request.question)

    sources = [
        {
            "section": doc.metadata.get("section"),
            "subsection": doc.metadata.get("subsection"),
            "content_preview": doc.page_content[:300]
        }
        for doc in result["source_documents"]
    ]

    return {
        "question": request.question,
        "answer": result["answer"],
        "sources": sources
    }