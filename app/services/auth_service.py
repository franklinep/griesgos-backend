# app/services/auth_service.py
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.repositories.auth_repository import AuthRepository
from app.schemas.auth import LoginRequest, LoginResponse
from app.models.persona import Persona, PersonaLogin
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, auth_repository: AuthRepository):
        self.auth_repository = auth_repository
    
    def login(self, login_data: LoginRequest) -> LoginResponse:
        user_data = self.auth_repository.get_user_by_documento(login_data.usuario)
        
        if not user_data:
            return LoginResponse(
                success=False,
                message="Credenciales inválidas",
                error={
                    "code": "AUTH001",
                    "details": "Usuario o contraseña incorrectos"
                }
            )
        
        persona, login = user_data
        
        if not self.verify_password(login_data.contrasenia, login.v_des_clave):
            return LoginResponse(
                success=False,
                message="Credenciales inválidas",
                error={
                    "code": "AUTH001",
                    "details": "Usuario o contraseña incorrectos"
                }
            )
        
        token = self.create_jwt_token(persona, login)
        
        return LoginResponse(
            success=True,
            message="Inicio de sesión exitoso",
            data={"token": token}
        )
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    def create_jwt_token(self, persona: Persona, login: PersonaLogin) -> str:
        now = datetime.now(timezone.utc)
        exp_time = now + timedelta(minutes=5)
        # Convertir a timestamp Unix (segundos desde la época)
        now_ts = int(now.timestamp())
        exp_ts = int(exp_time.timestamp())

        payload = {
            "id": persona.i_cod_persona,
            "username": persona.v_num_documento,
            "numeroDocumento": persona.v_num_documento,
            "nombres": persona.v_des_nombres,
            "apellidoPaterno": persona.v_des_apellidos,
            "correo": login.v_des_correo,
            "celular": login.v_num_telefono,
            "iat": now_ts,
            "exp": exp_ts
        }
        print("Issued at:", datetime.fromtimestamp(payload['iat']))
        print("Expires at:", datetime.fromtimestamp(payload['exp']))
        print("Current UTC time:", datetime.now(timezone.utc))
        
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)