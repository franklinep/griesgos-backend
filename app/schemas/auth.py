# app/schemas/auth.py
from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    usuario: str = Field(..., description="Número de documento del usuario")
    contrasenia: str = Field(..., description="Contraseña del usuario")

class LoginResponse(BaseModel):
    success: bool
    message: str
    data: dict | None = None
    error: dict | None = None