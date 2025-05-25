import os
os.environ["CHROMA_DB_IMPL"] = "duckdb+parquet"

from chromadb import Client
from chromadb.config import Settings

client = Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory=None  # Use in-memory DB
))
