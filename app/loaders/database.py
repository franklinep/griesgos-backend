# app/loaders/database.py
from typing import Generator
from sqlalchemy.orm import Session
from app.models.base import Base
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

# Crear el objeto URL para SQL Server
url_object = URL.create(
    "mssql+pyodbc",  # dialecto
    host="DESKTOP-7AMS20K",  # tu servidor
    database="GRiesgosDB",   # tu base de datos
    query={  # parámetros adicionales
        "driver": "ODBC Driver 17 for SQL Server",
        "TrustedConnection": "yes",
    },
)

# Crear el engine usando el objeto URL
engine = create_engine(
    url_object,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine, checkfirst=True)