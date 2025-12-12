from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from app.models.models import RoleEnum, EvaluationStatus, CriteriaType


# User schemas
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=255)
    role: RoleEnum = RoleEnum.ENFERMERO


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[RoleEnum] = None
    is_active: Optional[bool] = None


class User(UserBase):
    id: int
    is_active: bool
    totp_enabled: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    requires_2fa: bool = False


class TokenData(BaseModel):
    username: Optional[str] = None


class Login(BaseModel):
    username: str
    password: str
    totp_token: Optional[str] = None


class TwoFactorSetup(BaseModel):
    secret: str
    qr_code_uri: str


class TwoFactorVerify(BaseModel):
    token: str


# Criteria schemas
class CriteriaBase(BaseModel):
    code: str
    name: str
    description: str
    criteria_type: CriteriaType
    max_score: int = 5
    order: int


class CriteriaCreate(CriteriaBase):
    pass


class Criteria(CriteriaBase):
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True


# Evaluation Response schemas
class EvaluationResponseBase(BaseModel):
    criteria_id: int
    score: int = Field(..., ge=0, le=5)
    comments: Optional[str] = None


class EvaluationResponseCreate(EvaluationResponseBase):
    pass


class EvaluationResponse(EvaluationResponseBase):
    id: int
    evaluation_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Evaluation schemas
class EvaluationBase(BaseModel):
    evaluated_id: int
    period: str
    comments: Optional[str] = None


class EvaluationCreate(EvaluationBase):
    consent_given: bool = True


class EvaluationUpdate(BaseModel):
    status: Optional[EvaluationStatus] = None
    comments: Optional[str] = None


class Evaluation(EvaluationBase):
    id: int
    evaluator_id: int
    status: EvaluationStatus
    technical_score: Optional[float] = None
    attitudinal_score: Optional[float] = None
    total_score: Optional[float] = None
    pdf_generated: bool
    pdf_path: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class EvaluationDetail(Evaluation):
    evaluator: User
    evaluated: User
    responses: List[EvaluationResponse] = []


# Chatbot schemas
class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ChatRequest(BaseModel):
    evaluation_id: int
    message: str


class ChatResponse(BaseModel):
    message: str
    is_question: bool = False
    criteria_code: Optional[str] = None
    completed: bool = False


# PDF schemas
class PDFGenerate(BaseModel):
    evaluation_id: int


class PDFResponse(BaseModel):
    pdf_path: str
    pdf_hash: str
