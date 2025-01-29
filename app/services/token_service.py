# app/services/token_service.py
from datetime import datetime, timezone
from typing import Optional, Dict
from fastapi import HTTPException, status
from jose import ExpiredSignatureError, jwt, JWTError
from app.repositories.auth_repository import AuthRepository
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

class TokenService:
    def __init__(self, auth_repository: AuthRepository):
        self.auth_repository = auth_repository

    def validate_token(self, token: str) -> Dict:
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "success": False,
                    "message": "Token no proporcionado",
                    "error": {
                        "code": "AUTH002",
                        "details": "Se requiere token de autenticación"
                    }
                }
            )

        try:
            # Decodificar el token con validación automática de expiración
            payload = jwt.decode(
                token, 
                SECRET_KEY, 
                algorithms=[ALGORITHM], 
                options={"verify_exp": True}  # Habilitar validación del campo `exp`
            )

            # Verificar la expiración manualmente usando UTC
            now = datetime.now(timezone.utc)
            exp = datetime.fromtimestamp(payload['exp'], tz=timezone.utc)

            if now > exp:
                raise ExpiredSignatureError("Token has expired")
            
            return payload
  
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "success": False,
                    "message": "Sesión expirada",
                    "error": {
                        "code": "AUTH004",
                        "details": "Su sesión ha expirado. Por favor, vuelva a iniciar sesión"
                    }
                }
            )

        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "success": False,
                    "message": "Token inválido",
                    "error": {
                        "code": "AUTH005",
                        "details": "Token de autenticación inválido"
                    }
                }
            )