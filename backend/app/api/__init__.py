from fastapi import APIRouter

from app.api import admin, auth, evaluations

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(evaluations.router, prefix="/evaluations", tags=["evaluations"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
