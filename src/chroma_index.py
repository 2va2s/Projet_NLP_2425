import os
from chromadb import PersistentClient
from chromadb.config import Settings, DEFAULT_TENANT, DEFAULT_DATABASE
from src.config import CHROMA_PERSIST_DIR

# Initialize ChromaDB once at module load
chroma = PersistentClient(
    path=CHROMA_PERSIST_DIR,               
    settings=Settings(),                    
    tenant=DEFAULT_TENANT,                  
    database=DEFAULT_DATABASE               
)

def query_index(query: str, collection_name: str, k: int = 5):
    """Query local ChromaDB to retrieve top-k most similar docs."""
    col = chroma.get_or_create_collection(collection_name)
    results = col.query(
        query_texts=[query],
        n_results=k
    )
    return results["documents"][0]