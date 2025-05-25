import os
from openai import OpenAI
from chromadb import Client
from chromadb.config import Settings
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialisation OpenAI
openai_client = OpenAI(api_key=api_key)
client = Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory=None  # Use in-memory DB
))

def generate_answer(question, collection_name="company_faq"):
    collection = client.get_or_create_collection(collection_name)
    results = collection.query(query_texts=[question], n_results=3)

    if not results["documents"] or not results["documents"][0]:
        return "Je n’ai trouvé aucun document pertinent pour répondre à votre question."

    context = "\n".join(results["documents"][0])
    prompt = f"Réponds à la question suivante en t'appuyant sur les documents :\n{context}\n\nQuestion : {question}"

    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
