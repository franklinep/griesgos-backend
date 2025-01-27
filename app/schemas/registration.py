# app/schemas/registration.py
from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional
import re

class RegistrationRequest(BaseModel):
    documento: str = Field(..., min_length=8, max_length=20)
    contrasenia: str = Field(..., min_length=8)
    correo: EmailStr
    telefono: str = Field(..., min_length=9, max_length=15)

    @validator('documento')
    def validate_documento(cls, v):
        if not v.isdigit():
            raise ValueError('El documento debe contener solo números')
        return v

    @validator('contrasenia')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('La contraseña debe tener al menos 8 caracteres')
        if not re.search(r'[A-Z]', v):
            raise ValueError('La contraseña debe tener al menos una mayúscula')
        if not re.search(r'[a-z]', v):
            raise ValueError('La contraseña debe tener al menos una minúscula')
        if not re.search(r'\d', v):
            raise ValueError('La contraseña debe tener al menos un número')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('La contraseña debe tener al menos un carácter especial')
        return v

    @validator('telefono')
    def validate_telefono(cls, v):
        if not v.isdigit():
            raise ValueError('El teléfono debe contener solo números')
        return v
    
    class Config:
        from_attributes = True

class RegistrationVerifyRequest(RegistrationRequest):
    otp: str = Field(..., min_length=5, max_length=5)


class RegistrationResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None
    error: Optional[dict] = None

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Usuario registrado exitosamente",
                "data": {
                    "username": "40979631",
                    "email": "usuario@gmail.com"
                }
            }
        }