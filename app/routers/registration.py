# app/routers/registration.py
from typing import Dict
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.registration import RegistrationRequest, RegistrationResponse, RegistrationVerifyRequest
from app.repositories.registration_repository import RegistrationRepository
from app.services.email_service import EmailService
from app.services.registration_service import RegistrationService
from app.loaders.database import get_db

router = APIRouter(prefix="/api/registro", tags=["registro"])
email_service = EmailService()  
doc = None

@router.post("", response_model=RegistrationResponse)
async def register_initial(
    request: RegistrationRequest,
    db: Session = Depends(get_db)
):    
    success, message = email_service.send_otp_email(request.correo)
    doc = request.documento

    return RegistrationResponse(
        success=success,
        message=message,
        data={
            "documento": request.documento,
            "email": request.correo
        }
    )

@router.post("/verificar", response_model=RegistrationResponse)
async def verificar_otp(
    request: RegistrationVerifyRequest,
    db: Session = Depends(get_db)
):
    # Verify OTP first
    is_valid = email_service.verify_otp(request.correo, request.otp)
    if not is_valid:
        return RegistrationResponse(
            success=False,
            message="El código de verificación no es válido o ha expirado",
            error={"code": "REG001"}
        )

     # If OTP valid, proceed with registration
    registration_repository = RegistrationRepository(db)
    registration_service = RegistrationService(registration_repository)
    result = registration_service.register(request)

    return RegistrationResponse(
        success=True,
        message="Usuario registrado exitosamente",
        data={
            "username": request.documento,
            "email": request.correo
        }
    )