
from entities.cuenta import Cuenta
from database.config import get_session
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from sqlalchemy import text


class CuentaCRUD:
    """
    CRUD para la entidad Cuenta.
    Permite crear, leer, actualizar y eliminar cuentas bancarias.
    """

    @staticmethod
    def create(
        numeroCuenta: str,
        saldo: float,
        estado: str,
        tipoCuenta: str,
        idCliente: uuid.UUID,
        id_usuario_creacion: uuid.UUID,
    ):
        """Crea una nueva cuenta bancaria."""
        session = get_session()
        try:
            cuenta = Cuenta(
                numeroCuenta=numeroCuenta,
                saldo=saldo,
                estado=estado,
                tipoCuenta=tipoCuenta,
                idCliente=idCliente,
                id_usuario_creacion=id_usuario_creacion,
            )
            session.add(cuenta)
            session.commit()
            session.refresh(cuenta)
            return cuenta
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def get_by_id(cuenta_id: uuid.UUID):
        """Obtiene una cuenta bancaria por su ID."""
        session = get_session()
        try:
            return session.query(Cuenta).filter_by(idCuenta=cuenta_id).first()
        finally:
            session.close()

    @staticmethod
    def get_by_numero(
        numero_cuenta: str, session: Session = None, for_update: bool = False
    ):
        """
        Obtiene una cuenta bancaria por su número.
        Permite bloquear la fila para transacciones (for_update=True).
        """
        session_to_use = session if session else get_session()
        try:
            query = session_to_use.query(Cuenta).filter_by(numeroCuenta=numero_cuenta)
            if for_update:
                query = query.with_for_update()
            return query.first()
        finally:
            if not session:
                session_to_use.close()

    @staticmethod
    def get_all():
        """Obtiene todas las cuentas bancarias registradas."""
        session = get_session()
        try:
            return session.query(Cuenta).all()
        finally:
            session.close()

    @staticmethod
    def update(cuenta_id: uuid.UUID, id_usuario_edicion: uuid.UUID, **kwargs):
        """Actualiza los datos de una cuenta bancaria (excluye el saldo, que se actualiza con _update_balance)."""
        session = get_session()
        try:
            cuenta = session.query(Cuenta).filter_by(idCuenta=cuenta_id).first()
            if not cuenta:
                return None

            kwargs.pop("saldo", None)

            for key, value in kwargs.items():
                if hasattr(cuenta, key):
                    setattr(cuenta, key, value)

            cuenta.id_usuario_edicion = id_usuario_edicion
            cuenta.fecha_actualizacion = datetime.now()
            session.commit()
            session.refresh(cuenta)
            return cuenta
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def _update_balance(
        session: Session,
        cuenta_id: uuid.UUID,
        monto_cambio: float,
        id_usuario_edicion: uuid.UUID,
    ):
        """
        Método INTERNO para actualizar el saldo de una cuenta.
        DEBE ser llamado dentro de una sesión de transacción existente.
        """
        cuenta = (
            session.query(Cuenta)
            .filter_by(idCuenta=cuenta_id)
            .with_for_update()
            .first()
        )
        if not cuenta:
            raise ValueError("Cuenta no encontrada.")

        nuevo_saldo = cuenta.saldo + monto_cambio

        if monto_cambio < 0 and nuevo_saldo < 0:
            raise ValueError(
                f"Saldo insuficiente. Saldo actual: {cuenta.saldo:,.2f}. Monto a retirar: {-monto_cambio:,.2f}."
            )

        cuenta.saldo = nuevo_saldo
        cuenta.id_usuario_edicion = id_usuario_edicion
        cuenta.fecha_actualizacion = datetime.now()
        session.flush()
        return cuenta

    @staticmethod
    def delete(cuenta_id: uuid.UUID):
        """Elimina una cuenta bancaria."""
        session = get_session()
        try:
            cuenta = session.query(Cuenta).filter_by(idCuenta=cuenta_id).first()
            if not cuenta:
                return False
            session.delete(cuenta)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
