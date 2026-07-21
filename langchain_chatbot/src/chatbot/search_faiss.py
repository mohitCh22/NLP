import json
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer

from .config import FAISS_INDEX_PATH, SECTIONS_JSON_PATH

def search_faiss_index(
    query: str,
    metadata_path: str | Path = SECTIONS_JSON_PATH,
    index_path: str | Path = FAISS_INDEX_PATH,
    top_k=4,
):
    with open(metadata_path, "r", encoding="utf-8") as json_file:
        metadata = json.load(json_file)
    index = faiss.read_index(str(index_path))
    model = SentenceTransformer('all-MiniLM-L6-v2')    
    query_embedding = model.encode([query])
    _, I = index.search(query_embedding, k=top_k)
    return [metadata[i] for i in I[0]]