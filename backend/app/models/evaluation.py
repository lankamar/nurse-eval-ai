from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship

from app.db import Base


class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)
    evaluator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    evaluatee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(50), default="draft")
    scores = Column(JSON, nullable=False, default=dict)
    total_score = Column(String(10), nullable=True)
    classification = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    evaluator = relationship("User", foreign_keys=[evaluator_id])
    evaluatee = relationship("User", foreign_keys=[evaluatee_id])
