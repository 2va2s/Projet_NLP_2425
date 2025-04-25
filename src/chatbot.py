from openai import OpenAI
from src.chroma_index import query_index
from src.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_answer(question: str, collection_name: str) -> str:
    """Fetch context from index and ask LLM to generate a helpful answer."""
    context_docs = query_index(question, collection_name)
    prompt = (
        f"You are an internal FAQ assistant.\n"
        f"Context:\n{context_docs}\n"
        f"Question: {question}\n"
        f"Answer:"
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content.strip()
