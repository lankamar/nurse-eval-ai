from datetime import datetime, timedelta

import jwt
import pyotp
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.config import get_settings
from app.db import get_db
from app.models import User
from app.schemas.auth import LoginRequest, RefreshRequest, Token
from app.schemas.user import UserOut
from app.services.encryption import hash_value, verify_value

router = APIRouter()
settings = get_settings()
ALGORITHM = "HS256"


def _create_access_token(subject: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.jwt_expire_minutes)
    to_encode = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, settings.jwt_secret, algorithm=ALGORITHM)


def _create_refresh_token(subject: str) -> str:
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode = {"sub": subject, "exp": expire, "type": "refresh"}
    return jwt.encode(to_encode, settings.jwt_secret, algorithm=ALGORITHM)


def _verify_totp(code: str, secret: str) -> bool:
    totp = pyotp.TOTP(secret, interval=settings.totp_interval, issuer=settings.totp_issuer)
    return totp.verify(code, valid_window=1)


def _consume_backup_code(user: User, code: str, db: Session) -> bool:
    hashed_list = user.backup_codes or []
    for stored in hashed_list:
        if verify_value(code, stored):
            hashed_list.remove(stored)
            user.backup_codes = hashed_list
            db.add(user)
            db.commit()
            return True
    return False


@router.post("/login", response_model=Token)
async def login(payload: LoginRequest, db: Session = Depends(get_db)) -> Token:
    email = payload.email.lower()
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not verify_value(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not payload.code and not payload.backup_code:
        provisioning = pyotp.totp.TOTP(user.totp_secret, interval=settings.totp_interval, issuer=settings.totp_issuer).provisioning_uri(
            name=user.email, issuer_name=settings.totp_issuer
        )
        headers = {"X-TOTP-Secret": user.totp_secret}
        return JSONResponse(
            status_code=status.HTTP_206_PARTIAL_CONTENT,
            content={"detail": "TOTP required", "provisioning_uri": provisioning},
            headers=headers,
        )

    totp_ok = False
    if payload.code:
        totp_ok = _verify_totp(payload.code, user.totp_secret)
    if not totp_ok and payload.backup_code:
        totp_ok = _consume_backup_code(user, payload.backup_code, db)

    if not totp_ok:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid 2FA code")

    access = _create_access_token(str(user.id))
    refresh = _create_refresh_token(str(user.id))
    return Token(access_token=access, refresh_token=refresh)


@router.post("/refresh", response_model=Token)
async def refresh_token(payload: RefreshRequest) -> Token:
    try:
        decoded = jwt.decode(payload.refresh_token, settings.jwt_secret, algorithms=[ALGORITHM])
        if decoded.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        subject = decoded.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access = _create_access_token(subject)
    new_refresh = _create_refresh_token(subject)
    return Token(access_token=access, refresh_token=new_refresh)


@router.get("/me", response_model=UserOut)
async def me(db: Session = Depends(get_db)) -> UserOut:
    # In unprotected demo we return the first user; in production use auth dependency
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserOut(
        id=user.id,
        email=user.email,
        role=user.role,
        is_active=user.is_active,
        created_at=user.created_at or datetime.utcnow(),
    )
