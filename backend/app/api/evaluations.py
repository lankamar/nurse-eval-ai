from pathlib import Path
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.constants.rubric import ALL_KEYS, ATTITUDE_KEYS, TECHNICAL_KEYS, classify_score
from app.db import get_db
from app.models import Evaluation
from app.schemas.evaluation import EvaluationCreate, EvaluationOut, EvaluationUpdate
from app.services.pdf_generator import generate_pdf

router = APIRouter()

# In-memory storage for MVP scaffold

def _validate_scores(scores: Dict[str, int]):
    missing = [k for k in ALL_KEYS if k not in scores]
    extra = [k for k in scores if k not in ALL_KEYS]
    if missing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Faltan ítems: {', '.join(missing)}")
    if extra:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Ítems desconocidos: {', '.join(extra)}")
    for key, value in scores.items():
        if not isinstance(value, int):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{key} debe ser entero")
        if value < 1 or value > 5:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{key} fuera de rango (1-5)")


def _compute_total(scores: Dict[str, int]) -> tuple[str, str]:
    technical = [scores[k] for k in TECHNICAL_KEYS]
    attitude = [scores[k] for k in ATTITUDE_KEYS]
    ct_avg = sum(technical) / len(technical)
    ca_avg = sum(attitude) / len(attitude)
    total = (ct_avg * 0.6) + (ca_avg * 0.4)
    label = classify_score(total)
    return f"{total:.2f}", label


@router.post("", response_model=EvaluationOut, status_code=status.HTTP_201_CREATED)
async def create_evaluation(payload: EvaluationCreate, db: Session = Depends(get_db)) -> EvaluationOut:
    _validate_scores(payload.scores)
    total, label = _compute_total(payload.scores)

    evaluation = Evaluation(
        evaluator_id=1,  # TODO: replace with auth subject
        evaluatee_id=payload.evaluatee_id,
        status="draft",
        scores=payload.scores,
        total_score=total,
        classification=label,
    )
    db.add(evaluation)
    db.commit()
    db.refresh(evaluation)
    return EvaluationOut(
        id=evaluation.id,
        evaluator_id=evaluation.evaluator_id,
        evaluatee_id=evaluation.evaluatee_id,
        status=evaluation.status,
        scores=evaluation.scores,
        total_score=evaluation.total_score,
        classification=evaluation.classification,
        created_at=evaluation.created_at,
    )


@router.put("/{evaluation_id}", response_model=EvaluationOut)
async def update_evaluation(evaluation_id: int, payload: EvaluationUpdate, db: Session = Depends(get_db)) -> EvaluationOut:
    evaluation = db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()
    if not evaluation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evaluation not found")
    if payload.scores:
        _validate_scores(payload.scores)
        evaluation.scores = payload.scores
        total, label = _compute_total(payload.scores)
        evaluation.total_score = total
        evaluation.classification = label
    if payload.status:
        evaluation.status = payload.status
    db.add(evaluation)
    db.commit()
    db.refresh(evaluation)
    return EvaluationOut(
        id=evaluation.id,
        evaluator_id=evaluation.evaluator_id,
        evaluatee_id=evaluation.evaluatee_id,
        status=evaluation.status,
        scores=evaluation.scores,
        total_score=evaluation.total_score,
        classification=evaluation.classification,
        created_at=evaluation.created_at,
    )


@router.post("/{evaluation_id}/sign")
async def sign_evaluation(evaluation_id: int, db: Session = Depends(get_db)):
    evaluation = db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()
    if not evaluation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evaluation not found")
    pdf_path = generate_pdf(
        evaluation.id,
        evaluation.scores,
        evaluation.total_score or "0",
        evaluation.classification or "Sin clasificar",
        Path("/tmp/pdfs"),
    )
    evaluation.status = "signed"
    db.add(evaluation)
    db.commit()
    db.refresh(evaluation)
    return {
        "pdf": str(pdf_path),
        "status": evaluation.status,
        "total_score": evaluation.total_score,
        "classification": evaluation.classification,
    }
