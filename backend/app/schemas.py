"""
schemas.py — Pydantic v2 request/response schemas.
"""

import json
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------
class ClientCreate(BaseModel):
    name: str
    archetype: str = Field(..., pattern="^(consulting|startup)$")
    expectations: str = ""
    min_communication: int = Field(3, ge=1, le=5)
    min_adaptability: int = Field(3, ge=1, le=5)
    min_collaboration: int = Field(3, ge=1, le=5)
    min_problem_solving: int = Field(3, ge=1, le=5)
    min_leadership: int = Field(3, ge=1, le=5)


class ClientResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    name: str
    archetype: str
    expectations: str
    min_communication: int
    min_adaptability: int
    min_collaboration: int
    min_problem_solving: int
    min_leadership: int
    created_at: datetime


# ---------------------------------------------------------------------------
# Candidate
# ---------------------------------------------------------------------------
class CandidateCreate(BaseModel):
    name: str
    email: str = ""
    recruiter_notes: str = ""
    client_id: int


class ScoreResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    candidate_id: int
    communication: int
    adaptability: int
    collaboration: int
    problem_solving: int
    leadership: int
    overall_match: float
    mismatches: list[str] = []

    @field_validator("mismatches", mode="before")
    @classmethod
    def parse_mismatches(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v


class FeedbackResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    candidate_id: int
    outcome: str
    primary_reason: str
    client_notes: str
    created_at: datetime


class CandidateResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    name: str
    email: str
    recruiter_notes: str
    client_id: int
    created_at: datetime
    score: Optional[ScoreResponse] = None
    feedback: Optional[FeedbackResponse] = None


# ---------------------------------------------------------------------------
# Score
# ---------------------------------------------------------------------------
class ScoreCreate(BaseModel):
    communication: int = Field(..., ge=1, le=5)
    adaptability: int = Field(..., ge=1, le=5)
    collaboration: int = Field(..., ge=1, le=5)
    problem_solving: int = Field(..., ge=1, le=5)
    leadership: int = Field(..., ge=1, le=5)


# ---------------------------------------------------------------------------
# Feedback
# ---------------------------------------------------------------------------
class FeedbackCreate(BaseModel):
    outcome: str = Field(..., pattern="^(accepted|rejected)$")
    primary_reason: str = Field(
        ...,
        pattern="^(communication_soft_skills|technical_capability|alignment_cultural_vibe|candidate_declined)$",
    )
    client_notes: str = ""


# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------
class StatsResponse(BaseModel):
    total_candidates: int
    total_with_feedback: int
    accepted_count: int
    rejected_count: int
    acceptance_rate: float
    feedback_compliance_rate: float
