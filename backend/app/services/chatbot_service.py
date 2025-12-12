from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.models.models import Conversation, Evaluation, Criteria, CriteriaType, EvaluationResponse
from app.schemas.schemas import ChatMessage, ChatResponse


class ChatbotService:
    """Conversational chatbot for nurse evaluations per Decreto 366/06."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_or_create_conversation(self, evaluation_id: int) -> Conversation:
        """Get existing conversation or create a new one."""
        conversation = self.db.query(Conversation).filter(
            Conversation.evaluation_id == evaluation_id,
            Conversation.is_active == True
        ).first()
        
        if not conversation:
            conversation = Conversation(
                evaluation_id=evaluation_id,
                messages=[],
                is_active=True
            )
            self.db.add(conversation)
            self.db.commit()
            self.db.refresh(conversation)
        
        return conversation
    
    def get_next_criteria(self, evaluation_id: int) -> Optional[Criteria]:
        """Get next unanswered criteria."""
        # Get all criteria
        all_criteria = self.db.query(Criteria).filter(
            Criteria.is_active == True
        ).order_by(Criteria.order).all()
        
        # Get answered criteria
        answered_criteria_ids = [
            r.criteria_id for r in self.db.query(EvaluationResponse.criteria_id).filter(
                EvaluationResponse.evaluation_id == evaluation_id
            ).all()
        ]
        
        # Find next unanswered
        for criteria in all_criteria:
            if criteria.id not in answered_criteria_ids:
                return criteria
        
        return None
    
    def process_message(self, evaluation_id: int, user_message: str) -> ChatResponse:
        """Process user message and generate response."""
        conversation = self.get_or_create_conversation(evaluation_id)
        
        # Add user message to history
        user_msg = {
            "role": "user",
            "content": user_message,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if not conversation.messages:
            conversation.messages = []
        conversation.messages.append(user_msg)
        
        # Get next criteria to evaluate
        next_criteria = self.get_next_criteria(evaluation_id)
        
        if not next_criteria:
            # All criteria answered
            response_content = "¡Evaluación completada! Todas las competencias han sido evaluadas. ¿Desea revisar alguna respuesta o generar el informe PDF?"
            assistant_msg = {
                "role": "assistant",
                "content": response_content,
                "timestamp": datetime.utcnow().isoformat()
            }
            conversation.messages.append(assistant_msg)
            conversation.is_active = False
            self.db.commit()
            
            return ChatResponse(
                message=response_content,
                is_question=False,
                completed=True
            )
        
        # Generate question for next criteria
        response_content = self._generate_question(next_criteria)
        
        assistant_msg = {
            "role": "assistant",
            "content": response_content,
            "timestamp": datetime.utcnow().isoformat()
        }
        conversation.messages.append(assistant_msg)
        conversation.current_criteria_id = next_criteria.id
        self.db.commit()
        
        return ChatResponse(
            message=response_content,
            is_question=True,
            criteria_code=next_criteria.code,
            completed=False
        )
    
    def _generate_question(self, criteria: Criteria) -> str:
        """Generate conversational question for criteria."""
        tipo = "técnica" if criteria.criteria_type == CriteriaType.TECNICA else "actitudinal"
        
        intro = f"Evaluemos la competencia {tipo}: **{criteria.name}**\n\n"
        description = f"{criteria.description}\n\n"
        question = f"Por favor, evalúe este aspecto en una escala del 1 al {criteria.max_score}, donde:\n"
        question += f"- 1: Necesita mejora significativa\n"
        question += f"- {criteria.max_score}: Excelente desempeño\n\n"
        question += f"¿Qué puntuación otorgaría? Puede agregar comentarios adicionales."
        
        return intro + description + question
    
    def save_response(self, evaluation_id: int, criteria_code: str, score: int, comments: str = None):
        """Save evaluation response."""
        criteria = self.db.query(Criteria).filter(Criteria.code == criteria_code).first()
        if not criteria:
            return None
        
        response = EvaluationResponse(
            evaluation_id=evaluation_id,
            criteria_id=criteria.id,
            score=score,
            comments=comments
        )
        self.db.add(response)
        self.db.commit()
        return response
