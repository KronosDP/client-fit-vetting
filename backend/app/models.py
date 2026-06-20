"""
models.py — SQLAlchemy ORM models.

Defines the four core tables: Client, Candidate, Score, and Feedback.
"""

import enum
from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from .database import Base


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------
class ArchetypeEnum(str, enum.Enum):
    """Client cultural archetype."""
    consulting = "consulting"
    startup = "startup"


class OutcomeEnum(str, enum.Enum):
    """Post-interview outcome."""
    accepted = "accepted"
    rejected = "rejected"


class ReasonEnum(str, enum.Enum):
    """Primary reason for the interview decision."""
    communication_soft_skills = "communication_soft_skills"
    technical_capability = "technical_capability"
    alignment_cultural_vibe = "alignment_cultural_vibe"
    candidate_declined = "candidate_declined"


# ---------------------------------------------------------------------------
# ORM Models
# ---------------------------------------------------------------------------
class Client(Base):
    """A client company profile with archetype and minimum BARS thresholds."""

    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    archetype = Column(Enum(ArchetypeEnum), nullable=False)
    expectations = Column(Text, default="")

    # Minimum acceptable BARS scores per competency (1-5)
    min_communication = Column(Integer, default=3)
    min_adaptability = Column(Integer, default=3)
    min_collaboration = Column(Integer, default=3)
    min_problem_solving = Column(Integer, default=3)
    min_leadership = Column(Integer, default=3)

    created_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    candidates = relationship("Candidate", back_populates="client")


class Candidate(Base):
    """A candidate being evaluated for a specific client."""

    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), default="")
    recruiter_notes = Column(Text, default="")
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    created_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    client = relationship("Client", back_populates="candidates")
    score = relationship(
        "Score", back_populates="candidate", uselist=False
    )
    feedback = relationship(
        "Feedback", back_populates="candidate", uselist=False
    )


class Score(Base):
    """BARS competency scores for a candidate (1-5 per dimension)."""

    __tablename__ = "scores"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(
        Integer, ForeignKey("candidates.id"), unique=True, nullable=False
    )

    communication = Column(Integer, nullable=False)
    adaptability = Column(Integer, nullable=False)
    collaboration = Column(Integer, nullable=False)
    problem_solving = Column(Integer, nullable=False)
    leadership = Column(Integer, nullable=False)

    overall_match = Column(Float, default=0.0)
    mismatches = Column(Text, default="[]")  # JSON-encoded list of strings

    candidate = relationship("Candidate", back_populates="score")


class Feedback(Base):
    """Post-interview outcome and client feedback."""

    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(
        Integer, ForeignKey("candidates.id"), unique=True, nullable=False
    )

    outcome = Column(Enum(OutcomeEnum), nullable=False)
    primary_reason = Column(Enum(ReasonEnum), nullable=False)
    client_notes = Column(Text, default="")
    created_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    candidate = relationship("Candidate", back_populates="feedback")
