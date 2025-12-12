from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.models.models import User, Evaluation, EvaluationStatus
from app.schemas.schemas import (
    EvaluationCreate, Evaluation as EvaluationSchema,
    EvaluationDetail, EvaluationUpdate, EvaluationResponseCreate,
    EvaluationResponse as EvaluationResponseSchema
)
from app.api.deps import get_current_active_user, require_supervisora
from app.services.evaluation_service import (
    create_evaluation, add_evaluation_response, complete_evaluation,
    get_evaluation_by_id, list_evaluations
)

router = APIRouter()


@router.post("/", response_model=EvaluationSchema, status_code=status.HTTP_201_CREATED)
def create_new_evaluation(
    evaluation_data: EvaluationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_supervisora)
):
    """Create new evaluation (requires Supervisora+ role)."""
    # Verify evaluated user exists
    evaluated_user = db.query(User).filter(User.id == evaluation_data.evaluated_id).first()
    if not evaluated_user:
        raise HTTPException(status_code=404, detail="Evaluated user not found")
    
    evaluation = create_evaluation(evaluation_data, current_user.id, db)
    return evaluation


@router.get("/", response_model=List[EvaluationSchema])
def list_all_evaluations(
    skip: int = 0,
    limit: int = 100,
    status_filter: Optional[EvaluationStatus] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List evaluations (filtered by user role)."""
    # Role-based filtering
    if current_user.role.value == "enfermero":
        # Enfermeros can only see their own evaluations
        evaluations = list_evaluations(
            db, skip=skip, limit=limit,
            evaluated_id=current_user.id, status=status_filter
        )
    elif current_user.role.value in ["supervisora"]:
        # Supervisoras can see evaluations they created
        evaluations = list_evaluations(
            db, skip=skip, limit=limit,
            evaluator_id=current_user.id, status=status_filter
        )
    else:
        # Admin and Jefe can see all
        evaluations = list_evaluations(db, skip=skip, limit=limit, status=status_filter)
    
    return evaluations


@router.get("/{evaluation_id}", response_model=EvaluationDetail)
def get_evaluation(
    evaluation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get evaluation by ID."""
    evaluation = get_evaluation_by_id(evaluation_id, db)
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    
    # Check permissions
    if current_user.role.value == "enfermero":
        if evaluation.evaluated_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized")
    elif current_user.role.value == "supervisora":
        if evaluation.evaluator_id != current_user.id and evaluation.evaluated_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized")
    
    return evaluation


@router.post("/{evaluation_id}/responses", response_model=EvaluationResponseSchema)
def add_response(
    evaluation_id: int,
    response_data: EvaluationResponseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_supervisora)
):
    """Add response to evaluation."""
    evaluation = get_evaluation_by_id(evaluation_id, db)
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    
    # Only evaluator can add responses
    if evaluation.evaluator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    if evaluation.status == EvaluationStatus.COMPLETED:
        raise HTTPException(status_code=400, detail="Evaluation already completed")
    
    response = add_evaluation_response(evaluation_id, response_data, db)
    return response


@router.post("/{evaluation_id}/complete", response_model=EvaluationSchema)
def mark_completed(
    evaluation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_supervisora)
):
    """Mark evaluation as completed."""
    evaluation = get_evaluation_by_id(evaluation_id, db)
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    
    # Only evaluator can complete
    if evaluation.evaluator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    evaluation = complete_evaluation(evaluation_id, db)
    return evaluation


@router.patch("/{evaluation_id}", response_model=EvaluationSchema)
def update_evaluation(
    evaluation_id: int,
    update_data: EvaluationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_supervisora)
):
    """Update evaluation."""
    evaluation = get_evaluation_by_id(evaluation_id, db)
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    
    # Only evaluator can update
    if evaluation.evaluator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    if update_data.status is not None:
        evaluation.status = update_data.status
    if update_data.comments is not None:
        evaluation.comments = update_data.comments
    
    db.commit()
    db.refresh(evaluation)
    return evaluation
