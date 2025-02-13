# app/services/persona_service.py
from datetime import datetime, timezone
from typing import Optional, List
from fastapi import HTTPException
from app.repositories.persona_repository import PersonaRepository, PersonaLoginRepository
from app.schemas.persona import (
    PersonaCreate, 
    PersonaUpdate, 
    PersonaResponse,
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
        audit_data: dict
    ) -> PersonaResponse:
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
        
        new_persona = Persona(
            v_num_documento=persona_data.v_num_documento,
            v_des_nombres=persona_data.v_des_nombres,
            v_des_apellidos=persona_data.v_des_apellidos,
            v_cod_empresa=persona_data.v_cod_empresa,
            i_est_registro=1,
            v_usu_reg=audit_data["v_usu_reg"],
            v_host_reg=audit_data["v_host_reg"],
            v_ip_reg=audit_data["v_ip_reg"],
            t_fec_reg=audit_data["t_fec_reg"]
        )
        
        created_persona = self.persona_repository.create(new_persona)
        
        return PersonaResponse(
            success=True,
            message="Persona creada exitosamente",
            data=created_persona
        )
    
    def update_persona(
        self, 
        i_cod_persona: int, 
        persona_data: PersonaUpdate,
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
        
        # Verificar documento único de ser actualizado
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