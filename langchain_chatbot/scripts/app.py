import logging
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import FastAPI

from src.chatbot.logging_config import configure_logging
from src.chatbot.embeddings import get_embedding_model
from src.chatbot.vectorstore import load_vectorstore
from src.chatbot.retriever import get_retriever
from src.chatbot.chain import build_chain
from src.chatbot.config import FAISS_INDEX_PATH

from src.chatbot.rate_limit import limiter
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

from api.routes import router

configure_logging()

logger = logging.getLogger(__name__)

app = FastAPI(title = "CPA RAG API",version="1.0.0")
app.state.limiter = limiter

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
# ---------------------------------------------------------
# Load application resources once
# ---------------------------------------------------------

embeddings = get_embedding_model()

vectorstore = load_vectorstore(
    FAISS_INDEX_PATH,
    embeddings
)

retriever = get_retriever(vectorstore)

chain = build_chain(retriever)

# Store shared application resources
app.state.chain = chain

# Register API routes
app.include_router(router)

@app.get("/")
def root():
    return {"status": "ok", "message": "CPA Chatbot API is running. POST to /ask with {\"question\": \"...\"}"}
