"""
Digital Daemon MVP - Main FastAPI Application
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import logging
import uuid
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from triads.chroma import ChromaTriad
from triads.prismo import PrismoTriad
from triads.anchor import AnchorTriad
from callosum import CorpusCallosum
from soul import Soul
from sleep import SleepPhase
from vector_store import SimpleVectorStore
from slmu import load_slmu_rules
from models import (
    ProcessRequest,
    ProcessResponse,
    SoulResponse,
    HealthResponse,
    SleepResponse
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Digital Daemon MVP",
    version="7.1-mvp",
    description="Simplified triadic cognitive architecture with ethical alignment"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global components (initialized on startup)
vector_store = None
chroma = None
prismo = None
anchor = None
callosum = None
soul = None
sleep_phase = None


@app.on_event("startup")
async def startup_event():
    """Initialize all components on startup."""
    global vector_store, chroma, prismo, anchor, callosum, soul, sleep_phase
    
    logger.info("="*60)
    logger.info("Digital Daemon MVP Starting Up...")
    logger.info("="*60)
    
    try:
        # Load SLMU rules
        logger.info("Loading SLMU rules...")
        slmu_rules = load_slmu_rules("config/slmu_rules.json")
        
        # Initialize vector store
        logger.info("Initializing vector store...")
        vector_store = SimpleVectorStore("data/vectors.npz")
        
        # Initialize triads
        logger.info("Initializing Chroma triad...")
        chroma = ChromaTriad(vector_store)
        
        logger.info("Initializing Prismo triad...")
        prismo = PrismoTriad("data/dd.db", slmu_rules)
        
        logger.info("Initializing Anchor triad...")
        anchor = AnchorTriad("data/interactions.jsonl")
        
        # Initialize integration layer
        logger.info("Initializing Corpus Callosum...")
        callosum = CorpusCallosum()
        
        logger.info("Initializing Soul system...")
        soul = Soul("data")
        
        # Start sleep phase scheduler
        logger.info("Starting Sleep Phase scheduler...")
        sleep_phase = SleepPhase(chroma, prismo, anchor, soul, vector_store)
        sleep_phase.start(interval_hours=6)
        
        logger.info("="*60)
        logger.info("Digital Daemon MVP Ready!")
        logger.info("="*60)
        
    except Exception as e:
        logger.error(f"Failed to initialize components: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Digital Daemon MVP shutting down...")
    if sleep_phase:
        sleep_phase.stop()
    logger.info("Shutdown complete.")


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Digital Daemon MVP",
        "version": "7.1-mvp",
        "description": "Triadic cognitive architecture with ethical alignment",
        "endpoints": {
            "process": "/process",
            "soul": "/soul/{user_id}",
            "health": "/health",
            "sleep": "/sleep/trigger",
            "docs": "/docs"
        }
    }


@app.post("/process", response_model=ProcessResponse, tags=["Core"])
async def process_input(req: ProcessRequest):
    """
    Main processing endpoint: runs all triads + callosum fusion.
    
    This is the core of the Digital Daemon - processes user input through
    all three triads (Chroma, Prismo, Anchor), fuses the results via the
    Callosum, and updates the user's Soul.
    """
    try:
        # Generate session ID if not provided
        session_id = req.session_id or str(uuid.uuid4())
        
        logger.info(f"Processing request for user {req.user_id}")
        logger.debug(f"Input text: {req.text[:100]}...")
        
        # Run triads (synchronous for MVP)
        logger.info("Running Chroma triad...")
        chroma_out = chroma.process(req.text, req.user_id)
        
        logger.info("Running Prismo triad...")
        prismo_out = prismo.process(req.text, req.user_id)
        
        logger.info("Running Anchor triad...")
        anchor_out = anchor.process(req.text, req.user_id, session_id)
        
        # Fusion via Callosum
        logger.info("Fusing triad outputs...")
        fused = callosum.fuse(chroma_out, prismo_out, anchor_out)
        
        if not fused['success']:
            logger.warning(f"Fusion failed: {fused.get('reason')}")
            raise HTTPException(
                status_code=400,
                detail=fused.get('reason', 'Unknown error')
            )
        
        # Update soul
        logger.info("Updating user soul...")
        chroma_vector = np.array(chroma_out['color_vector'])
        updated_soul = soul.update(req.user_id, chroma_vector, fused['coherence'])
        
        logger.info(f"Request processed successfully. Coherence: {fused['coherence']:.3f}")
        
        return ProcessResponse(
            success=True,
            coherence=fused['coherence'],
            response=fused['response'],
            details={
                'sentiment': chroma_out['sentiment'],
                'concepts': prismo_out.get('concepts', []),
                'soul_alignment': updated_soul['alignment_score'],
                'session_id': session_id,
                'similar_memories': len(chroma_out.get('similar_memories', [])),
                'triad_outputs': fused.get('triad_outputs', {})
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Processing error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/soul/{user_id}", response_model=SoulResponse, tags=["Soul"])
async def get_soul(user_id: str):
    """
    Get user's soul state.
    
    Returns the persistent soul data including alignment score,
    interaction count, and ROYGBIV vector representation.
    """
    try:
        user_soul = soul.get_or_create(user_id)
        return SoulResponse(**user_soul)
    except Exception as e:
        logger.error(f"Error retrieving soul: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/soul/{user_id}/stats", tags=["Soul"])
async def get_soul_stats(user_id: str):
    """Get detailed statistics for a user's soul."""
    try:
        user_soul = soul.get_or_create(user_id)
        alignment = soul.get_alignment(user_id)
        vector = soul.get_vector(user_id)
        
        return {
            "user_id": user_id,
            "alignment_score": alignment,
            "interaction_count": user_soul['interaction_count'],
            "vector_magnitude": float(np.linalg.norm(vector)),
            "created_at": user_soul.get('created_at'),
            "last_updated": user_soul.get('last_updated'),
            "preferences": user_soul.get('preferences', {})
        }
    except Exception as e:
        logger.error(f"Error retrieving soul stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/souls/stats", tags=["Soul"])
async def get_all_souls_stats():
    """Get aggregate statistics across all souls."""
    try:
        stats = soul.get_stats()
        return {
            "system_stats": stats,
            "total_users": len(soul.get_all_users())
        }
    except Exception as e:
        logger.error(f"Error retrieving soul stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """
    Health check endpoint.
    
    Returns system status and component counts.
    """
    try:
        concept_count = prismo.get_concept_count() if prismo else 0
        
        return HealthResponse(
            status='healthy',
            vectors=vector_store.count() if vector_store else 0,
            concepts=concept_count,
            souls=len(soul.souls) if soul else 0
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthResponse(
            status='unhealthy',
            vectors=0,
            concepts=0,
            souls=0
        )


@app.get("/sleep/status", tags=["System"])
async def get_sleep_status():
    """Get sleep phase scheduler status."""
    try:
        if not sleep_phase:
            return {"status": "not_initialized"}
        
        status = sleep_phase.get_status()
        return status
    except Exception as e:
        logger.error(f"Error getting sleep status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/sleep/trigger", response_model=SleepResponse, tags=["System"])
async def trigger_sleep():
    """
    Manually trigger sleep phase (for testing).
    
    Runs the sleep cycle immediately regardless of schedule.
    """
    try:
        logger.info("Manual sleep phase trigger requested")
        results = sleep_phase.run_sleep_cycle()
        
        return SleepResponse(
            status='completed' if results.get('success') else 'failed',
            duration_seconds=results.get('duration_seconds'),
            details=results
        )
    except Exception as e:
        logger.error(f"Sleep phase trigger failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/session/{session_id}/history", tags=["History"])
async def get_session_history(session_id: str, limit: int = 10):
    """Get interaction history for a session."""
    try:
        history = anchor.get_session_history(session_id, limit=limit)
        return {
            "session_id": session_id,
            "interaction_count": len(history),
            "history": history
        }
    except Exception as e:
        logger.error(f"Error retrieving session history: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/user/{user_id}/history", tags=["History"])
async def get_user_history(user_id: str, limit: int = 10):
    """Get interaction history for a user."""
    try:
        history = anchor.get_user_history(user_id, limit=limit)
        return {
            "user_id": user_id,
            "interaction_count": len(history),
            "history": history
        }
    except Exception as e:
        logger.error(f"Error retrieving user history: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
