STATIC_FALLBACKS = {
    "302-01-2": "CRITICAL HYDRAZINE FALLBACK: Evacuate 10m radius. Don SCBA suit. Flush spill with water for 15 mins.",
    "7664-41-7": "CRITICAL AMMONIA FALLBACK: Evacuate upwind immediately. Apply water spray fog to absorb vapor."
}

def verify_or_fallback(instructions: str, cas: str) -> str:
    if not instructions or len(instructions.strip()) < 15:
        return STATIC_FALLBACKS.get(cas, "EMERGENCY: Evacuate cleanroom bay immediately and alert safety manager.")
    return instructions