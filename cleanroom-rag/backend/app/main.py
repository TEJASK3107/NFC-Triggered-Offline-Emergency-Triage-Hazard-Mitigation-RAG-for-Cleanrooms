from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.rag_engine import RAGEngine
from app.guardrails import verify_or_fallback

app = FastAPI(title="Cleanroom RAG Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag = RAGEngine()

class NFCPayload(BaseModel):
    station_id: str
    substance: str
    cas: str

@app.get("/health")
async def health_check():
    return {"status": "online", "active_model": "llama3.1:latest"}

@app.post("/api/triage")
async def process_triage(payload: NFCPayload):
    raw_result = rag.query(payload.substance, payload.cas)
    verified_instructions = verify_or_fallback(raw_result["action"], payload.cas)

    return {
        "status": "SUCCESS",
        "station": payload.station_id,
        "substance": payload.substance,
        "cas": payload.cas,
        "instructions": verified_instructions,
        "source": raw_result["source_page"],
        "is_mock": raw_result.get("is_mock", False)
    }