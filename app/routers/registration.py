# app/routers/registration.py
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.schemas.registration import RegistrationRequest, RegistrationResponse, RegistrationVerifyRequest
from app.repositories.registration_repository import RegistrationRepository
from app.services.email_service import EmailService
from app.services.registration_service import RegistrationService
from app.loaders.database import get_db

router = APIRouter(prefix="/api/registro", tags=["registro"])
email_service = EmailService()  

def get_audit_data(request: Request) -> dict:
    return {
        "v_ip_reg": request.client.host,
        "v_ip_mod": request.client.host,
        "v_host_reg": request.headers.get("host", ""),
        "v_host_mod": request.headers.get("host", ""),
        "v_usu_reg": request.headers.get("x-user-id", "system"),
        "v_usu_mod": request.headers.get("x-user-id", "system"),
        "t_fec_reg": datetime.now(),
        "t_fec_mod": datetime.now()
    }

@router.post("", response_model=RegistrationResponse)
async def register_initial(
    request: RegistrationRequest,
    db: Session = Depends(get_db)
):    
    
    registration_service = RegistrationService(RegistrationRepository(db))

    # Validar datos usando el servicio de registro
    validation_result = registration_service.validate_registration(request)
    if not validation_result.success:
        return validation_result
    
    # Envía OTP y guarda datos de registro
    success, message = email_service.send_otp_email(
        request.correo, 
        request.dict()  # Pasa todos los datos del registro
    )

    return RegistrationResponse(
        success=success,
        message=message,
        data={
            "documento": request.documento,
            "email": request.correo
        }
    )

# app/routers/registration.py
@router.post("/verificar", response_model=RegistrationResponse)
async def verificar_otp(
    verify_request: RegistrationVerifyRequest,  # Cambio de nombre para evitar conflicto
    request: Request,  # Nuevo parámetro para obtener datos del cliente
    db: Session = Depends(get_db)
):
    # Verificar OTP y obtener datos de registro
    stored_data = email_service.verify_otp(verify_request.correo, verify_request.otp)
    if not stored_data:
        return RegistrationResponse(
            success=False,
            message="Código inválido o expirado",
            error={"code": "REG001"}
        )

    # Obtener datos de auditoría
    audit_data = get_audit_data(request)

    # Crear usuario con datos almacenados
    registration_request = RegistrationRequest(**stored_data)
    registration_service = RegistrationService(RegistrationRepository(db))
    registration_service.register(registration_request, audit_data)  # Pasamos audit_data

    return RegistrationResponse(
        success=True,
        message="Registro exitoso",
        data={
            "username": registration_request.documento,
            "email": registration_request.correo
        }
    )