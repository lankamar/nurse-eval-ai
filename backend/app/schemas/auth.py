from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str


class LoginRequest(BaseModel):
    email: str
    password: str
    code: str | None = None
    backup_code: str | None = None


class RefreshRequest(BaseModel):
    refresh_token: str
