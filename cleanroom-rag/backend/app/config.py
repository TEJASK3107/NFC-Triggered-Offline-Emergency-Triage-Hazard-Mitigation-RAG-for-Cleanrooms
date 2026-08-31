import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANCEDB_URI = os.path.join(BASE_DIR, "lancedb_data")
TABLE_NAME = "isro_sops"
LLM_MODEL = "llama3.1:latest"
EMBED_MODEL = "nomic-embed-text"
HOST_IP = "0.0.0.0"
PORT = 8000