"""
Pydantic models for request/response validation.
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, List


class ProcessRequest(BaseModel):
    """Request model for /process endpoint."""
    text: str = Field(..., min_length=1, max_length=5000, description="Input text to process")
    user_id: str = Field(..., min_length=1, max_length=100, description="User identifier")
    session_id: Optional[str] = Field(None, description="Optional session identifier")


class ProcessResponse(BaseModel):
    """Response model for /process endpoint."""
    success: bool
    coherence: float = Field(..., ge=0.0, le=1.0)
    response: str
    details: Dict


class SoulResponse(BaseModel):
    """Response model for /soul endpoint."""
    user_id: str
    vector: List[float]
    alignment_score: float
    interaction_count: int
    preferences: Dict


class HealthResponse(BaseModel):
    """Response model for /health endpoint."""
    status: str
    vectors: int
    concepts: int
    souls: int


class SleepResponse(BaseModel):
    """Response model for /sleep/trigger endpoint."""
    status: str
    duration_seconds: Optional[float] = None
    details: Optional[Dict] = None
