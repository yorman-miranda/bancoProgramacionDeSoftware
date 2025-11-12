"""
API de Cuentas - Endpoints para gestión de cuentas bancarias
"""

from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.config import get_db
from crud import CuentaCRUD
from schemas import CuentaResponse, CuentaCreate, CuentaUpdate, RespuestaAPI

router = APIRouter(prefix="/cuentas", tags=["cuentas"])


@router.get("/", response_model=List[CuentaResponse])
async def obtener_cuentas(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Obtener todas las cuentas con paginación."""
    try:
        cuentas = CuentaCRUD.get_all()
        return cuentas[skip : skip + limit]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener cuentas: {str(e)}",
        )


@router.get("/{cuenta_id}", response_model=CuentaResponse)
async def obtener_cuenta(cuenta_id: UUID, db: Session = Depends(get_db)):
    """Obtener una cuenta por ID."""
    try:
        cuenta = CuentaCRUD.get_by_id(cuenta_id)
        if not cuenta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cuenta no encontrada"
            )
        return cuenta
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener cuenta: {str(e)}",
        )


@router.get("/numero/{numero_cuenta}", response_model=CuentaResponse)
async def obtener_cuenta_por_numero(numero_cuenta: str, db: Session = Depends(get_db)):
    """Obtener una cuenta por número de cuenta."""
    try:
        cuenta = CuentaCRUD.get_by_numero(numero_cuenta)
        if not cuenta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cuenta no encontrada"
            )
        return cuenta
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener cuenta: {str(e)}",
        )


@router.post("/", response_model=CuentaResponse, status_code=status.HTTP_201_CREATED)
async def crear_cuenta(cuenta_data: CuentaCreate, db: Session = Depends(get_db)):
    """Crear una nueva cuenta bancaria."""
    try:
        cuenta = CuentaCRUD.create(
            numeroCuenta=cuenta_data.numeroCuenta,
            saldo=cuenta_data.saldo,
            estado=cuenta_data.estado,
            tipoCuenta=cuenta_data.tipoCuenta,
            idCliente=cuenta_data.idCliente,
            id_usuario_creacion=cuenta_data.idUser,  # Usar el cliente como creador
        )
        return cuenta
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear cuenta: {str(e)}",
        )


@router.put("/{cuenta_id}", response_model=CuentaResponse)
async def actualizar_cuenta(
    cuenta_id: UUID, cuenta_data: CuentaUpdate, db: Session = Depends(get_db)
):
    """Actualizar una cuenta existente."""
    try:
        # Verificar que la cuenta existe
        cuenta_existente = CuentaCRUD.get_by_id(cuenta_id)
        if not cuenta_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cuenta no encontrada"
            )

        # Filtrar campos None para actualización
        campos_actualizacion = {
            k: v for k, v in cuenta_data.dict().items() if v is not None
        }

        if not campos_actualizacion:
            return cuenta_existente

        cuenta_actualizada = CuentaCRUD.update(
            cuenta_id,
            id_usuario_edicion=cuenta_existente.id_usuario_creacion,
            **campos_actualizacion,
        )
        return cuenta_actualizada
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar cuenta: {str(e)}",
        )


@router.delete("/{cuenta_id}", response_model=RespuestaAPI)
async def eliminar_cuenta(cuenta_id: UUID, db: Session = Depends(get_db)):
    """Eliminar una cuenta."""
    try:
        # Verificar que la cuenta existe
        cuenta_existente = CuentaCRUD.get_by_id(cuenta_id)
        if not cuenta_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cuenta no encontrada"
            )

        eliminado = CuentaCRUD.delete(cuenta_id)
        if eliminado:
            return RespuestaAPI(mensaje="Cuenta eliminada exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar cuenta",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar cuenta: {str(e)}",
        )
