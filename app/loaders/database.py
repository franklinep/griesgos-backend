# app/loaders/database.py
from typing import Generator
from sqlalchemy.orm import Session
from app.models.base import Base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
# Asegurarse que el directorio data existe
os.makedirs("data", exist_ok=True)

# Usar SQLite como base de datos
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Conectar a SQLite con soporte para foreign keys
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
# autoflush: True -> Envía el estado actual de los cambios de la sesión a la base de datos de manera automatica
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    #Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine, checkfirst=True)