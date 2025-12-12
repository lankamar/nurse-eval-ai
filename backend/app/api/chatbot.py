from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.models import User
from app.schemas.schemas import ChatRequest, ChatResponse
from app.api.deps import get_current_active_user, require_supervisora
from app.services.chatbot_service import ChatbotService
from app.services.evaluation_service import get_evaluation_by_id

router = APIRouter()


@router.post("/message", response_model=ChatResponse)
def send_message(
    chat_request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_supervisora)
):
    """Send message to chatbot for evaluation."""
    # Verify evaluation exists and user has permission
    evaluation = get_evaluation_by_id(chat_request.evaluation_id, db)
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    
    if evaluation.evaluator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Process message with chatbot
    chatbot = ChatbotService(db)
    response = chatbot.process_message(chat_request.evaluation_id, chat_request.message)
    
    return response


@router.post("/start/{evaluation_id}", response_model=ChatResponse)
def start_conversation(
    evaluation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_supervisora)
):
    """Start evaluation conversation."""
    # Verify evaluation exists and user has permission
    evaluation = get_evaluation_by_id(evaluation_id, db)
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    
    if evaluation.evaluator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Start conversation
    chatbot = ChatbotService(db)
    welcome_message = f"""
    ¡Bienvenido a la Evaluación de Desempeño de Enfermería!
    
    Esta evaluación se basa en el Decreto 366/06 y evalúa 25 competencias:
    - 11 competencias técnicas
    - 14 competencias actitudinales
    
    Evaluando a: {evaluation.evaluated.full_name}
    Período: {evaluation.period}
    
    Comenzaremos con las preguntas. ¿Está listo para iniciar?
    """
    
    response = chatbot.process_message(evaluation_id, "Iniciar evaluación")
    response.message = welcome_message + "\n\n" + response.message
    
    return response
