# app/schemas/estructura_org.py
from pydantic import BaseModel
from typing import Optional

class UnidadBase(BaseModel):
    v_des_nombre: str
    
    class Config:
        from_attributes = True

class AreaBase(BaseModel):
    i_cod_unidad: int
    v_des_nombre: str
    
    class Config:
        from_attributes = True

class PuestoBase(BaseModel):
    v_des_nombre: str
    
    class Config:
        from_attributes = True

class CategoriaBase(BaseModel):
    v_des_nombre: str
    
    class Config:
        from_attributes = True