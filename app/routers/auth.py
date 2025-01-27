# app/routers/auth.py
from fastapi import APIRouter, Depends, Request
from app.schemas.auth import LoginRequest, LoginResponse
from app.repositories.auth_repository import AuthRepository
from app.services.auth_service import AuthService
from app.loaders.database import get_db

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/login", response_model=LoginResponse)
async def login(
    request: Request,
    login_data: LoginRequest,
    db = Depends(get_db)
):
    auth_repository = AuthRepository(db)
    auth_service = AuthService(auth_repository)
    return auth_service.login(login_data)