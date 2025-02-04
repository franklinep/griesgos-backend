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

@router.post("", response_model=RegistrationResponse)
async def register_initial(
    request: RegistrationRequest,
    db: Session = Depends(get_db)
):    
    # Validar existencia previa
    registration_service = RegistrationService(RegistrationRepository(db))
    validation_result = registration_service.validate_registration(request)
    if not validation_result.success:
        return validation_result
    
    # Envía OTP y guarda datos de registro
    success, message, session_token = email_service.send_otp_email(
        request.correo, 
        request.dict()
    )

    return RegistrationResponse(
        success=success,
        message=message,
        session_token=session_token,
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
    # Verificar OTP y obtener datos de registro
    stored_data = email_service.verify_otp(request.session_token, request.otp)
    if not stored_data:
        return RegistrationResponse(
            success=False,
            message="Código inválido o expirado",
            error={"code": "REG001"}
        )

    # Crear usuario con datos almacenados
    registration_request = RegistrationRequest(**stored_data)
    registration_service = RegistrationService(RegistrationRepository(db))
    
    # Validar nuevamente antes de crear
    validation_result = registration_service.validate_registration(registration_request)
    if not validation_result.success:
        return validation_result
        
    result = registration_service.register(registration_request)
    return result