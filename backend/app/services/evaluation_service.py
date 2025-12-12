from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.models.models import Evaluation, EvaluationResponse, Criteria, EvaluationStatus
from app.schemas.schemas import EvaluationCreate, EvaluationResponseCreate


def calculate_scores(evaluation_id: int, db: Session) -> dict:
    """Calculate technical, attitudinal, and total scores for an evaluation."""
    evaluation = db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()
    if not evaluation:
        return None
    
    responses = db.query(EvaluationResponse).filter(
        EvaluationResponse.evaluation_id == evaluation_id
    ).all()
    
    if not responses:
        return {"technical_score": 0, "attitudinal_score": 0, "total_score": 0}
    
    # Get criteria for score calculation
    technical_scores = []
    attitudinal_scores = []
    
    for response in responses:
        criteria = db.query(Criteria).filter(Criteria.id == response.criteria_id).first()
        if criteria:
            score_percentage = (response.score / criteria.max_score) * 100
            if criteria.criteria_type.value == "tecnica":
                technical_scores.append(score_percentage)
            else:
                attitudinal_scores.append(score_percentage)
    
    # Calculate averages
    technical_score = sum(technical_scores) / len(technical_scores) if technical_scores else 0
    attitudinal_score = sum(attitudinal_scores) / len(attitudinal_scores) if attitudinal_scores else 0
    total_score = (technical_score + attitudinal_score) / 2
    
    return {
        "technical_score": round(technical_score, 2),
        "attitudinal_score": round(attitudinal_score, 2),
        "total_score": round(total_score, 2)
    }


def create_evaluation(evaluation_data: EvaluationCreate, evaluator_id: int, db: Session) -> Evaluation:
    """Create a new evaluation."""
    evaluation = Evaluation(
        evaluator_id=evaluator_id,
        evaluated_id=evaluation_data.evaluated_id,
        period=evaluation_data.period,
        comments=evaluation_data.comments,
        consent_given=evaluation_data.consent_given,
        consent_date=datetime.utcnow() if evaluation_data.consent_given else None
    )
    db.add(evaluation)
    db.commit()
    db.refresh(evaluation)
    return evaluation


def add_evaluation_response(
    evaluation_id: int,
    response_data: EvaluationResponseCreate,
    db: Session
) -> EvaluationResponse:
    """Add a response to an evaluation."""
    response = EvaluationResponse(
        evaluation_id=evaluation_id,
        criteria_id=response_data.criteria_id,
        score=response_data.score,
        comments=response_data.comments
    )
    db.add(response)
    db.commit()
    db.refresh(response)
    
    # Recalculate scores
    scores = calculate_scores(evaluation_id, db)
    evaluation = db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()
    if evaluation and scores:
        evaluation.technical_score = scores["technical_score"]
        evaluation.attitudinal_score = scores["attitudinal_score"]
        evaluation.total_score = scores["total_score"]
        db.commit()
    
    return response


def complete_evaluation(evaluation_id: int, db: Session) -> Evaluation:
    """Mark evaluation as completed."""
    evaluation = db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()
    if not evaluation:
        return None
    
    evaluation.status = EvaluationStatus.COMPLETED
    evaluation.completed_at = datetime.utcnow()
    db.commit()
    db.refresh(evaluation)
    return evaluation


def get_evaluation_by_id(evaluation_id: int, db: Session) -> Optional[Evaluation]:
    """Get evaluation by ID."""
    return db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()


def list_evaluations(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    evaluator_id: Optional[int] = None,
    evaluated_id: Optional[int] = None,
    status: Optional[EvaluationStatus] = None
) -> List[Evaluation]:
    """List evaluations with filters."""
    query = db.query(Evaluation)
    
    if evaluator_id:
        query = query.filter(Evaluation.evaluator_id == evaluator_id)
    if evaluated_id:
        query = query.filter(Evaluation.evaluated_id == evaluated_id)
    if status:
        query = query.filter(Evaluation.status == status)
    
    return query.offset(skip).limit(limit).all()
