# app/services/registration_service.py
from datetime import datetime, timezone
from passlib.context import CryptContext
from app.repositories.registration_repository import RegistrationRepository
from app.schemas.registration import RegistrationRequest, RegistrationResponse
from app.models.persona import PersonaLogin

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class RegistrationService:
    def __init__(self, registration_repository: RegistrationRepository):
        self.registration_repository = registration_repository

    def validate_registration(self, registration_data: RegistrationRequest) -> RegistrationResponse:
        # Verificar si existe la persona
        persona = self.registration_repository.get_persona_by_documento(
            registration_data.documento
        )
        
        if not persona:
            return RegistrationResponse(
                success=False,
                message="Persona no encontrada",
                error={
                    "code": "REG001",
                    "details": "No existe una persona registrada con este número de documento"
                }
            )
        
        # Verificar si ya tiene login
        existing_login = self.registration_repository.get_existing_login(
            persona.i_cod_persona
        )
        
        if existing_login:
            return RegistrationResponse(
                success=False,
                message="Usuario ya registrado",
                error={
                    "code": "REG002",
                    "details": "Esta persona ya tiene credenciales de acceso registradas"
                }
            )
            
        # Verificar si el correo ya está registrado
        existing_email = self.registration_repository.get_by_correo(
            registration_data.correo
        )
        
        if existing_email:
            return RegistrationResponse(
                success=False,
                message="Correo ya registrado",
                error={
                    "code": "REG003",
                    "details": "Este correo electrónico ya está registrado"
                }
            )
            
        return RegistrationResponse(
            success=True,
            message="Validación exitosa"
        )
    
    def register(self, registration_data: RegistrationRequest, audit_data: dict) -> RegistrationResponse:
        persona = self.registration_repository.get_persona_by_documento(
            registration_data.documento
        )
        
        hashed_password = pwd_context.hash(registration_data.contrasenia)
        new_login = PersonaLogin(
            i_cod_persona=persona.i_cod_persona,
            v_des_usuario=persona.v_num_documento,
            v_des_clave=hashed_password,
            v_des_correo=registration_data.correo,
            v_num_telefono=registration_data.telefono,
            # Campos de auditoría
            v_usu_reg=audit_data["v_usu_reg"],
            t_fec_reg=audit_data["t_fec_reg"],
            v_host_reg=audit_data["v_host_reg"],
            v_ip_reg=audit_data["v_ip_reg"],
        )
        
        self.registration_repository.create_login(new_login)
        
        return RegistrationResponse(
            success=True,
            message="Usuario registrado exitosamente",
            data={
                "username": persona.v_num_documento,
                "email": registration_data.correo
            }
        )