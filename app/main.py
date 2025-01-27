# main.py
from fastapi import FastAPI, Request
from app.loaders.database import init_db
from app.routers import (
    auth,
    persona,
    persona_trabajador,
    registration,
    excel
)

app = FastAPI(
    title="API GRIESGOS",
    description="API para el sistema de gestión de riesgos",
    version="1.0.0"
)

# Registrar los routers
app.include_router(auth.router)
app.include_router(persona.router)
app.include_router(persona_trabajador.router)
app.include_router(registration.router)
app.include_router(excel.router)

@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/")
async def root():
    return {
        "message": "API GRIESGOS funcionando correctamente",
        "status": "OK"
    }