from entities.transaccion import Transaccion
from database.config import get_session
from sqlalchemy.orm import Session
from datetime import datetime
import uuid


class TransaccionCRUD:
    """
    CRUD para la entidad Transacción.
    Se añaden métodos para operaciones transaccionales.
    """

    @staticmethod
    def create(
        tipo: str, monto: float, idCuenta: uuid.UUID, id_usuario_creacion: uuid.UUID
    ):
        """Crea una nueva transacción en la base de datos (con nueva sesión)."""
        session = get_session()
        try:
            transaccion = Transaccion(
                tipo=tipo,
                monto=monto,
                idCuenta=idCuenta,
                id_usuario_creacion=id_usuario_creacion,
            )
            session.add(transaccion)
            session.commit()
            session.refresh(transaccion)
            return transaccion
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def create_with_session(
        session: Session,
        tipo: str,
        monto: float,
        idCuenta: uuid.UUID,
        id_usuario_creacion: uuid.UUID,
    ):
        """
        Crea una nueva transacción usando una sesión de base de datos existente.
        Es clave para asegurar la atomicidad de las operaciones bancarias.
        """
        try:
            transaccion = Transaccion(
                tipo=tipo,
                monto=monto,
                idCuenta=idCuenta,
                id_usuario_creacion=id_usuario_creacion,
            )
            session.add(transaccion)
            session.flush()  # Guarda en la sesión, pero no hace COMMIT
            return transaccion
        except Exception as e:
            raise e

    @staticmethod
    def get_by_id(transaccion_id: uuid.UUID):
        """Obtiene una transacción por su ID."""
        session = get_session()
        try:
            return (
                session.query(Transaccion)
                .filter_by(idTransaccion=transaccion_id)
                .first()
            )
        finally:
            session.close()

    @staticmethod
    def get_all():
        """Obtiene todas las transacciones registradas."""
        session = get_session()
        try:
            return session.query(Transaccion).all()
        finally:
            session.close()

    @staticmethod
    def get_by_cuenta(idCuenta: uuid.UUID):
        """Obtiene todas las transacciones de una cuenta específica."""
        session = get_session()
        try:
            return (
                session.query(Transaccion)
                .filter_by(idCuenta=idCuenta)
                .order_by(Transaccion.fecha.desc())
                .all()
            )
        finally:
            session.close()

    @staticmethod
    def update(transaccion_id: uuid.UUID, id_usuario_edicion: uuid.UUID, **kwargs):
        """Actualiza los datos de una transacción (usualmente no se usa en transacciones)."""
        session = get_session()
        try:
            transaccion = (
                session.query(Transaccion)
                .filter_by(idTransaccion=transaccion_id)
                .first()
            )
            if not transaccion:
                return None
            for key, value in kwargs.items():
                if hasattr(transaccion, key):
                    setattr(transaccion, key, value)

            transaccion.id_usuario_edicion = id_usuario_edicion
            transaccion.fecha_actualizacion = datetime.now()
            session.commit()
            session.refresh(transaccion)
            return transaccion
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def delete(transaccion_id: uuid.UUID):
        """Elimina una transacción de la base de datos (usualmente no permitido)."""
        session = get_session()
        try:
            transaccion = (
                session.query(Transaccion)
                .filter_by(idTransaccion=transaccion_id)
                .first()
            )
            if not transaccion:
                return False
            session.delete(transaccion)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()