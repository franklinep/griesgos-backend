# app/schemas/persona.py
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class PersonaBase(BaseModel):
    v_num_documento: str = Field(None, description="Número de documento de la persona")
    v_des_nombres: str = Field(None, min_length=2, max_length=100, description="Nombres de la persona")
    v_des_apellidos: str = Field(None, min_length=2, max_length=100, description="Apellidos de la persona")
    v_cod_empresa: Optional[str] = Field(None, max_length=20, description="Código de empresa")

class PersonaCreate(PersonaBase):
    pass

class PersonaUpdate(PersonaBase):
    v_num_documento: Optional[str] = Field(None)
    v_des_nombres: Optional[str] = Field(None, min_length=2, max_length=100)
    v_des_apellidos: Optional[str] = Field(None, min_length=2, max_length=100)
    v_cod_empresa: Optional[str] = Field(None, max_length=20)

class PersonaLoginBase(BaseModel):
    v_des_usuario: str = Field(None, min_length=3, max_length=50)
    v_des_correo: Optional[str] = Field(None, max_length=100)
    v_num_telefono: Optional[str] = Field(None, max_length=20)

class PersonaLoginCreate(PersonaLoginBase):
    v_des_clave: str = Field(..., min_length=8)

class PersonaLoginUpdate(PersonaLoginBase):
    v_des_clave: Optional[str] = Field(None, min_length=8)

class Persona(PersonaBase):
    i_cod_persona: int
    i_est_registro: int
    v_usu_reg: str
    t_fec_reg: datetime
    v_host_reg: str
    v_ip_reg: str
    v_usu_mod: Optional[str] = None
    t_fec_mod: Optional[datetime] = None
    v_host_mod: Optional[str] = None
    v_ip_mod: Optional[str] = None

    class Config:
        from_attributes = True

class PersonaResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Persona | list[Persona]] = None
    error: Optional[dict] = None
    
    class Config:
        from_attributes = True