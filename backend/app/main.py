"""
main.py — FastAPI application entry point.

Exposes the REST API and optionally serves the React frontend build.
"""

from pathlib import Path
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from sqlalchemy.orm import Session

from .brief_generator import generate_brief
from .crud import (
    create_candidate,
    create_client,
    get_candidate,
    get_client,
    get_stats,
    list_candidates,
    list_clients,
    submit_feedback,
    submit_scores,
)
from .database import Base, engine, get_db
from .schemas import (
    CandidateCreate,
    CandidateResponse,
    ClientCreate,
    ClientResponse,
    FeedbackCreate,
    FeedbackResponse,
    ScoreCreate,
    ScoreResponse,
    StatsResponse,
)
from .seed import BARS_ANCHORS, BARS_QUESTIONS, ARCHETYPE_DEFAULTS

# ---------------------------------------------------------------------------
# App initialization
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Staffinc Match — Client-Fit Matching & Briefing Tool",
    version="0.1.0",
    description="MVP for improving client-stage interview acceptance rates.",
)

# CORS — permissive for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    """Create database tables on first run."""
    Base.metadata.create_all(bind=engine)


# ===================================================================
# API Routes
# ===================================================================

# --- Clients -----------------------------------------------------------
@app.post("/api/clients", response_model=ClientResponse, status_code=201)
def api_create_client(data: ClientCreate, db: Session = Depends(get_db)):
    """Create a new client profile with archetype and BARS thresholds."""
    return create_client(db, data)


@app.get("/api/clients", response_model=list[ClientResponse])
def api_list_clients(db: Session = Depends(get_db)):
    """List all client profiles."""
    return list_clients(db)


# --- Candidates --------------------------------------------------------
@app.post("/api/candidates", response_model=CandidateResponse, status_code=201)
def api_create_candidate(data: CandidateCreate, db: Session = Depends(get_db)):
    """Register a candidate for a specific client."""
    client = get_client(db, data.client_id)
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return create_candidate(db, data)


@app.get("/api/candidates", response_model=list[CandidateResponse])
def api_list_candidates(
    client_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    """List candidates, optionally filtered by client_id."""
    return list_candidates(db, client_id=client_id)


@app.get("/api/candidates/{candidate_id}", response_model=CandidateResponse)
def api_get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    """Get detailed candidate info including scores and feedback."""
    candidate = get_candidate(db, candidate_id)
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate


# --- Scores ------------------------------------------------------------
@app.post(
    "/api/candidates/{candidate_id}/scores",
    response_model=ScoreResponse,
    status_code=201,
)
def api_submit_scores(
    candidate_id: int, data: ScoreCreate, db: Session = Depends(get_db)
):
    """Submit BARS scores for a candidate and receive mismatch warnings."""
    candidate = get_candidate(db, candidate_id)
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    try:
        return submit_scores(db, candidate_id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# --- Feedback ----------------------------------------------------------
@app.post(
    "/api/candidates/{candidate_id}/feedback",
    response_model=FeedbackResponse,
    status_code=201,
)
def api_submit_feedback(
    candidate_id: int, data: FeedbackCreate, db: Session = Depends(get_db)
):
    """Record post-interview outcome and client feedback."""
    candidate = get_candidate(db, candidate_id)
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return submit_feedback(db, candidate_id, data)


# --- Brief -------------------------------------------------------------
@app.get("/api/candidates/{candidate_id}/brief")
def api_generate_brief(candidate_id: int, db: Session = Depends(get_db)):
    """Generate a candidate interview preparation brief."""
    candidate = get_candidate(db, candidate_id)
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    if candidate.score is None:
        raise HTTPException(
            status_code=400,
            detail="Candidate has no scores yet. Submit scores first.",
        )
    client = get_client(db, candidate.client_id)
    return generate_brief(candidate, client, candidate.score)


# --- Stats -------------------------------------------------------------
@app.get("/api/stats", response_model=StatsResponse)
def api_get_stats(db: Session = Depends(get_db)):
    """Return dashboard statistics."""
    return get_stats(db)


# --- BARS data ---------------------------------------------------------
@app.get("/api/bars")
def api_get_bars():
    """Return BARS questions, anchors, and archetype defaults."""
    return {
        "questions": BARS_QUESTIONS,
        "anchors": BARS_ANCHORS,
        "archetype_defaults": ARCHETYPE_DEFAULTS,
    }


# --- Health check ------------------------------------------------------
@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Health check endpoint to verify app status and DB connection."""
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database connection failed: {str(e)}",
        )


# ===================================================================
# Static file serving (unified deployment)
# ===================================================================
_frontend_dist = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"
if _frontend_dist.is_dir():
    app.mount("/", StaticFiles(directory=str(_frontend_dist), html=True), name="spa")
