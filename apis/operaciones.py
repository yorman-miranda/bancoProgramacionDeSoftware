"""
API de Operaciones Bancarias - Endpoints para operaciones específicas del banco
"""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.config import get_db
from crud import CuentaCRUD, TransaccionCRUD
from schemas import OperacionBancaria, Transferencia, RespuestaAPI

router = APIRouter(prefix="/operaciones", tags=["operaciones bancarias"])


@router.post("/deposito", response_model=RespuestaAPI)
async def realizar_deposito(
    operacion: OperacionBancaria, db: Session = Depends(get_db)
):
    """Realizar un depósito en una cuenta."""
    try:
        # Verificar que la cuenta existe
        cuenta = CuentaCRUD.get_by_id(operacion.idCuenta)
        if not cuenta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cuenta no encontrada"
            )

        # Realizar depósito (aquí deberías implementar la lógica transaccional)
        # Esta es una implementación básica - deberías usar sesiones transaccionales

        # Crear transacción de depósito
        transaccion = TransaccionCRUD.create(
            tipo="DEPOSITO",
            monto=operacion.monto,
            idCuenta=operacion.idCuenta,
            id_usuario_creacion=UUID("00000000-0000-0000-0000-000000000000"),
        )

        # Actualizar saldo de la cuenta (implementación simplificada)
        nuevo_saldo = cuenta.saldo + operacion.monto
        CuentaCRUD.update(
            operacion.idCuenta,
            id_usuario_edicion=cuenta.id_usuario_creacion,
            saldo=nuevo_saldo,
        )

        return RespuestaAPI(
            mensaje=f"Depósito de {operacion.monto} realizado exitosamente",
            exito=True,
            datos={
                "nuevo_saldo": nuevo_saldo,
                "transaccion_id": str(transaccion.idTransaccion),
            },
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al realizar depósito: {str(e)}",
        )


@router.post("/retiro", response_model=RespuestaAPI)
async def realizar_retiro(operacion: OperacionBancaria, db: Session = Depends(get_db)):
    """Realizar un retiro de una cuenta."""
    try:
        # Verificar que la cuenta existe
        cuenta = CuentaCRUD.get_by_id(operacion.idCuenta)
        if not cuenta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cuenta no encontrada"
            )

        # Verificar fondos suficientes
        if cuenta.saldo < operacion.monto:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Fondos insuficientes"
            )

        # Crear transacción de retiro
        transaccion = TransaccionCRUD.create(
            tipo="RETIRO",
            monto=operacion.monto,
            idCuenta=operacion.idCuenta,
            id_usuario_creacion=UUID("00000000-0000-0000-0000-000000000000"),
        )

        # Actualizar saldo de la cuenta
        nuevo_saldo = cuenta.saldo - operacion.monto
        CuentaCRUD.update(
            operacion.idCuenta,
            id_usuario_edicion=cuenta.id_usuario_creacion,
            saldo=nuevo_saldo,
        )

        return RespuestaAPI(
            mensaje=f"Retiro de {operacion.monto} realizado exitosamente",
            exito=True,
            datos={
                "nuevo_saldo": nuevo_saldo,
                "transaccion_id": str(transaccion.idTransaccion),
            },
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al realizar retiro: {str(e)}",
        )
