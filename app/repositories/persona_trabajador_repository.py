# app/repositories/persona_trabajador_repository.py
from sqlalchemy import and_
from typing import Optional, List
from app.models.persona_trabajador import PersonaTrabajador
from app.loaders.database import SessionLocal

class PersonaTrabajadorRepository:
    def __init__(self, db: SessionLocal):
        self.db = db
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[PersonaTrabajador]:
        return (
            self.db.query(PersonaTrabajador)
            .filter(PersonaTrabajador.i_est_registro == 1)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_id(self, i_cod_trabajador: int) -> Optional[PersonaTrabajador]:
        return (
            self.db.query(PersonaTrabajador)
            .filter(
                and_(
                    PersonaTrabajador.i_cod_trabajador == i_cod_trabajador,
                    PersonaTrabajador.i_est_registro == 1
                )
            )
            .first()
        )
    
    def get_cod_persona(self, i_cod_persona: int) -> Optional[PersonaTrabajador]:
        return (
            self.db.query(PersonaTrabajador)
            .filter(
                and_(
                    PersonaTrabajador.i_cod_persona == i_cod_persona,
                    PersonaTrabajador.i_est_registro == 1
                )
            )
            .first()
        )
    
    def create(self, trabajador: PersonaTrabajador) -> PersonaTrabajador:
        self.db.add(trabajador)
        self.db.commit()
        self.db.refresh(trabajador)
        return trabajador
    
    def update(self, trabajador: PersonaTrabajador) -> PersonaTrabajador:
        self.db.commit()
        self.db.refresh(trabajador)
        return trabajador
    
    def delete(self, trabajador: PersonaTrabajador) -> PersonaTrabajador:
        trabajador.i_est_registro = 0
        self.db.commit()
        self.db.refresh(trabajador)
        return trabajador