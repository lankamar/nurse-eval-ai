from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os

from app.db.session import get_db
from app.models.models import User
from app.schemas.schemas import PDFGenerate, PDFResponse
from app.api.deps import get_current_active_user
from app.services.evaluation_service import get_evaluation_by_id
from app.services.pdf_service import PDFService

router = APIRouter()
pdf_service = PDFService()


@router.post("/generate", response_model=PDFResponse)
def generate_pdf(
    pdf_data: PDFGenerate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Generate PDF report for evaluation."""
    evaluation = get_evaluation_by_id(pdf_data.evaluation_id, db)
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    
    # Check permissions
    if current_user.role.value == "enfermero":
        if evaluation.evaluated_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized")
    elif current_user.role.value == "supervisora":
        if evaluation.evaluator_id != current_user.id and evaluation.evaluated_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized")
    
    # Generate PDF
    result = pdf_service.generate_evaluation_pdf(pdf_data.evaluation_id, db)
    if not result:
        raise HTTPException(status_code=500, detail="Failed to generate PDF")
    
    return PDFResponse(
        pdf_path=result["pdf_path"],
        pdf_hash=result["pdf_hash"]
    )


@router.get("/download/{evaluation_id}")
def download_pdf(
    evaluation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Download PDF report."""
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
    
    if not evaluation.pdf_generated or not evaluation.pdf_path:
        raise HTTPException(status_code=404, detail="PDF not generated yet")
    
    if not os.path.exists(evaluation.pdf_path):
        raise HTTPException(status_code=404, detail="PDF file not found")
    
    filename = os.path.basename(evaluation.pdf_path)
    return FileResponse(
        evaluation.pdf_path,
        media_type="application/pdf",
        filename=filename
    )
