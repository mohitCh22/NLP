from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.chatbot.loader import load_documents
from src.chatbot.embeddings import get_embedding_model
from src.chatbot.vectorstore import (
    create_vectorstore,
    save_vectorstore
)

from src.chatbot.config import JSON_PATH, FAISS_PATH

documents = load_documents(JSON_PATH)

embeddings = get_embedding_model()

vectorstore = create_vectorstore(
    documents,
    embeddings
)

save_vectorstore(vectorstore, FAISS_PATH)

print("FAISS index created successfully")