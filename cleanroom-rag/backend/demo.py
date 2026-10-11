import os
import json
from llama_index.core import StorageContext, VectorStoreIndex, Settings
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.vector_stores.lancedb import LanceDBVectorStore

def get_safety_context_for_nfc(nfc_tag_id: str, user_query: str):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    mapping_path = os.path.join(base_dir, "data", "station_mapping.json")
    db_dir = os.path.join(base_dir, "..", "..", "lancedb_data") # Adjust relative path to root

    # 1. NFC Lookup
    with open(mapping_path, "r", encoding="utf-8") as f:
        mapping = json.load(f)
    
    if nfc_tag_id not in mapping:
        return {"error": f"NFC Tag ID {nfc_tag_id} not found."}
    
    station_info = mapping[nfc_tag_id]

    # 2. Vector DB Query
    embed_model = OllamaEmbedding(model_name="nomic-embed-text")
    Settings.embed_model = embed_model
    Settings.llm = None

    vector_store = LanceDBVectorStore(uri=db_dir, table_name="isro_sops")
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context, embed_model=embed_model)

    query_engine = index.as_query_engine(similarity_top_k=1)
    nodes = query_engine.retrieve(user_query)

    top_node = nodes[0] if nodes else None
    window_text = top_node.node.metadata.get("window", top_node.node.text) if top_node else "No procedure found."

    return {
        "station": station_info,
        "retrieved_window": window_text
    }