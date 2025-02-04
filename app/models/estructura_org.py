# app/models/estructura_org.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base
from datetime import datetime, timezone

class Unidad(Base):
    __tablename__ = 'grietbx_unidad'
    
    i_cod_unidad = Column(Integer, primary_key=True, autoincrement=True)
    v_des_nombre = Column(String(100), nullable=False)
    
    # Campos de auditoría
    i_est_registro = Column(Integer, default=1)
    v_usu_reg = Column(String(50))
    v_usu_mod = Column(String(50))
    t_fec_reg = Column(DateTime, default=datetime.now(timezone.utc))
    t_fec_mod = Column(DateTime)
    v_host_reg = Column(String(50))
    v_host_mod = Column(String(50))
    v_ip_reg = Column(String(15))
    v_ip_mod = Column(String(15))
    
    # Relaciones
    trabajadores = relationship("PersonaTrabajador", back_populates="unidad")

class Area(Base):
    __tablename__ = 'grietbx_area'
    
    i_cod_area = Column(Integer, primary_key=True, autoincrement=True)
    v_des_nombre = Column(String(100), nullable=False)
    
    # Campos de auditoría
    i_est_registro = Column(Integer, default=1)
    v_usu_reg = Column(String(50))
    v_usu_mod = Column(String(50))
    t_fec_reg = Column(DateTime, default=datetime.now(timezone.utc))
    t_fec_mod = Column(DateTime)
    v_host_reg = Column(String(50))
    v_host_mod = Column(String(50))
    v_ip_reg = Column(String(15))
    v_ip_mod = Column(String(15))
    
    # Relaciones
    trabajadores = relationship("PersonaTrabajador", back_populates="area")

class Puesto(Base):
    __tablename__ = 'grietbx_puesto'
    
    i_cod_puesto = Column(Integer, primary_key=True, autoincrement=True)
    v_des_nombre = Column(String(100), nullable=False)
    
    # Campos de auditoría
    i_est_registro = Column(Integer, default=1)
    v_usu_reg = Column(String(50))
    v_usu_mod = Column(String(50))
    t_fec_reg = Column(DateTime, default=datetime.now(timezone.utc))
    t_fec_mod = Column(DateTime)
    v_host_reg = Column(String(50))
    v_host_mod = Column(String(50))
    v_ip_reg = Column(String(15))
    v_ip_mod = Column(String(15))
    
    # Relaciones
    trabajadores = relationship("PersonaTrabajador", back_populates="puesto")

class Categoria(Base):
    __tablename__ = 'grietbx_categoria'
    
    i_cod_categoria = Column(Integer, primary_key=True, autoincrement=True)
    v_des_nombre = Column(String(100), nullable=False)
    
    # Campos de auditoría
    i_est_registro = Column(Integer, default=1)
    v_usu_reg = Column(String(50))
    v_usu_mod = Column(String(50))
    t_fec_reg = Column(DateTime, default=datetime.now(timezone.utc))
    t_fec_mod = Column(DateTime)
    v_host_reg = Column(String(50))
    v_host_mod = Column(String(50))
    v_ip_reg = Column(String(15))
    v_ip_mod = Column(String(15))
    
    # Relaciones
    trabajadores = relationship("PersonaTrabajador", back_populates="categoria")