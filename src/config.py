import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)

LLM_NAME = os.getenv("LLM_NAME")
LLM_HOST = os.getenv("LLM_HOST")
VECTOR_DB_HOST = os.getenv("QDRANT_URL")
COLLECT_NAME = os.getenv("COLLECT_NAME")
