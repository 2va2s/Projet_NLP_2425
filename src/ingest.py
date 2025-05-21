import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from file_utils import extract_text_from_file
from chromadb import Client
from chromadb.config import Settings

client = Client(Settings(persist_directory="data/chroma_db"))

def embed_and_store(file_path, collection_name="company_faq"):
    if not file_path.lower().endswith((".pdf", ".txt")):
        print(f"[IGNORÉ] Format non pris en charge : {file_path}")
        return

    try:
        content = extract_text_from_file(file_path)
    except Exception as e:
        print(f"[ERREUR] Impossible d'extraire le texte de {file_path} : {e}")
        return

    if not content.strip():
        print(f"[IGNORÉ] Document vide ou sans texte : {file_path}")
        return

    collection = client.get_or_create_collection(collection_name)
    file_name = os.path.basename(file_path)

    chunks = [content[i:i+500] for i in range(0, len(content), 500)]

    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            ids=[f"{file_name}_{i}"],
            metadatas=[{"source": file_name}]
        )
