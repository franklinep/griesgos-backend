# app/routers/persona_trabajador.py
from fastapi import APIRouter, Depends, Request, Query, HTTPException
from sqlalchemy.orm import Session
from app.schemas.persona_trabajador import (
    PersonaTrabajadorCreate,
    PersonaTrabajadorUpdate,
    PersonaTrabajadorResponse
)
from app.repositories.persona_trabajador_repository import PersonaTrabajadorRepository
from app.services.persona_trabajador_service import PersonaTrabajadorService
from app.loaders.database import get_db
from app.services.token_dependency import validate_token


router = APIRouter(prefix="/api/trabajadores", tags=["trabajadores"])

def get_audit_data(request: Request) -> dict:
    """Obtiene los datos de auditoría de la request."""
    return {
        "v_ip_reg": request.client.host,
        "v_ip_mod": request.client.host,
        "v_host_reg": request.headers.get("host", ""),
        "v_host_mod": request.headers.get("host", ""),
        "v_usu_reg": request.headers.get("x-user-id", "system"),
        "v_usu_mod": request.headers.get("x-user-id", "system")
    }

@router.get("", response_model=PersonaTrabajadorResponse)
async def get_trabajadores(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    token_data: dict = Depends(validate_token)
):
    try:
        trabajador_repository = PersonaTrabajadorRepository(db)
        trabajador_service = PersonaTrabajadorService(trabajador_repository)
        return trabajador_service.get_trabajadores(skip, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{trabajador_id}", response_model=PersonaTrabajadorResponse)
async def get_trabajador(
    trabajador_id: int,
    db: Session = Depends(get_db),
    token_data: dict = Depends(validate_token)
):
    try:
        trabajador_repository = PersonaTrabajadorRepository(db)
        trabajador_service = PersonaTrabajadorService(trabajador_repository)
        response = trabajador_service.get_trabajador(trabajador_id)
        if not response.success:
            raise HTTPException(status_code=404, detail=response.error)
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("", response_model=PersonaTrabajadorResponse)
async def create_trabajador(
    request: Request,
    trabajador: PersonaTrabajadorCreate,
    db: Session = Depends(get_db),
    token_data: dict = Depends(validate_token)
):
    try:
        trabajador_repository = PersonaTrabajadorRepository(db)
        trabajador_service = PersonaTrabajadorService(trabajador_repository)
        audit_data = get_audit_data(request)
        response = trabajador_service.create_trabajador(trabajador, audit_data)
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error)
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{trabajador_id}", response_model=PersonaTrabajadorResponse)
async def update_trabajador(
    request: Request,
    trabajador_id: int,
    trabajador: PersonaTrabajadorUpdate,
    db: Session = Depends(get_db),
    token_data: dict = Depends(validate_token)
):
    try:
        trabajador_repository = PersonaTrabajadorRepository(db)
        trabajador_service = PersonaTrabajadorService(trabajador_repository)
        audit_data = get_audit_data(request)
        response = trabajador_service.update_trabajador(trabajador_id, trabajador, audit_data)
        if not response.success:
            raise HTTPException(status_code=404, detail=response.error)
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{trabajador_id}", response_model=PersonaTrabajadorResponse)
async def delete_trabajador(
    request: Request,
    trabajador_id: int,
    db: Session = Depends(get_db),
    token_data: dict = Depends(validate_token)
):
    try:
        trabajador_repository = PersonaTrabajadorRepository(db)
        trabajador_service = PersonaTrabajadorService(trabajador_repository)
        audit_data = get_audit_data(request)
        response = trabajador_service.delete_trabajador(trabajador_id, audit_data)
        if not response.success:
            raise HTTPException(status_code=404, detail=response.error)
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
