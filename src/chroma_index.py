from chromadb import Client
from chromadb.config import Settings

client = Client(Settings(
    persist_directory="data/chroma_db",  # tu peux changer ce chemin si besoin
))


def list_documents(collection_name):
    collection = client.get_or_create_collection(collection_name)
    return list(set([m["source"] for m in collection.get()["metadatas"]]))

def delete_document_chunks(collection_name, file_name):
    collection = client.get_collection(collection_name)
    ids_to_delete = [id for id, meta in zip(collection.get()["ids"], collection.get()["metadatas"]) if meta["source"] == file_name]
    collection.delete(ids=ids_to_delete)
