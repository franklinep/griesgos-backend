# app/models/persona_trabajador.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.models.base import Base
from datetime import datetime

class PersonaTrabajador(Base):
    __tablename__ = 'griemvc_persona_trabajador'
    
    i_cod_trabajador = Column(Integer, primary_key=True, autoincrement=True)
    i_cod_persona = Column(Integer, ForeignKey('grietbc_persona.i_cod_persona'))
    i_cod_unidad = Column(Integer, ForeignKey('grietbx_unidad.i_cod_unidad'))
    i_cod_area = Column(Integer, ForeignKey('grietbx_area.i_cod_area'))
    i_cod_puesto = Column(Integer, ForeignKey('grietbx_puesto.i_cod_puesto'))
    i_cod_categoria = Column(Integer, ForeignKey('grietbx_categoria.i_cod_categoria'))
    n_imp_sueldo = Column(Numeric(10, 2))
    t_fec_ingreso = Column(DateTime, default=datetime.utcnow)
    
    # Campos de auditoría
    i_est_registro = Column(Integer, default=1)
    v_usu_reg = Column(String(50))
    v_usu_mod = Column(String(50))
    t_fec_reg = Column(DateTime, default=datetime.utcnow)
    t_fec_mod = Column(DateTime)
    v_host_reg = Column(String(50))
    v_host_mod = Column(String(50))
    v_ip_reg = Column(String(50))
    v_ip_mod = Column(String(50))
    
    # Relaciones
    persona = relationship("Persona", back_populates="trabajador")
    unidad = relationship("Unidad", back_populates="trabajadores")
    area = relationship("Area", back_populates="trabajadores")
    puesto = relationship("Puesto", back_populates="trabajadores")
    categoria = relationship("Categoria", back_populates="trabajadores")