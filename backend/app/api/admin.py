import csv
import io
import secrets
from typing import List

import pyotp
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import User
from app.services.encryption import hash_value

router = APIRouter()


def _generate_backup_codes(count: int) -> List[str]:
    return [f"BACKUP-CODE-{i}-{secrets.token_hex(2)}" for i in range(1, count + 1)]


@router.post("/import-staff")
async def import_staff(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(('.csv', '.txt')):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Solo se aceptan CSV")

    content = await file.read()
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        text = content.decode("latin-1")
    reader = csv.DictReader(io.StringIO(text))
    required = {"email", "role"}
    if not required.issubset(set(reader.fieldnames or [])):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="CSV debe tener columnas email, role")

    created = 0
    skipped = 0
    provisioned = []
    for row in reader:
        email = (row.get("email") or "").strip().lower()
        role = (row.get("role") or "nurse").strip().lower() or "nurse"
        if not email:
            continue
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            skipped += 1
            continue
        totp_secret = pyotp.random_base32()
        backup_raw = _generate_backup_codes(10)
        backup_hashed = [hash_value(code) for code in backup_raw]
        temp_password = f"Temp-{secrets.token_hex(3)}!"
        user = User(
            email=email,
            role=role,
            hashed_password=hash_value(temp_password),
            totp_secret=totp_secret,
            backup_codes=backup_hashed,
            is_active=True,
        )
        db.add(user)
        created += 1
        provisioned.append({"email": email, "role": role, "temp_password": temp_password, "totp_secret": totp_secret, "backup_codes": backup_raw})
    db.commit()
    return {"created": created, "skipped": skipped, "provisioned": provisioned}
