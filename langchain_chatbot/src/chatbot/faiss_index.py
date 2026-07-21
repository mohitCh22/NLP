import json
from pathlib import Path

import faiss
import numpy as np

from sentence_transformers import SentenceTransformer
from .config import FAISS_INDEX_PATH, SECTIONS_JSON_PATH

def build_faiss_index(
    json_file_path: str | Path = SECTIONS_JSON_PATH,
    index_file_path: str | Path = FAISS_INDEX_PATH,
) -> str:
    with open(json_file_path, "r", encoding="utf-8") as json_file:
        lst_cpa_dict = json.load(json_file)
    
    embed_text = [f"{i['section_number']} {i['subsection']} : {i['text']}" for i in lst_cpa_dict]
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(embed_text, convert_to_numpy=True)
    print("This is the shape of embeddings:", embeddings.shape)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(np.array(embeddings, dtype=np.float32))

    index_file_path = Path(index_file_path)
    index_file_path.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(index_file_path))
    print("FAISS index built and saved successfully.")
    return str(index_file_path)
