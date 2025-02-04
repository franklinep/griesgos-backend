# app/schemas/estructura_org.py
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
class AuditFields(BaseModel):
    v_des_nombre: str

    i_est_registro: Optional[int] = 1
    v_usu_reg: Optional[str] = None
    v_usu_mod: Optional[str] = None
    t_fec_reg: Optional[datetime] = None
    t_fec_mod: Optional[datetime] = None
    v_host_reg: Optional[str] = None
    v_host_mod: Optional[str] = None
    v_ip_reg: Optional[str] = None
    v_ip_mod: Optional[str] = None

    class config:
        from_attributes = True

class UnidadBase(AuditFields):
    pass

class AreaBase(AuditFields):
    pass

class PuestoBase(AuditFields):
    pass

class CategoriaBase(AuditFields):
    pass