from datetime import datetime
from typing import Dict
from pydantic import BaseModel, ConfigDict


class EvaluationCreate(BaseModel):
    evaluatee_id: int
    scores: Dict[str, int]


class EvaluationUpdate(BaseModel):
    scores: Dict[str, int]
    status: str | None = None


class EvaluationOut(BaseModel):
    id: int
    evaluator_id: int
    evaluatee_id: int
    status: str
    scores: Dict[str, int]
    total_score: str | None
    classification: str | None = None
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
