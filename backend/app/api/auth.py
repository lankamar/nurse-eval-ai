from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
import qrcode
import io
import base64

from app.db.session import get_db
from app.models.models import User
from app.schemas.schemas import Login, Token, UserCreate, User as UserSchema, TwoFactorSetup, TwoFactorVerify
from app.core.security import (
    verify_password, get_password_hash, create_access_token,
    generate_totp_secret, verify_totp, get_totp_uri
)
from app.core.config import settings
from app.api.deps import get_current_active_user

router = APIRouter()


@router.post("/register", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    # Check if user exists
    if db.query(User).filter(User.username == user_in.username).first():
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    if db.query(User).filter(User.email == user_in.email).first():
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Create new user
    db_user = User(
        username=user_in.username,
        email=user_in.email,
        full_name=user_in.full_name,
        role=user_in.role,
        hashed_password=get_password_hash(user_in.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


@router.post("/login", response_model=Token)
def login(login_data: Login, db: Session = Depends(get_db)):
    """Authenticate user and return JWT token."""
    user = db.query(User).filter(User.username == login_data.username).first()
    
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    # Check 2FA
    if user.totp_enabled:
        if not login_data.totp_token:
            return Token(
                access_token="",
                requires_2fa=True
            )
        
        if not verify_totp(user.totp_secret, login_data.totp_token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid 2FA token"
            )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, requires_2fa=False)


@router.post("/2fa/setup", response_model=TwoFactorSetup)
def setup_2fa(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Setup 2FA for current user."""
    if current_user.totp_enabled:
        raise HTTPException(status_code=400, detail="2FA already enabled")
    
    # Generate secret
    secret = generate_totp_secret()
    
    # Generate QR code
    uri = get_totp_uri(secret, current_user.username)
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(uri)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
    qr_code_uri = f"data:image/png;base64,{qr_code_base64}"
    
    # Save secret (not enabled yet)
    current_user.totp_secret = secret
    db.commit()
    
    return TwoFactorSetup(secret=secret, qr_code_uri=qr_code_uri)


@router.post("/2fa/verify")
def verify_2fa(
    verify_data: TwoFactorVerify,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Verify and enable 2FA."""
    if not current_user.totp_secret:
        raise HTTPException(status_code=400, detail="2FA not set up")
    
    if not verify_totp(current_user.totp_secret, verify_data.token):
        raise HTTPException(status_code=400, detail="Invalid token")
    
    # Enable 2FA
    current_user.totp_enabled = True
    db.commit()
    
    return {"message": "2FA enabled successfully"}


@router.post("/2fa/disable")
def disable_2fa(
    verify_data: TwoFactorVerify,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Disable 2FA."""
    if not current_user.totp_enabled:
        raise HTTPException(status_code=400, detail="2FA not enabled")
    
    if not verify_totp(current_user.totp_secret, verify_data.token):
        raise HTTPException(status_code=400, detail="Invalid token")
    
    # Disable 2FA
    current_user.totp_enabled = False
    current_user.totp_secret = None
    db.commit()
    
    return {"message": "2FA disabled successfully"}


@router.get("/me", response_model=UserSchema)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get current user."""
    return current_user
