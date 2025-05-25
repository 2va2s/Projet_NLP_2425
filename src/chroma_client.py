import os
import sys
import streamlit as st

import pysqlite3
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

# os.environ["CHROMA_DB_IMPL"] = "duckdb+parquet"

from chromadb import Client
from chromadb.config import Settings

@st.cache_resource
def get_chroma_client():
    return Client(Settings(persist_directory="data/chroma_db"))

client = get_chroma_client()
