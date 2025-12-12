from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Text, Float, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.session import Base


class RoleEnum(str, enum.Enum):
    """User roles per RBAC requirements."""
    ADMIN = "admin"
    JEFE = "jefe"
    SUPERVISORA = "supervisora"
    ENFERMERO = "enfermero"


class User(Base):
    """User model with 2FA support."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.ENFERMERO, nullable=False)
    
    # 2FA fields
    totp_secret = Column(String(32), nullable=True)
    totp_enabled = Column(Boolean, default=False)
    
    # Account status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    evaluations_created = relationship("Evaluation", back_populates="evaluator", foreign_keys="Evaluation.evaluator_id")
    evaluations_received = relationship("Evaluation", back_populates="evaluated", foreign_keys="Evaluation.evaluated_id")


class CriteriaType(str, enum.Enum):
    """Criteria types per Decreto 366/06."""
    TECNICA = "tecnica"  # Technical - 11 criteria
    ACTITUDINAL = "actitudinal"  # Attitudinal - 14 criteria


class Criteria(Base):
    """Evaluation criteria based on Decreto 366/06."""
    __tablename__ = "criteria"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    criteria_type = Column(Enum(CriteriaType), nullable=False)
    max_score = Column(Integer, default=5, nullable=False)
    order = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    responses = relationship("EvaluationResponse", back_populates="criteria")


class EvaluationStatus(str, enum.Enum):
    """Evaluation status."""
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    APPROVED = "approved"
    REJECTED = "rejected"


class Evaluation(Base):
    """Evaluation instance."""
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)
    evaluator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    evaluated_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    status = Column(Enum(EvaluationStatus), default=EvaluationStatus.DRAFT, nullable=False)
    
    # Scores
    technical_score = Column(Float, nullable=True)
    attitudinal_score = Column(Float, nullable=True)
    total_score = Column(Float, nullable=True)
    
    # Metadata
    period = Column(String(50), nullable=False)  # e.g., "2024-Q1"
    comments = Column(Text, nullable=True)
    
    # Compliance tracking (Ley 25.326)
    consent_given = Column(Boolean, default=False)
    consent_date = Column(DateTime, nullable=True)
    
    # PDF audit trail
    pdf_generated = Column(Boolean, default=False)
    pdf_path = Column(String(500), nullable=True)
    pdf_hash = Column(String(64), nullable=True)  # SHA-256 hash for audit
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    evaluator = relationship("User", back_populates="evaluations_created", foreign_keys=[evaluator_id])
    evaluated = relationship("User", back_populates="evaluations_received", foreign_keys=[evaluated_id])
    responses = relationship("EvaluationResponse", back_populates="evaluation", cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="evaluation", cascade="all, delete-orphan")


class EvaluationResponse(Base):
    """Individual criteria responses."""
    __tablename__ = "evaluation_responses"

    id = Column(Integer, primary_key=True, index=True)
    evaluation_id = Column(Integer, ForeignKey("evaluations.id"), nullable=False)
    criteria_id = Column(Integer, ForeignKey("criteria.id"), nullable=False)
    
    score = Column(Integer, nullable=False)
    comments = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    evaluation = relationship("Evaluation", back_populates="responses")
    criteria = relationship("Criteria", back_populates="responses")


class Conversation(Base):
    """Chatbot conversation for evaluation."""
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    evaluation_id = Column(Integer, ForeignKey("evaluations.id"), nullable=False)
    
    # Conversation data
    messages = Column(JSON, default=list)  # Store conversation history
    current_criteria_id = Column(Integer, ForeignKey("criteria.id"), nullable=True)
    
    # State management
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    evaluation = relationship("Evaluation", back_populates="conversations")


class AuditLog(Base):
    """Audit log for compliance (Ley 25.326 + RENFAMED)."""
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String(100), nullable=False)
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(Integer, nullable=True)
    details = Column(JSON, nullable=True)
    ip_address = Column(String(50), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
