"""
crud.py — Database CRUD operations.
"""

import json

from sqlalchemy import func
from sqlalchemy.orm import Session

from . import models, schemas


# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------
def create_client(db: Session, data: schemas.ClientCreate) -> models.Client:
    """Create a new client profile."""
    client = models.Client(**data.model_dump())
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


def list_clients(db: Session) -> list[models.Client]:
    """Return all client profiles ordered by creation date (newest first)."""
    return db.query(models.Client).order_by(models.Client.created_at.desc()).all()


def get_client(db: Session, client_id: int) -> models.Client | None:
    """Return a single client by ID, or None."""
    return db.query(models.Client).filter(models.Client.id == client_id).first()


# ---------------------------------------------------------------------------
# Candidate
# ---------------------------------------------------------------------------
def create_candidate(db: Session, data: schemas.CandidateCreate) -> models.Candidate:
    """Create a new candidate linked to a client."""
    candidate = models.Candidate(**data.model_dump())
    db.add(candidate)
    db.commit()
    db.refresh(candidate)
    return candidate


def list_candidates(
    db: Session, client_id: int | None = None
) -> list[models.Candidate]:
    """Return candidates, optionally filtered by client_id."""
    query = db.query(models.Candidate)
    if client_id is not None:
        query = query.filter(models.Candidate.client_id == client_id)
    return query.order_by(models.Candidate.created_at.desc()).all()


def get_candidate(db: Session, candidate_id: int) -> models.Candidate | None:
    """Return a single candidate by ID with eager-loaded score and feedback."""
    return (
        db.query(models.Candidate)
        .filter(models.Candidate.id == candidate_id)
        .first()
    )


# ---------------------------------------------------------------------------
# Score (with mismatch detection)
# ---------------------------------------------------------------------------
_COMPETENCY_FIELDS = [
    ("communication", "Communication"),
    ("adaptability", "Adaptability"),
    ("collaboration", "Collaboration"),
    ("problem_solving", "Problem Solving"),
    ("leadership", "Leadership"),
]


def submit_scores(
    db: Session, candidate_id: int, data: schemas.ScoreCreate
) -> models.Score:
    """Score a candidate on the 5 BARS competencies and detect mismatches."""
    candidate = get_candidate(db, candidate_id)
    if candidate is None:
        raise ValueError("Candidate not found")

    client = get_client(db, candidate.client_id)
    if client is None:
        raise ValueError("Client not found")

    # Build mismatch list
    mismatches: list[str] = []
    passing = 0
    total = len(_COMPETENCY_FIELDS)

    for field, label in _COMPETENCY_FIELDS:
        score_val = getattr(data, field)
        min_val = getattr(client, f"min_{field}")
        if score_val >= min_val:
            passing += 1
        else:
            mismatches.append(
                f"{label}: scored {score_val}, minimum required {min_val}"
            )

    overall_match = passing / total if total > 0 else 0.0

    # Check if score already exists for this candidate
    existing = (
        db.query(models.Score)
        .filter(models.Score.candidate_id == candidate_id)
        .first()
    )
    if existing:
        # Update existing score
        for field, _ in _COMPETENCY_FIELDS:
            setattr(existing, field, getattr(data, field))
        existing.overall_match = overall_match
        existing.mismatches = json.dumps(mismatches)
        db.commit()
        db.refresh(existing)
        return existing

    # Create new score
    score = models.Score(
        candidate_id=candidate_id,
        **data.model_dump(),
        overall_match=overall_match,
        mismatches=json.dumps(mismatches),
    )
    db.add(score)
    db.commit()
    db.refresh(score)
    return score


# ---------------------------------------------------------------------------
# Feedback
# ---------------------------------------------------------------------------
def submit_feedback(
    db: Session, candidate_id: int, data: schemas.FeedbackCreate
) -> models.Feedback:
    """Record post-interview feedback for a candidate."""
    # Check if feedback already exists
    existing = (
        db.query(models.Feedback)
        .filter(models.Feedback.candidate_id == candidate_id)
        .first()
    )
    if existing:
        existing.outcome = data.outcome
        existing.primary_reason = data.primary_reason
        existing.client_notes = data.client_notes
        db.commit()
        db.refresh(existing)
        return existing

    feedback = models.Feedback(candidate_id=candidate_id, **data.model_dump())
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return feedback


# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------
def get_stats(db: Session) -> dict:
    """Compute dashboard statistics."""
    total_candidates = db.query(func.count(models.Candidate.id)).scalar() or 0
    total_with_feedback = (
        db.query(func.count(models.Feedback.id)).scalar() or 0
    )
    accepted_count = (
        db.query(func.count(models.Feedback.id))
        .filter(models.Feedback.outcome == "accepted")
        .scalar()
        or 0
    )
    rejected_count = (
        db.query(func.count(models.Feedback.id))
        .filter(models.Feedback.outcome == "rejected")
        .scalar()
        or 0
    )

    acceptance_rate = (
        (accepted_count / total_with_feedback * 100)
        if total_with_feedback > 0
        else 0.0
    )
    feedback_compliance_rate = (
        (total_with_feedback / total_candidates * 100)
        if total_candidates > 0
        else 0.0
    )

    return {
        "total_candidates": total_candidates,
        "total_with_feedback": total_with_feedback,
        "accepted_count": accepted_count,
        "rejected_count": rejected_count,
        "acceptance_rate": round(acceptance_rate, 1),
        "feedback_compliance_rate": round(feedback_compliance_rate, 1),
    }
