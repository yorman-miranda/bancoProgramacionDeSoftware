from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.config import get_db
from crud import CuentaCRUD, TransaccionCRUD
from auth.dependencies import get_current_user
from schemas import OperacionBancaria, Transferencia, RespuestaAPI

router = APIRouter(prefix="/operaciones", tags=["operaciones bancarias"])


@router.post("/deposito", response_model=RespuestaAPI)
async def realizar_deposito(
    operacion: OperacionBancaria,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Realizar un depósito en una cuenta."""
    try:
        # Usar create_with_session para atomicidad
        transaccion = TransaccionCRUD.create_with_session(
            session=db,
            tipo="DEPOSITO",
            monto=operacion.monto,
            idCuenta=operacion.idCuenta,
            id_usuario_creacion=current_user.idUser,
        )

        db.commit()

        return RespuestaAPI(
            mensaje=f"Depósito de {operacion.monto} realizado exitosamente",
            exito=True,
            datos={
                "transaccion_id": str(transaccion.idTransaccion),
            },
        )
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al realizar depósito: {str(e)}",
        )


@router.post("/retiro", response_model=RespuestaAPI)
async def realizar_retiro(
    operacion: OperacionBancaria,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Realizar un retiro de una cuenta."""
    try:
        # Usar create_with_session para atomicidad
        transaccion = TransaccionCRUD.create_with_session(
            session=db,
            tipo="RETIRO",
            monto=operacion.monto,
            idCuenta=operacion.idCuenta,
            id_usuario_creacion=current_user.idUser,
        )

        db.commit()

        return RespuestaAPI(
            mensaje=f"Retiro de {operacion.monto} realizado exitosamente",
            exito=True,
            datos={
                "transaccion_id": str(transaccion.idTransaccion),
            },
        )
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al realizar retiro: {str(e)}",
        )
