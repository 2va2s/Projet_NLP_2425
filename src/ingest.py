import os
from openai import OpenAI
from chromadb import Client
from chromadb.config import Settings
from src.config import EMBEDDING_MODEL, CHROMA_PERSIST_DIR

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def embed_and_store(doc_path: str, collection_name: str):
    """Read a text file, compute embeddings and push to ChromaDB."""
    with open(doc_path, "r", encoding="utf-8") as f:
        text = f.read()
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=[text]
    )
    embedding = response["data"][0]["embedding"]

    # Local persistent ChromaDB
    chroma = Client(Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory=CHROMA_PERSIST_DIR
    ))
    col = chroma.get_or_create_collection(collection_name)
    col.add(
        documents=[text],
        embeddings=[embedding],
        ids=[os.path.basename(doc_path)]
    )
