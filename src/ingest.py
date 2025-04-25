import os
from openai import OpenAI
from chromadb import PersistentClient
from chromadb.config import Settings, DEFAULT_TENANT, DEFAULT_DATABASE
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

    # Initialize local persistent ChromaDB with the new client signature
    # Initialize local persistent ChromaDB using the new PersistentClient
    chroma = PersistentClient(
        path=CHROMA_PERSIST_DIR,        # directory where data is stored
        settings=Settings(),            # default settings (no legacy keys)
        teant=DEFAULT_TENANT,          # use default tenant
        database=DEFAULT_DATABASE       # use default database
)
    col = chroma.get_or_create_collection(collection_name)
    col.add(
        documents=[text],
        embeddings=[embedding],
        ids=[os.path.basename(doc_path)]
    )
