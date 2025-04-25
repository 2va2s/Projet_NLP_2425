import os
from openai import OpenAI
from chromadb import PersistentClient
from chromadb.config import Settings, DEFAULT_TENANT, DEFAULT_DATABASE
from src.config import EMBEDDING_MODEL, CHROMA_PERSIST_DIR, OPENAI_API_KEY
from PyPDF2 import PdfReader
import tiktoken
import re
from typing import List


client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize local persistent ChromaDB client
chroma = PersistentClient(
    path=CHROMA_PERSIST_DIR,
    settings=Settings(),
    tenant=DEFAULT_TENANT,
    database=DEFAULT_DATABASE
)

def extract_text_from_file(path: str) -> str:
    """Extract raw text from TXT or PDF, with encoding fallback."""
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        reader = PdfReader(path)
        # French comment : Extraction de texte page par page
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    else:
        # French comment : Lecture de texte brut avec fallback en cas d’erreur d’encodage
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

def chunk_text(
    text: str,
    max_tokens: int = 500,
    overlap_tokens: int = 50
) -> List[str]:
    """
    Naive sentence-based chunking with token overlap.
    - Split on sentence boundaries via regex.
    - Accumulate sentences until max_tokens, 
      then create a chunk and start the next one
      while keeping `overlap_tokens` lasts tokens.
    """
    tokenizer = tiktoken.get_encoding("cl100k_base")
    # Split on sentence enders (., !, ?)
    sentences = re.split(r'(?<=[\.\!\?])\s+', text.strip())
    chunks: List[List[int]] = []
    current_tokens: List[int] = []

    for sentence in sentences:
        sent_tokens = tokenizer.encode(sentence)
        # Si on dépasserait la limite, on finalise le chunk courant
        if len(current_tokens) + len(sent_tokens) > max_tokens:
            chunks.append(current_tokens)
            # prepare next chunk with overlap
            current_tokens = current_tokens[-overlap_tokens:]
        current_tokens.extend(sent_tokens)

    # Ajouter le dernier chunk s’il reste des tokens
    if current_tokens:
        chunks.append(current_tokens)

    # Décoder chaque chunk en texte
    return [tokenizer.decode(chunk) for chunk in chunks]

def embed_and_store(doc_path: str, collection_name: str):
    """Read a file, split into chunks, compute embeddings per chunk and push to ChromaDB."""
    # 1. Extract full text
    text = extract_text_from_file(doc_path)

    # 2. Chunk the text
    text_chunks = chunk_text(text, max_tokens=500, overlap_tokens=50)

    # Call OpenAI to create embeddings for each chunk
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text_chunks  # one embedding per chunk
    )
    # Extract the embeddings from the response objects
    embeddings = [item.embedding for item in response.data]

    # 4. Store each chunk+embedding in ChromaDB
    col = chroma.get_or_create_collection(collection_name)
    ids = [f"{os.path.basename(doc_path)}_{i}" for i in range(len(text_chunks))]
    col.add(
        documents=text_chunks,
        embeddings=embeddings,
        ids=ids
    )