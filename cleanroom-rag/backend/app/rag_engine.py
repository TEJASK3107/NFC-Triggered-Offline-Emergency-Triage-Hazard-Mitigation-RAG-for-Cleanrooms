import os
from app.config import LANCEDB_URI, TABLE_NAME, EMBED_MODEL, LLM_MODEL
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.lancedb import LanceDBVectorStore
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama

class RAGEngine:
    def __init__(self):
        self.llm = Ollama(
            model=LLM_MODEL, 
            request_timeout=30.0,
            additional_kwargs={"num_ctx": 2048}
        )
        self.embed_model = OllamaEmbedding(model_name=EMBED_MODEL)
        self.index = None
        self.load_index()

    def load_index(self):
        if os.path.exists(LANCEDB_URI) and os.listdir(LANCEDB_URI):
            try:
                vector_store = LanceDBVectorStore(uri=LANCEDB_URI, table_name=TABLE_NAME)
                self.index = VectorStoreIndex.from_vector_store(
                    vector_store=vector_store,
                    embed_model=self.embed_model
                )
                print("[RAG Engine] LanceDB index loaded successfully.")
            except Exception as e:
                print(f"[RAG Engine] Error loading LanceDB: {e}. Defaulting to Mock Mode.")
        else:
            print("[RAG Engine] lancedb_data empty. Running in MOCK mode.")

    def query(self, substance: str, cas: str):
        if not self.index:
            return {
                "action": f"1. Evacuate 10m perimeter immediately for {substance}.\n2. Don Level-A SCBA suit before entering.\n3. Neutralize liquid spill with 5% dilute calcium hypochlorite.",
                "source_page": "ISRO-SOP-PG-MOCK",
                "is_mock": True
            }

        query_str = f"Immediate hazard mitigation steps for {substance} CAS {cas}"
        retriever = self.index.as_retriever(similarity_top_k=2)
        nodes = retriever.retrieve(query_str)

        context = "\n".join([n.node.metadata.get("window", n.node.text) for n in nodes])
        prompt = (
            f"Context from ISRO Handbook:\n{context}\n\n"
            f"Task: Provide 3 direct, numbered emergency response steps for {substance} (CAS {cas}):"
        )

        response = self.llm.complete(prompt)
        page = nodes[0].node.metadata.get("page_label", "ISRO-SOP-PG-42") if nodes else "ISRO-SOP"
        return {"action": str(response), "source_page": page, "is_mock": False}