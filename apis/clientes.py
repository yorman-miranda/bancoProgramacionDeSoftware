"""
API de Clientes - Endpoints para gestión de clientes del banco
"""

from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.config import get_db
from crud import ClienteCRUD
from schemas import ClienteResponse, ClienteCreate, ClienteUpdate, RespuestaAPI

router = APIRouter(prefix="/clientes", tags=["clientes"])


@router.get("/", response_model=List[ClienteResponse])
async def obtener_clientes(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Obtener todos los clientes con paginación."""
    try:
        clientes = ClienteCRUD.get_all()
        return clientes[skip : skip + limit]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener clientes: {str(e)}",
        )


@router.get("/{cliente_id}", response_model=ClienteResponse)
async def obtener_cliente(cliente_id: UUID, db: Session = Depends(get_db)):
    """Obtener un cliente por ID."""
    try:
        cliente = ClienteCRUD.get_by_id(cliente_id)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado"
            )
        return cliente
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener cliente: {str(e)}",
        )


@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
async def crear_cliente(cliente_data: ClienteCreate, db: Session = Depends(get_db)):
    """Crear un nuevo cliente."""
    try:
        cliente = ClienteCRUD.create(
            nombre=cliente_data.nombre,
            documento=cliente_data.documento,
            telefono=cliente_data.telefono,
            direccion=cliente_data.direccion,
            email=cliente_data.email,
            idUsuario=cliente_data.idUsuario,
            idSucursal=cliente_data.idSucursal,
            id_usuario_creacion=cliente_data.idUsuario,  # Usar el mismo usuario como creador
        )
        return cliente
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear cliente: {str(e)}",
        )


@router.put("/{cliente_id}", response_model=ClienteResponse)
async def actualizar_cliente(
    cliente_id: UUID, cliente_data: ClienteUpdate, db: Session = Depends(get_db)
):
    """Actualizar un cliente existente."""
    try:
        # Verificar que el cliente existe
        cliente_existente = ClienteCRUD.get_by_id(cliente_id)
        if not cliente_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado"
            )

        # Filtrar campos None para actualización
        campos_actualizacion = {
            k: v for k, v in cliente_data.dict().items() if v is not None
        }

        if not campos_actualizacion:
            return cliente_existente

        cliente_actualizado = ClienteCRUD.update(
            cliente_id,
            id_usuario_edicion=cliente_existente.idUsuario,
            **campos_actualizacion,
        )
        return cliente_actualizado
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar cliente: {str(e)}",
        )


@router.delete("/{cliente_id}", response_model=RespuestaAPI)
async def eliminar_cliente(cliente_id: UUID, db: Session = Depends(get_db)):
    """Eliminar un cliente."""
    try:
        # Verificar que el cliente existe
        cliente_existente = ClienteCRUD.get_by_id(cliente_id)
        if not cliente_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado"
            )

        eliminado = ClienteCRUD.delete(cliente_id)
        if eliminado:
            return RespuestaAPI(mensaje="Cliente eliminado exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar cliente",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar cliente: {str(e)}",
        )
