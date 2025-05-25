import os
import sys

import pysqlite3
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

os.environ["CHROMA_DB_IMPL"] = "duckdb+parquet"

from chromadb import Client
from chromadb.config import Settings

client = Client(Settings(anonymized_telemetry=False))
