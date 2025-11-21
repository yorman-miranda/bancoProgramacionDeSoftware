"""
API de Transacciones - Endpoints para gestión de transacciones bancarias
"""

from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.config import get_db
from crud import TransaccionCRUD, CuentaCRUD
from auth.dependencies import get_current_user, get_current_admin
from schemas import (
    TransaccionResponse,
    TransaccionCreate,
    TransaccionUpdate,
    RespuestaAPI,
)

router = APIRouter(prefix="/transacciones", tags=["transacciones"])


@router.get("/", response_model=List[TransaccionResponse])
async def obtener_transacciones(
    skip: int = 0,
    limit: int = 100,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Obtener todas las transacciones con paginación."""
    try:
        transacciones = TransaccionCRUD.get_all()
        return transacciones[skip : skip + limit]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener transacciones: {str(e)}",
        )


@router.get("/{transaccion_id}", response_model=TransaccionResponse)
async def obtener_transaccion(
    transaccion_id: UUID,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Obtener una transacción por ID."""
    try:
        transaccion = TransaccionCRUD.get_by_id(transaccion_id)
        if not transaccion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transacción no encontrada",
            )
        return transaccion
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener transacción: {str(e)}",
        )


@router.get("/cuenta/{cuenta_id}", response_model=List[TransaccionResponse])
async def obtener_transacciones_por_cuenta(
    cuenta_id: UUID,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Obtener transacciones por cuenta."""
    try:
        transacciones = TransaccionCRUD.get_by_cuenta(cuenta_id)
        return transacciones
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener transacciones por cuenta: {str(e)}",
        )


@router.post(
    "/", response_model=TransaccionResponse, status_code=status.HTTP_201_CREATED
)
async def crear_transaccion(
    transaccion_data: TransaccionCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Crear una nueva transacción."""
    try:
        # Verificar que la cuenta existe
        cuenta = CuentaCRUD.get_by_id(transaccion_data.idCuenta)
        if not cuenta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cuenta no encontrada"
            )

        # Usar create_with_session para atomicidad
        transaccion = TransaccionCRUD.create_with_session(
            session=db,
            tipo=transaccion_data.tipo,
            monto=transaccion_data.monto,
            idCuenta=transaccion_data.idCuenta,
            id_usuario_creacion=current_user.idUser,
        )

        # Hacer commit de la transacción completa
        db.commit()
        return transaccion

    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear transacción: {str(e)}",
        )


@router.put("/{transaccion_id}", response_model=TransaccionResponse)
async def actualizar_transaccion(
    transaccion_id: UUID,
    transaccion_data: TransaccionUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Actualizar una transacción existente."""
    try:
        transaccion_existente = TransaccionCRUD.get_by_id(transaccion_id)
        if not transaccion_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transacción no encontrada",
            )

        campos_actualizacion = {
            k: v
            for k, v in transaccion_data.dict(exclude_unset=True).items()
            if v is not None
        }

        if not campos_actualizacion:
            return transaccion_existente

        transaccion_actualizada = TransaccionCRUD.update(
            transaccion_id,
            id_usuario_edicion=current_user.idUser,  # ID del usuario que modifica
            **campos_actualizacion,
        )
        return transaccion_actualizada
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar transacción: {str(e)}",
        )


@router.delete("/{transaccion_id}", response_model=RespuestaAPI)
async def eliminar_transaccion(
    transaccion_id: UUID,
    current_user=Depends(get_current_admin),  # Solo admin
    db: Session = Depends(get_db),
):
    """Eliminar una transacción (solo administradores)."""
    try:
        transaccion_existente = TransaccionCRUD.get_by_id(transaccion_id)
        if not transaccion_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transacción no encontrada",
            )

        eliminada = TransaccionCRUD.delete(transaccion_id)
        if eliminada:
            return RespuestaAPI(
                mensaje="Transacción eliminada exitosamente", exito=True
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar transacción",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar transacción: {str(e)}",
        )
