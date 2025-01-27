# app/models/persona.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Persona(Base):
    __tablename__ = 'grietbc_persona'
    
    i_cod_persona = Column(Integer, primary_key=True, autoincrement=True)
    v_num_documento = Column(String(20), nullable=False, unique=True)
    v_des_nombres = Column(String(100), nullable=False)
    v_des_apellidos = Column(String(100), nullable=False)
    v_cod_empresa = Column(String(20), nullable=True)
    
    # campos de auditoria
    i_est_registro = Column(Integer, default=1)
    v_usu_reg = Column(String(50))
    v_usu_mod = Column(String(50))
    t_fec_reg = Column(DateTime)
    t_fec_mod = Column(DateTime)
    v_host_reg = Column(String(50))
    v_host_mod = Column(String(50))
    v_ip_reg = Column(String(15))
    v_ip_mod = Column(String(15))

    # Relaciones
    login = relationship("PersonaLogin", back_populates="persona", uselist=False)
    trabajador = relationship("PersonaTrabajador", back_populates="persona", uselist=False)

class PersonaLogin(Base):
    __tablename__ = 'grietbc_persona_login'
    
    i_cod_login = Column(Integer, primary_key=True, autoincrement=True)
    i_cod_persona = Column(Integer, ForeignKey('grietbc_persona.i_cod_persona'))
    v_des_usuario = Column(String(50), nullable=False)
    v_des_clave = Column(String(255), nullable=False)
    v_des_correo = Column(String(100), nullable=True, unique=True)
    v_num_telefono = Column(String(20), nullable=True)
    
    persona = relationship("Persona", back_populates="login")