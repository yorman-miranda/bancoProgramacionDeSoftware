from entities.empleado import Empleado
from database.config import get_session
import uuid


class EmpleadoCRUD:
    """
    CRUD para la entidad Empleado.
    Permite crear, leer, actualizar y eliminar empleados.
    """

    # crud/empleado_crud.py - modificar el método create
    @staticmethod
    def create(nombre, apellido, cargo, idSucursal, idUsuario, id_usuario_creacion):
        """
        Crea un nuevo empleado en la base de datos.
        """
        session = get_session()
        try:
            empleado = Empleado(
                nombre=nombre,
                apellido=apellido,
                cargo=cargo,
                idSucursal=idSucursal,
                idUsuario=idUsuario,  
                id_usuario_creacion=id_usuario_creacion,
            )
            session.add(empleado)
            session.commit()
            session.refresh(empleado)
            return empleado
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def get_by_id(empleado_id):
        """
        Obtiene un empleado por su ID.
        """
        session = get_session()
        try:
            return session.query(Empleado).filter_by(idEmpleado=empleado_id).first()
        finally:
            session.close()

    @staticmethod
    def get_all():
        """
        Obtiene todos los empleados registrados.
        """
        session = get_session()
        try:
            return session.query(Empleado).all()
        finally:
            session.close()

    @staticmethod
    def update(empleado_id, id_usuario_edicion, **kwargs):
        """
        Actualiza los datos de un empleado.
        """
        session = get_session()
        try:
            empleado = session.query(Empleado).filter_by(idEmpleado=empleado_id).first()
            if not empleado:
                return None
            for key, value in kwargs.items():
                if hasattr(empleado, key):
                    setattr(empleado, key, value)

            empleado.id_usuario_edicion = id_usuario_edicion
            session.commit()
            session.refresh(empleado)
            return empleado
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def delete(empleado_id):
        """
        Elimina un empleado de la base de datos.
        """
        session = get_session()
        try:
            empleado = session.query(Empleado).filter_by(idEmpleado=empleado_id).first()
            if not empleado:
                return False
            session.delete(empleado)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()