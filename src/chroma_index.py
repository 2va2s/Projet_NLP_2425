from openai import OpenAI
from chromadb import PersistentClient
from chromadb.config import Settings, DEFAULT_TENANT, DEFAULT_DATABASE
from src.config import CHROMA_PERSIST_DIR, EMBEDDING_MODEL, OPENAI_API_KEY

# Client OpenAI pour créer les embeddings de la requête
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize ChromaDB once at module load
chroma = PersistentClient(
    path=CHROMA_PERSIST_DIR,               
    settings=Settings(),                    
    tenant=DEFAULT_TENANT,                  
    database=DEFAULT_DATABASE               
)

def query_index(query: str, collection_name: str, k: int = 5):
    """Embed the query with OpenAI (1536D) puis récupérer les k docs les plus proches."""
    # 1. Calculer l'embedding de la requête avec le même modèle
    resp = openai_client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=[query]
    )
    q_embed = resp.data[0].embedding

    # 2. Interroger Chroma avec query_embeddings (et non query_texts)
    col = chroma.get_collection(collection_name)
    results = col.query(
        query_embeddings=[q_embed],
        n_results=k
    )
    # 3. On retourne le premier document trouvé
    return results["documents"][0]