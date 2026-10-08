from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Import extraction engine
from analyzer import extract_intelligence

app = FastAPI(
    title="Investigation Intelligence Engine",
    description="Extracts entities, relationships, and graph insights from unstructured investigation notes.",
    version="1.0.0"
)

# ---------------------------------------------------------------------------
# CORS Configuration
# Allows requests from Vite (5173), Next.js / React (3000), or any local dev port
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set to specific origins like ["http://localhost:3000"] in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Pydantic Schemas (Enforces the API Contract)
# ---------------------------------------------------------------------------
class AnalyzeRequest(BaseModel):
    text: str = Field(
        ..., 
        min_length=1, 
        description="Messy case or surveillance text to parse",
        examples=["Rahul met Arjun at Park Street. Arjun transferred ₹50,000 to Vikram."]
    )

class Entity(BaseModel):
    id: str
    name: str
    type: str

class Relationship(BaseModel):
    source: str
    target: str
    type: str

class Insight(BaseModel):
    entity: str
    reason: str

class AnalyzeResponse(BaseModel):
    entities: List[Entity]
    relationships: List[Relationship]
    insights: List[Insight]

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint to verify backend status."""
    return {"status": "ok", "service": "intelligence-engine"}

@app.post(
    "/analyze", 
    response_model=AnalyzeResponse, 
    status_code=status.HTTP_200_OK,
    tags=["Analysis"]
)
async def analyze_text(payload: AnalyzeRequest):
    """
    Accepts raw investigation text, parses entities and relationships,
    and returns graph-ready structured JSON with analytical insights.
    """
    try:
        result = extract_intelligence(payload.text)
        return result
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis pipeline failed: {str(exc)}"
        )