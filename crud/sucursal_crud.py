from entities.sucursal import Sucursal
from database.config import get_session
import uuid


class SucursalCRUD:
    """
    CRUD para la entidad Sucursal.
    Permite crear, leer, actualizar y eliminar sucursales.
    """

    @staticmethod
    def create(nombreSucursal, ciudad, direccion, telefono, id_usuario_creacion):
        """
        Crea una nueva sucursal en la base de datos.
        """
        session = get_session()
        try:
            sucursal = Sucursal(
                nombreSucursal=nombreSucursal,
                ciudad=ciudad,
                direccion=direccion,
                telefono=telefono,
                id_usuario_creacion=id_usuario_creacion,
            )
            session.add(sucursal)
            session.commit()
            session.refresh(sucursal)
            return sucursal
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def get_by_id(sucursal_id):
        """
        Obtiene una sucursal por su ID.
        """
        session = get_session()
        try:
            return session.query(Sucursal).filter_by(idSucursal=sucursal_id).first()
        finally:
            session.close()

    @staticmethod
    def get_all():
        """
        Obtiene todas las sucursales registradas.
        """
        session = get_session()
        try:
            return session.query(Sucursal).all()
        finally:
            session.close()

    @staticmethod
    def update(sucursal_id, id_usuario_edicion, **kwargs):
        """
        Actualiza los datos de una sucursal.
        """
        session = get_session()
        try:
            sucursal = session.query(Sucursal).filter_by(idSucursal=sucursal_id).first()
            if not sucursal:
                return None
            for key, value in kwargs.items():
                if hasattr(sucursal, key):
                    setattr(sucursal, key, value)

            sucursal.id_usuario_edicion = id_usuario_edicion
            session.commit()
            session.refresh(sucursal)
            return sucursal
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def delete(sucursal_id):
        """
        Elimina una sucursal de la base de datos.
        """
        session = get_session()
        try:
            sucursal = session.query(Sucursal).filter_by(idSucursal=sucursal_id).first()
            if not sucursal:
                return False
            session.delete(sucursal)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()