# app/schemas/persona_trabajador.py
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from decimal import Decimal

class PersonaTrabajadorBase(BaseModel):
    i_cod_persona: Optional[int] = Field(None, description="Código de la persona")
    i_cod_unidad: Optional[int] = Field(None, description="Código de la unidad")
    i_cod_area: Optional[int] = Field(None, description="Código del área")
    i_cod_puesto: Optional[int] = Field(None, description="Código del puesto")
    i_cod_categoria: Optional[int] = Field(None, description="Código de la categoría")
    n_imp_sueldo: Optional[Decimal] = Field(None, description="Sueldo del trabajador")
    t_fec_ingreso: Optional[datetime] = Field(None, description="Fecha de ingreso")

    class Config:
        from_attributes = True

class PersonaTrabajadorCreate(PersonaTrabajadorBase):
    pass

class PersonaTrabajadorUpdate(BaseModel):
    i_cod_unidad: Optional[int] = None
    i_cod_area: Optional[int] = None
    i_cod_puesto: Optional[int] = None
    i_cod_categoria: Optional[int] = None
    n_imp_sueldo: Optional[Decimal] = None
    t_fec_ingreso: Optional[datetime] = None

    

class PersonaTrabajadorResponse(BaseModel):
    success: bool
    message: str
    data: Optional[PersonaTrabajadorBase | list[PersonaTrabajadorBase]] = None
    error: Optional[dict] = None

    class Config:
        from_attributes = True
