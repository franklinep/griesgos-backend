# app/services/persona_service.py
from datetime import datetime, timezone
from typing import Optional, List
from fastapi import HTTPException
from app.repositories.persona_repository import PersonaRepository, PersonaLoginRepository
from app.schemas.persona import (
    PersonaCreate, 
    PersonaUpdate, 
    PersonaResponse,
    PersonaLoginCreate,
    PersonaLoginUpdate
)
from app.models.persona import Persona, PersonaLogin
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class PersonaService:
    def __init__(
        self, 
        persona_repository: PersonaRepository,
        persona_login_repository: PersonaLoginRepository
    ):
        self.persona_repository = persona_repository
        self.persona_login_repository = persona_login_repository
    
    def get_personas(self, skip: int = 0, limit: int = 100) -> PersonaResponse:
        personas = self.persona_repository.get_all(skip, limit)
        return PersonaResponse(
            success=True,
            message="Personas recuperadas exitosamente",
            data=personas
        )
    
    def get_persona(self, i_cod_persona: int) -> PersonaResponse:
        persona = self.persona_repository.get_by_id(i_cod_persona)
        if not persona:
            return PersonaResponse(
                success=False,
                message="Persona no encontrada",
                error={
                    "code": "PER001",
                    "details": f"No se encontró la persona con código {i_cod_persona}"
                }
            )
        
        return PersonaResponse(
            success=True,
            message="Persona recuperada exitosamente",
            data=persona
        )

    def get_personas_by_empresa(self, v_cod_empresa: str) -> PersonaResponse:
        personas = self.persona_repository.get_by_empresa(v_cod_empresa)
        return PersonaResponse(
            success=True,
            message="Personas recuperadas exitosamente",
            data=personas
        )
    
    def create_persona(
        self, 
        persona_data: PersonaCreate, 
        login_data: Optional[PersonaLoginCreate],
        audit_data: dict
    ) -> PersonaResponse:
        # Verificar si ya existe una persona con el mismo documento
        existing_persona = self.persona_repository.get_by_documento(persona_data.v_num_documento)
        if existing_persona:
            return PersonaResponse(
                success=False,
                message="Documento ya registrado",
                error={
                    "code": "PER002",
                    "details": "Ya existe una persona con este número de documento"
                }
            )
        
        # Verificar correo único si se proporciona
        if login_data and login_data.v_des_correo:
            existing_login = self.persona_login_repository.get_by_correo(login_data.v_des_correo)
            if existing_login:
                return PersonaResponse(
                    success=False,
                    message="Correo ya registrado",
                    error={
                        "code": "PER003",
                        "details": "Ya existe un usuario con este correo electrónico"
                    }
                )
        
        # Crear nueva persona
        new_persona = Persona(
            v_num_documento=persona_data.v_num_documento,
            v_des_nombres=persona_data.v_des_nombres,
            v_des_apellidos=persona_data.v_des_apellidos,
            v_cod_empresa=persona_data.v_cod_empresa,
            i_est_registro=1,
            v_usu_reg=audit_data["v_usu_reg"],
            t_fec_reg=audit_data["t_fec_reg"],
            v_host_reg=audit_data["v_host_reg"],
            v_ip_reg=audit_data["v_ip_reg"],
        )
        
        created_persona = self.persona_repository.create(new_persona)
        
        # Crear login si se proporciona
        if login_data:
            new_login = PersonaLogin(
                i_cod_persona=created_persona.i_cod_persona,
                v_des_usuario=login_data.v_des_usuario,
                v_des_clave=pwd_context.hash(login_data.v_des_clave),
                v_des_correo=login_data.v_des_correo,
                v_num_telefono=login_data.v_num_telefono
            )
            self.persona_login_repository.create(new_login)
        
        return PersonaResponse(
            success=True,
            message="Persona creada exitosamente",
            data=created_persona
        )
    
    def update_persona(
        self, 
        i_cod_persona: int, 
        persona_data: PersonaUpdate,
        login_data: Optional[PersonaLoginUpdate],
        audit_data: dict
    ) -> PersonaResponse:
        # Verificar si existe la persona
        persona = self.persona_repository.get_by_id(i_cod_persona)
        if not persona:
            return PersonaResponse(
                success=False,
                message="Persona no encontrada",
                error={
                    "code": "PER001",
                    "details": f"No se encontró la persona con código {i_cod_persona}"
                }
            )
        
        # Verificar documento único si se está actualizando
        if persona_data.v_num_documento:
            existing_persona = self.persona_repository.get_by_documento(persona_data.v_num_documento)
            if existing_persona and existing_persona.i_cod_persona != i_cod_persona:
                return PersonaResponse(
                    success=False,
                    message="Documento ya registrado",
                    error={
                        "code": "PER002",
                        "details": "Ya existe otra persona con este número de documento"
                    }
                )
        
        # Verificar correo único si se está actualizando
        if login_data and login_data.v_des_correo:
            existing_login = self.persona_login_repository.get_by_correo(login_data.v_des_correo)
            if existing_login and existing_login.i_cod_persona != i_cod_persona:
                return PersonaResponse(
                    success=False,
                    message="Correo ya registrado",
                    error={
                        "code": "PER003",
                        "details": "Ya existe otro usuario con este correo electrónico"
                    }
                )
        
        # Actualizar campos de persona si se proporcionaron
        if persona_data.v_num_documento:
            persona.v_num_documento = persona_data.v_num_documento
        if persona_data.v_des_nombres:
            persona.v_des_nombres = persona_data.v_des_nombres
        if persona_data.v_des_apellidos:
            persona.v_des_apellidos = persona_data.v_des_apellidos
        if persona_data.v_cod_empresa:
            persona.v_cod_empresa = persona_data.v_cod_empresa
            
        # Actualizar campos de auditoría
        persona.v_usu_mod = audit_data["v_usu_mod"]
        persona.v_host_mod = audit_data["v_host_mod"]
        persona.v_ip_mod = audit_data["v_ip_mod"]
        persona.t_fec_mod = datetime.now(timezone.utc)
        
        updated_persona = self.persona_repository.update(persona)
        
        # Actualizar login si se proporciona
        if login_data:
            persona_login = self.persona_login_repository.get_by_persona(i_cod_persona)
            if persona_login:
                if login_data.v_des_usuario:
                    persona_login.v_des_usuario = login_data.v_des_usuario
                if login_data.v_des_clave:
                    persona_login.v_des_clave = pwd_context.hash(login_data.v_des_clave)
                if login_data.v_des_correo:
                    persona_login.v_des_correo = login_data.v_des_correo
                if login_data.v_num_telefono:
                    persona_login.v_num_telefono = login_data.v_num_telefono
                
                self.persona_login_repository.update(persona_login)
        
        return PersonaResponse(
            success=True,
            message="Persona actualizada exitosamente",
            data=updated_persona
        )
    
    def delete_persona(
        self, 
        i_cod_persona: int, 
        audit_data: dict
    ) -> PersonaResponse:
        persona = self.persona_repository.get_by_id(i_cod_persona)
        if not persona:
            return PersonaResponse(
                success=False,
                message="Persona no encontrada",
                error={
                    "code": "PER001",
                    "details": f"No se encontró la persona con código {i_cod_persona}"
                }
            )
        
        # Actualizar campos de auditoría
        persona.v_usu_mod = audit_data["v_usu_mod"]
        persona.v_host_mod = audit_data["v_host_mod"]
        persona.v_ip_mod = audit_data["v_ip_mod"]
        persona.t_fec_mod = datetime.utcnow()
        
        self.persona_repository.delete(persona)
        
        return PersonaResponse(
            success=True,
            message="Persona eliminada exitosamente"
        )