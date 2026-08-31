import os
from llama_index.core import SimpleDirectoryReader, StorageContext, VectorStoreIndex
from llama_index.core.node_parser import SentenceWindowNodeParser
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.vector_stores.lancedb import LanceDBVectorStore

def run_ingestion():
    sop_dir = "./data/sops"
    if not os.path.exists(sop_dir) or not os.listdir(sop_dir):
        print(f"[Error] Directory '{sop_dir}' is empty. Add .txt or .pdf manuals first.")
        return

    print("Parsing documents with 3-sentence context window...")
    documents = SimpleDirectoryReader(sop_dir).load_data()

    node_parser = SentenceWindowNodeParser.from_defaults(
        window_size=3,
        window_metadata_key="window",
        original_text_metadata_key="original_sentence"
    )
    nodes = node_parser.get_nodes_from_documents(documents)

    vector_store = LanceDBVectorStore(uri="./lancedb_data", table_name="isro_sops")
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    embed_model = OllamaEmbedding(model_name="nomic-embed-text")

    print("Generating embeddings via nomic-embed-text...")
    VectorStoreIndex(
        nodes,
        storage_context=storage_context,
        embed_model=embed_model,
        show_progress=True
    )
    print("Ingestion complete. LanceDB database populated at ./lancedb_data")

if __name__ == "__main__":
    run_ingestion()