from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pyotp
from sqlalchemy.orm import Session

from app.api import api_router
from app.config import get_settings
from app.db import Base, engine, SessionLocal
from app.models import User
from app.services.encryption import hash_value

app = FastAPI(title="NurseEval AI", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    _seed_demo_user()


def _seed_demo_user():
    settings = get_settings()
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == "demo@hospital.test").first()
        if existing:
            return
        # Use deterministic secrets/codes so the demo user can log in locally
        totp_secret = settings.demo_totp_secret
        backup_codes = settings.demo_backup_codes
        hashed_codes = [hash_value(code) for code in backup_codes]
        demo = User(
            email="demo@hospital.test",
            hashed_password=hash_value("P@ssw0rd!"),
            role="chief",
            totp_secret=totp_secret,
            backup_codes=hashed_codes,
            is_active=True,
        )
        db.add(demo)
        db.commit()
    finally:
        db.close()


@app.get("/health")
async def health():
    return {"status": "ok"}
