"""
API de Sucursales - Endpoints para gestión de sucursales del banco
"""

from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.config import get_db
from crud import SucursalCRUD
from schemas import SucursalResponse, SucursalCreate, SucursalUpdate, RespuestaAPI

router = APIRouter(prefix="/sucursales", tags=["sucursales"])


@router.get("/", response_model=List[SucursalResponse])
async def obtener_sucursales(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Obtener todas las sucursales con paginación."""
    try:
        sucursales = SucursalCRUD.get_all()
        return sucursales[skip : skip + limit]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener sucursales: {str(e)}",
        )


@router.get("/{sucursal_id}", response_model=SucursalResponse)
async def obtener_sucursal(sucursal_id: UUID, db: Session = Depends(get_db)):
    """Obtener una sucursal por ID."""
    try:
        sucursal = SucursalCRUD.get_by_id(sucursal_id)
        if not sucursal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Sucursal no encontrada"
            )
        return sucursal
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener sucursal: {str(e)}",
        )


@router.get("/ciudad/{ciudad}", response_model=List[SucursalResponse])
async def obtener_sucursales_por_ciudad(ciudad: str, db: Session = Depends(get_db)):
    """Obtener sucursales por ciudad."""
    try:
        sucursales = SucursalCRUD.get_all()
        sucursales_ciudad = [
            suc for suc in sucursales if suc.ciudad.lower() == ciudad.lower()
        ]
        return sucursales_ciudad
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener sucursales por ciudad: {str(e)}",
        )


@router.post("/", response_model=SucursalResponse, status_code=status.HTTP_201_CREATED)
async def crear_sucursal(sucursal_data: SucursalCreate, db: Session = Depends(get_db)):
    """Crear una nueva sucursal."""
    try:
        sucursal = SucursalCRUD.create(
            nombreSucursal=sucursal_data.nombreSucursal,
            ciudad=sucursal_data.ciudad,
            direccion=sucursal_data.direccion,
            telefono=sucursal_data.telefono,
            id_usuario_creacion=UUID(""),  # Admin por defecto
        )
        return sucursal
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear sucursal: {str(e)}",
        )


@router.put("/{sucursal_id}", response_model=SucursalResponse)
async def actualizar_sucursal(
    sucursal_id: UUID, sucursal_data: SucursalUpdate, db: Session = Depends(get_db)
):
    """Actualizar una sucursal existente."""
    try:
        # Verificar que la sucursal existe
        sucursal_existente = SucursalCRUD.get_by_id(sucursal_id)
        if not sucursal_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Sucursal no encontrada"
            )

        # Filtrar campos None para actualización
        campos_actualizacion = {
            k: v for k, v in sucursal_data.dict().items() if v is not None
        }

        if not campos_actualizacion:
            return sucursal_existente

        sucursal_actualizada = SucursalCRUD.update(
            sucursal_id,
            id_usuario_edicion=sucursal_existente.id_usuario_creacion,
            **campos_actualizacion,
        )
        return sucursal_actualizada
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar sucursal: {str(e)}",
        )


@router.delete("/{sucursal_id}", response_model=RespuestaAPI)
async def eliminar_sucursal(sucursal_id: UUID, db: Session = Depends(get_db)):
    """Eliminar una sucursal."""
    try:
        # Verificar que la sucursal existe
        sucursal_existente = SucursalCRUD.get_by_id(sucursal_id)
        if not sucursal_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Sucursal no encontrada"
            )

        eliminada = SucursalCRUD.delete(sucursal_id)
        if eliminada:
            return RespuestaAPI(mensaje="Sucursal eliminada exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar sucursal",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar sucursal: {str(e)}",
        )
