import json
from langchain_core.documents import Document

def load_documents(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    documents = []
    for chunk in data:
        # Extract the text text string
        text = chunk.get("text", "")
        
        # Correctly map your exact JSON keys into the metadata dictionary
        metadata = {
            "section": chunk.get("section_number"), # Changed from "section" to "section_number"
            "subsection": chunk.get("subsection"),
            "chunk_id": chunk.get("chunk_id")       # Added tracking for your chunk IDs
        }
        
        # Create the LangChain Document object
        doc = Document(page_content=text, metadata=metadata)
        documents.append(doc)
        
    return documents