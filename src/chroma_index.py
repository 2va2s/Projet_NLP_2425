import os
from chromadb import Client
from chromadb.config import Settings
from src.config import CHROMA_PERSIST_DIR

def query_index(query: str, collection_name: str, k: int = 5):
    """Query local ChromaDB to retrieve top-k most similar docs."""
    chroma = Client(Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory=CHROMA_PERSIST_DIR
    ))
    col = chroma.get_collection(collection_name)
    results = col.query(
        query_texts=[query],
        n_results=k
    )
    return results["documents"][0]
