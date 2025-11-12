"""
API de Empleados - Endpoints para gestión de empleados del banco
"""

from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.config import get_db
from crud import EmpleadoCRUD
from auth.dependencies import get_current_user, get_current_admin
from schemas import EmpleadoResponse, EmpleadoCreate, EmpleadoUpdate, RespuestaAPI

router = APIRouter(prefix="/empleados", tags=["empleados"])


@router.get("/", response_model=List[EmpleadoResponse])
async def obtener_empleados(
    skip: int = 0,
    limit: int = 100,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Obtener todos los empleados con paginación."""
    try:
        empleados = EmpleadoCRUD.get_all()
        return empleados[skip : skip + limit]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener empleados: {str(e)}",
        )


@router.get("/{empleado_id}", response_model=EmpleadoResponse)
async def obtener_empleado(
    empleado_id: UUID,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Obtener un empleado por ID."""
    try:
        empleado = EmpleadoCRUD.get_by_id(empleado_id)
        if not empleado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Empleado no encontrado"
            )
        return empleado
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener empleado: {str(e)}",
        )


@router.get("/sucursal/{sucursal_id}", response_model=List[EmpleadoResponse])
async def obtener_empleados_por_sucursal(
    sucursal_id: UUID,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Obtener empleados por sucursal."""
    try:
        empleados = EmpleadoCRUD.get_all()
        empleados_sucursal = [
            emp for emp in empleados if str(emp.idSucursal) == str(sucursal_id)
        ]
        return empleados_sucursal
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener empleados por sucursal: {str(e)}",
        )


@router.post("/", response_model=EmpleadoResponse, status_code=status.HTTP_201_CREATED)
async def crear_empleado(
    empleado_data: EmpleadoCreate,
    current_user=Depends(get_current_admin),  # Solo admin
    db: Session = Depends(get_db),
):
    """Crear un nuevo empleado (solo administradores)."""
    try:
        empleado = EmpleadoCRUD.create(
            nombre=empleado_data.nombre,
            apellido=empleado_data.apellido,
            cargo=empleado_data.cargo,
            idSucursal=empleado_data.idSucursal,
            idUsuario=empleado_data.idUsuario,
            id_usuario_creacion=current_user.idUser,  # ID del admin que crea
        )
        return empleado
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear empleado: {str(e)}",
        )


@router.put("/{empleado_id}", response_model=EmpleadoResponse)
async def actualizar_empleado(
    empleado_id: UUID,
    empleado_data: EmpleadoUpdate,
    current_user=Depends(get_current_admin),  # Solo admin
    db: Session = Depends(get_db),
):
    """Actualizar un empleado existente (solo administradores)."""
    try:
        empleado_existente = EmpleadoCRUD.get_by_id(empleado_id)
        if not empleado_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Empleado no encontrado"
            )

        campos_actualizacion = {
            k: v
            for k, v in empleado_data.dict(exclude_unset=True).items()
            if v is not None
        }

        if not campos_actualizacion:
            return empleado_existente

        empleado_actualizado = EmpleadoCRUD.update(
            empleado_id,
            id_usuario_edicion=current_user.idUser,  # ID del admin que modifica
            **campos_actualizacion,
        )
        return empleado_actualizado
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar empleado: {str(e)}",
        )


@router.delete("/{empleado_id}", response_model=RespuestaAPI)
async def eliminar_empleado(
    empleado_id: UUID,
    current_user=Depends(get_current_admin),  # Solo admin
    db: Session = Depends(get_db),
):
    """Eliminar un empleado (solo administradores)."""
    try:
        empleado_existente = EmpleadoCRUD.get_by_id(empleado_id)
        if not empleado_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Empleado no encontrado"
            )

        eliminado = EmpleadoCRUD.delete(empleado_id)
        if eliminado:
            return RespuestaAPI(mensaje="Empleado eliminado exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar empleado",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar empleado: {str(e)}",
        )
