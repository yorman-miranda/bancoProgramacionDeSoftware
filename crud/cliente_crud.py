from entities.cliente import Cliente
from database.config import get_session
import uuid


class ClienteCRUD:
    """
    CRUD para la entidad Cliente.
    Permite crear, leer, actualizar y eliminar clientes.
    """

    @staticmethod
    def create(
        nombre,
        documento,
        telefono,
        direccion,
        email,
        idUsuario,
        idSucursal,
        id_usuario_creacion,
    ):
        """
        Crea un nuevo cliente en la base de datos.
        """
        session = get_session()
        try:
            cliente = Cliente(
                nombre=nombre,
                documento=documento,
                telefono=telefono,
                direccion=direccion,
                email=email,
                idUsuario=idUsuario,
                idSucursal=idSucursal,
                id_usuario_creacion=id_usuario_creacion,
            )
            session.add(cliente)
            session.commit()
            session.refresh(cliente)
            return cliente
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def get_by_id(cliente_id):
        """
        Obtiene un cliente por su ID.
        """
        session = get_session()
        try:
            return session.query(Cliente).filter_by(idCliente=cliente_id).first()
        finally:
            session.close()

    @staticmethod
    def get_all():
        """
        Obtiene todos los clientes registrados.
        """
        session = get_session()
        try:
            return session.query(Cliente).all()
        finally:
            session.close()

    @staticmethod
    def update(cliente_id, id_usuario_edicion, **kwargs):
        """
        Actualiza los datos de un cliente.
        """
        session = get_session()
        try:
            cliente = session.query(Cliente).filter_by(idCliente=cliente_id).first()
            if not cliente:
                return None
            for key, value in kwargs.items():
                if hasattr(cliente, key):
                    setattr(cliente, key, value)

            cliente.id_usuario_edicion = id_usuario_edicion
            session.commit()
            session.refresh(cliente)
            return cliente
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def delete(cliente_id):
        """
        Elimina un cliente de la base de datos.
        """
        session = get_session()
        try:
            cliente = session.query(Cliente).filter_by(idCliente=cliente_id).first()
            if not cliente:
                return False
            session.delete(cliente)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
