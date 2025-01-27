# app/models/estructura_org.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Unidad(Base):
    __tablename__ = 'grietbx_unidad'
    
    i_cod_unidad = Column(Integer, primary_key=True, autoincrement=True)
    v_des_nombre = Column(String(100), nullable=False)
    
    # Usar strings para referencias diferidas
    areas = relationship("Area", back_populates="unidad")
    trabajadores = relationship("PersonaTrabajador", back_populates="unidad")

class Area(Base):
    __tablename__ = 'grietbx_area'
    
    i_cod_area = Column(Integer, primary_key=True, autoincrement=True)
    i_cod_unidad = Column(Integer, ForeignKey('grietbx_unidad.i_cod_unidad'))
    v_des_nombre = Column(String(100), nullable=False)
    
    unidad = relationship("Unidad", back_populates="areas")
    trabajadores = relationship("PersonaTrabajador", back_populates="area")

class Puesto(Base):
    __tablename__ = 'grietbx_puesto'
    
    i_cod_puesto = Column(Integer, primary_key=True, autoincrement=True)
    v_des_nombre = Column(String(100), nullable=False)
    
    trabajadores = relationship("PersonaTrabajador", back_populates="puesto")

class Categoria(Base):
    __tablename__ = 'grietbx_categoria'
    
    i_cod_categoria = Column(Integer, primary_key=True, autoincrement=True)
    v_des_nombre = Column(String(100), nullable=False)
    
    trabajadores = relationship("PersonaTrabajador", back_populates="categoria")
