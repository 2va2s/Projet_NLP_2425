import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY    = os.getenv("OPENAI_API_KEY")
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "data/chroma_db")
WHISPER_MODEL_BASE = os.getenv("WHISPER_MODEL_BASE")
EMBEDDING_MODEL    = os.getenv("EMBEDDING_MODEL")
