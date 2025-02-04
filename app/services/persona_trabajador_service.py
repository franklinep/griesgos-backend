# app/services/persona_trabajador_service.py
from datetime import datetime, timezone
from app.repositories.persona_trabajador_repository import PersonaTrabajadorRepository
from app.schemas.persona_trabajador import (
    PersonaTrabajadorCreate,
    PersonaTrabajadorUpdate,
    PersonaTrabajadorResponse
)
from app.models.persona_trabajador import PersonaTrabajador

class PersonaTrabajadorService:
    def __init__(self, trabajador_repository: PersonaTrabajadorRepository):
        self.trabajador_repository = trabajador_repository
    
    def get_trabajadores(self, skip: int = 0, limit: int = 100) -> PersonaTrabajadorResponse:
        trabajadores = self.trabajador_repository.get_all(skip, limit)
        return PersonaTrabajadorResponse(
            success=True,
            message="Trabajadores recuperados exitosamente",
            data=trabajadores
        )
    
    def get_trabajador(self, i_cod_trabajador: int) -> PersonaTrabajadorResponse:
        trabajador = self.trabajador_repository.get_by_id(i_cod_trabajador)
        if not trabajador:
            return PersonaTrabajadorResponse(
                success=False,
                message="Trabajador no encontrado",
                error={
                    "code": "TRB001",
                    "details": f"No se encontró el trabajador con código {i_cod_trabajador}"
                }
            )
        
        return PersonaTrabajadorResponse(
            success=True,
            message="Trabajador recuperado exitosamente",
            data=trabajador
        )
    
    def create_trabajador(
        self, 
        trabajador_data: PersonaTrabajadorCreate,
        audit_data: dict
    ) -> PersonaTrabajadorResponse:
        # Verificar si ya existe un trabajador para esta persona
        existing_trabajador = self.trabajador_repository.get_by_persona(
            trabajador_data.i_cod_persona
        )
        
        if existing_trabajador:
            return PersonaTrabajadorResponse(
                success=False,
                message="Trabajador ya existe",
                error={
                    "code": "TRB002",
                    "details": "Esta persona ya está registrada como trabajador"
                }
            )
        
        # Crear nuevo trabajador
        new_trabajador = PersonaTrabajador(
            i_cod_persona=trabajador_data.i_cod_persona,
            i_cod_unidad=trabajador_data.i_cod_unidad,
            i_cod_area=trabajador_data.i_cod_area,
            i_cod_puesto=trabajador_data.i_cod_puesto,
            i_cod_categoria=trabajador_data.i_cod_categoria,
            n_imp_sueldo=trabajador_data.n_imp_sueldo,
            t_fec_ingreso=trabajador_data.t_fec_ingreso,
            i_est_registro=1,
            v_usu_reg=audit_data["v_usu_reg"],
            v_host_reg=audit_data["v_host_reg"],
            v_ip_reg=audit_data["v_ip_reg"],
            t_fec_reg=datetime.now(timezone.utc)
        )
        
        created_trabajador = self.trabajador_repository.create(new_trabajador)
        
        return PersonaTrabajadorResponse(
            success=True,
            message="Trabajador creado exitosamente",
            data=created_trabajador
        )
    
    def update_trabajador(
        self,
        i_cod_trabajador: int,
        trabajador_data: PersonaTrabajadorUpdate,
        audit_data: dict
    ) -> PersonaTrabajadorResponse:
        trabajador = self.trabajador_repository.get_by_id(i_cod_trabajador)
        if not trabajador:
            return PersonaTrabajadorResponse(
                success=False,
                message="Trabajador no encontrado",
                error={
                    "code": "TRB001",
                    "details": f"No se encontró el trabajador con código {i_cod_trabajador}"
                }
            )
        
        # Actualizar campos si se proporcionaron
        if trabajador_data.i_cod_unidad is not None:
            trabajador.i_cod_unidad = trabajador_data.i_cod_unidad
        if trabajador_data.i_cod_area is not None:
            trabajador.i_cod_area = trabajador_data.i_cod_area
        if trabajador_data.i_cod_puesto is not None:
            trabajador.i_cod_puesto = trabajador_data.i_cod_puesto
        if trabajador_data.i_cod_categoria is not None:
            trabajador.i_cod_categoria = trabajador_data.i_cod_categoria
        if trabajador_data.n_imp_sueldo is not None:
            trabajador.n_imp_sueldo = trabajador_data.n_imp_sueldo
        if trabajador_data.t_fec_ingreso is not None:
            trabajador.t_fec_ingreso = trabajador_data.t_fec_ingreso
        
        # Actualizar campos de auditoría
        trabajador.v_usu_mod = audit_data["v_usu_mod"]
        trabajador.v_host_mod = audit_data["v_host_mod"]
        trabajador.v_ip_mod = audit_data["v_ip_mod"]
        trabajador.t_fec_mod = datetime.utcnow()
        
        updated_trabajador = self.trabajador_repository.update(trabajador)
        
        return PersonaTrabajadorResponse(
            success=True,
            message="Trabajador actualizado exitosamente",
            data=updated_trabajador
        )
    
    def delete_trabajador(
        self,
        i_cod_trabajador: int,
        audit_data: dict
    ) -> PersonaTrabajadorResponse:
        trabajador = self.trabajador_repository.get_by_id(i_cod_trabajador)
        if not trabajador:
            return PersonaTrabajadorResponse(
                success=False,
                message="Trabajador no encontrado",
                error={
                    "code": "TRB001",
                    "details": f"No se encontró el trabajador con código {i_cod_trabajador}"
                }
            )
        
        # Actualizar campos de auditoría
        trabajador.v_usu_mod = audit_data["v_usu_mod"]
        trabajador.v_host_mod = audit_data["v_host_mod"]
        trabajador.v_ip_mod = audit_data["v_ip_mod"]
        trabajador.t_fec_mod = datetime.utcnow()
        
        self.trabajador_repository.delete(trabajador)
        
        return PersonaTrabajadorResponse(
            success=True,
            message="Trabajador eliminado exitosamente"
        )
