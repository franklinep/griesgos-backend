# app/routers/persona.py
from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.orm import Session
from app.schemas.persona import (
    PersonaCreate,
    PersonaUpdate,
    PersonaResponse,
    PersonaLoginCreate,
    PersonaLoginUpdate
)
from app.repositories.persona_repository import PersonaRepository, PersonaLoginRepository
from app.services.persona_service import PersonaService
from app.loaders.database import get_db
from app.services.token_dependency import validate_token

router = APIRouter(prefix="/api/personas", tags=["personas"])

def get_audit_data(request: Request) -> dict:
    return {
        "v_ip_reg": request.client.host,
        "v_ip_mod": request.client.host,
        "v_host_reg": request.headers.get("host", ""),
        "v_host_mod": request.headers.get("host", ""),
        "v_usu_reg": request.headers.get("x-user-id", "system"),
        "v_usu_mod": request.headers.get("x-user-id", "system")
    }

def get_services(db: Session = Depends(get_db)) -> PersonaService:
    persona_repository = PersonaRepository(db)
    persona_login_repository = PersonaLoginRepository(db)
    return PersonaService(persona_repository, persona_login_repository)

@router.get("", response_model=PersonaResponse)
async def get_personas(
    request: Request,
    page: int = Query(1, gt=0),
    per_page: int = Query(10, gt=0, le=100),
    empresa: str | None = None,
    service: PersonaService = Depends(get_services),
    token_data: dict = Depends(validate_token)
):
    print(f"Token Data: {token_data}")
    skip = (page - 1) * per_page
    return service.get_personas_by_empresa(empresa) if empresa else service.get_personas(skip, per_page)

@router.get("/{persona_id}", response_model=PersonaResponse)
async def get_persona(
    persona_id: int,
    service: PersonaService = Depends(get_services),
    token_data: dict = Depends(validate_token)
):
    return service.get_persona(persona_id)

@router.post("", response_model=PersonaResponse)
async def create_persona(
    request: Request,
    persona: PersonaCreate,
    login_data: PersonaLoginCreate | None = None,
    service: PersonaService = Depends(get_services),
    token_data: dict = Depends(validate_token)
):
    return service.create_persona(persona, login_data, get_audit_data(request))

@router.put("/{persona_id}", response_model=PersonaResponse)
async def update_persona(
    request: Request,
    persona_id: int,
    persona: PersonaUpdate,
    login_data: PersonaLoginUpdate | None = None,
    service: PersonaService = Depends(get_services),
    token_data: dict = Depends(validate_token)
):
    return service.update_persona(persona_id, persona, login_data, get_audit_data(request))

@router.delete("/{persona_id}", response_model=PersonaResponse)
async def delete_persona(
    request: Request,
    persona_id: int,
    service: PersonaService = Depends(get_services),
    token_data: dict = Depends(validate_token)
):
    return service.delete_persona(persona_id, get_audit_data(request))