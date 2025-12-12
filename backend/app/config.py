from functools import lru_cache

from pydantic import field_validator
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)

    database_url: str = Field("postgresql://postgres:postgres@localhost:5432/nurse_eval", alias="DATABASE_URL")
    jwt_secret: str = Field(..., alias="JWT_SECRET")
    jwt_expire_minutes: int = Field(1440, alias="JWT_EXPIRE_MINUTES")
    totp_issuer: str = Field("NurseEval", alias="TOTP_ISSUER")
    totp_interval: int = Field(30, alias="TOTP_INTERVAL")
    backup_codes: int = Field(10, alias="BACKUP_CODES")

    # Demo seed defaults (fixed so the team can log in locally)
    demo_totp_secret: str = Field("JBSWY3DPEHPK3PXP", alias="DEMO_TOTP_SECRET")
    demo_backup_codes: list[str] = Field(
        default_factory=lambda: [
            "BACKUP-0001",
            "BACKUP-0002",
            "BACKUP-0003",
            "BACKUP-0004",
            "BACKUP-0005",
        ],
        alias="DEMO_BACKUP_CODES",
    )

    gcp_project_id: str | None = Field(None, alias="GCP_PROJECT_ID")
    gcp_bucket: str | None = Field(None, alias="GCP_BUCKET")

    redis_url: str = Field("redis://localhost:6379/0", alias="REDIS_URL")

    @field_validator("database_url", mode="before")
    @classmethod
    def _normalize_database_url(cls, value: str):
        if isinstance(value, str) and value.startswith("postgres://"):
            # Render (y otros) a veces entregan postgres://; SQLAlchemy espera postgresql://
            return "postgresql://" + value[len("postgres://") :]
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
