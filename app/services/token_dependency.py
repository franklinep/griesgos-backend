# app/services/token_dependency.py
from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.loaders.database import get_db
from app.repositories.auth_repository import AuthRepository
from app.services.token_service import TokenService

async def validate_token(
    authorization: Optional[str] = Header(None, description="Bearer token"),
    db: Session = Depends(get_db)
) -> dict:
    print("Se está ejecutando la validación del token...")
    if not authorization:
        raise HTTPException(status_code=401, detail="No se otorgó token de autenticación")
        
    token = authorization.split(" ")[1] if authorization.startswith("Bearer ") else authorization
    auth_repository = AuthRepository(db)
    token_service = TokenService(auth_repository)
    return token_service.validate_token(token)