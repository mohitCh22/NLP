import shutil
from pathlib import Path
from langchain_community.vectorstores import FAISS

def create_vectorstore(documents, embeddings):

    vectorstore = FAISS.from_documents(
        documents=documents,
        embedding=embeddings
    )

    return vectorstore


def save_vectorstore(vectorstore, path):
    path = Path(path)
    if path.is_dir():
        shutil.rmtree(path)
    elif path.exists():
        path.unlink()

    vectorstore.save_local(str(path))


def load_vectorstore(path, embeddings):

    vectorstore = FAISS.load_local(
        path,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore

