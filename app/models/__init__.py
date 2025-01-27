# app/models/__init__.py
from app.models.base import Base
from app.models.estructura_org import Unidad, Area, Puesto, Categoria
from app.models.persona import Persona, PersonaLogin
from app.models.persona_trabajador import PersonaTrabajador

__all__ = [
    'Base',
    'Unidad',
    'Area',
    'Puesto',
    'Categoria',
    'Persona',
    'PersonaLogin',
    'PersonaTrabajador'
]