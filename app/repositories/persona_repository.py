# app/repositories/persona_repository.py
from app.loaders.database import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional, List
from datetime import datetime
from app.models.persona import Persona, PersonaLogin

class PersonaRepository:
    def __init__(self, db: Session = SessionLocal):
        self.db = db
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Persona]:
        return (
            self.db.query(Persona)
            .filter(Persona.i_est_registro == 1)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_id(self, i_cod_persona: int) -> Optional[Persona]:
        return (
            self.db.query(Persona)
            .filter(
                and_(
                    Persona.i_cod_persona == i_cod_persona,
                    Persona.i_est_registro == 1
                )
            )
            .first()
        )
    
    def get_by_documento(self, v_num_documento: str) -> Optional[Persona]:
        return (
            self.db.query(Persona)
            .filter(
                and_(
                    Persona.v_num_documento == v_num_documento,
                    Persona.i_est_registro == 1
                )
            )
            .first()
        )

    def get_by_empresa(self, v_cod_empresa: str) -> List[Persona]:
        return (
            self.db.query(Persona)
            .filter(
                and_(
                    Persona.v_cod_empresa == v_cod_empresa,
                    Persona.i_est_registro == 1
                )
            )
            .all()
        )
    
    def create(self, persona: Persona) -> Persona:
        self.db.add(persona)
        self.db.commit()
        self.db.refresh(persona)
        return persona
    
    def update(self, persona: Persona) -> Persona:
        self.db.commit()
        self.db.refresh(persona)
        return persona
    
    def delete(self, persona: Persona) -> Persona:
        persona.i_est_registro = 0
        self.db.commit()
        self.db.refresh(persona)
        return persona

class PersonaLoginRepository:
    def __init__(self, db: SessionLocal):
        self.db = db
    
    def get_by_persona(self, i_cod_persona: int) -> Optional[PersonaLogin]:
        return (
            self.db.query(PersonaLogin)
            .filter(PersonaLogin.i_cod_persona == i_cod_persona)
            .first()
        )

    def get_by_correo(self, v_des_correo: str) -> Optional[PersonaLogin]:
        return (
            self.db.query(PersonaLogin)
            .filter(PersonaLogin.v_des_correo == v_des_correo)
            .first()
        )

    def create(self, persona_login: PersonaLogin) -> PersonaLogin:
        self.db.add(persona_login)
        self.db.commit()
        self.db.refresh(persona_login)
        return persona_login

    def update(self, persona_login: PersonaLogin) -> PersonaLogin:
        self.db.commit()
        self.db.refresh(persona_login)
        return persona_login