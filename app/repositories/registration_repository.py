# app/repositories/registration_repository.py
from pytest import Session
from app.models.persona import PersonaLogin, Persona
from sqlalchemy import and_
from app.loaders.database import SessionLocal

class RegistrationRepository:
    def __init__(self, db: Session = SessionLocal):
        self.db = db
    
    def get_persona_by_documento(self, documento: str) -> Persona:
        return (
            self.db.query(Persona)
            .filter(
                and_(
                    Persona.v_num_documento == documento,
                    Persona.i_est_registro == 1
                )
            )
            .first()
        )
    
    def get_existing_login(self, persona_id: int) -> PersonaLogin:
        return (
            self.db.query(PersonaLogin)
            .filter(PersonaLogin.i_cod_persona == persona_id)
            .first()
        )
    
    def get_by_correo(self, correo: str) -> PersonaLogin:
        return (
            self.db.query(PersonaLogin)
            .filter(PersonaLogin.v_des_correo == correo)
            .first()
        )
    
    def create_login(self, persona_login: PersonaLogin) -> PersonaLogin:
        self.db.add(persona_login)
        self.db.commit()
        self.db.refresh(persona_login)
        return persona_login