# app/repositories/auth_repository.py
from app.loaders.database import SessionLocal
from app.models.persona import Persona, PersonaLogin

class AuthRepository:
    def __init__(self, db: SessionLocal): # type: ignore
        self.db = db

    def get_user_by_documento(self, documento: str) -> tuple[Persona, PersonaLogin] | None:
        return (
            self.db.query(Persona, PersonaLogin)
            .join(PersonaLogin)
            .filter(
                Persona.v_num_documento == documento,
                Persona.i_est_registro == 1
            )
            .first()
        )