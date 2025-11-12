from datetime import datetime
from entities.user import User
from database.config import get_session
from auth.security import PasswordManager
import uuid


class UserCRUD:
    """
    CRUD para la entidad User.
    Proporciona métodos para crear, leer, actualizar y eliminar usuarios.
    """

    @staticmethod
    def create(firstName, lastName, username, password, id_usuario_creacion, **kwargs):
        """
        Crea un nuevo usuario en la base de datos.
        Acepta **kwargs para campos opcionales como 'activo' o 'es_admin'.
        """
        session = get_session()
        try:

            hashed_password = PasswordManager.hash_password(password)

            user = User(
                firstName=firstName,
                lastName=lastName,
                username=username,
                password=hashed_password,
                id_usuario_creacion=id_usuario_creacion,
                **kwargs,
            )

            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def get_by_id(user_id):
        """
        Obtiene un usuario por su ID.
        """
        session = get_session()
        try:
            return session.query(User).filter_by(idUser=user_id).first()
        finally:
            session.close()

    @staticmethod
    def get_by_username(username):
        """
        Obtiene un usuario por su nombre de usuario.
        """
        session = get_session()
        try:
            return session.query(User).filter_by(username=username).first()
        finally:
            session.close()

    @staticmethod
    def get_all():
        """
        Obtiene todos los usuarios registrados.
        """
        session = get_session()
        try:
            return session.query(User).all()
        finally:
            session.close()

    @staticmethod
    def update(user_id, id_usuario_edicion, **kwargs):
        """
        Actualiza los datos de un usuario y registra quién lo modificó.
        """
        session = get_session()
        try:
            user = session.query(User).filter_by(idUser=user_id).first()
            if not user:
                return None

            if "password" in kwargs:
                password = kwargs["password"]
                is_valid, message = PasswordManager.validate_password_strength(password)
                if not is_valid:
                    raise ValueError(f"Contraseña débil: {message}")
                kwargs["password"] = PasswordManager.hash_password(password)

            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)

            user.id_usuario_edicion = id_usuario_edicion
            user.fecha_actualizacion = datetime.now()

            session.commit()
            session.refresh(user)
            return user
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def delete(user_id):
        """
        Elimina un usuario de la base de datos.
        """
        session = get_session()
        try:
            user = session.query(User).filter_by(idUser=user_id).first()
            if not user:
                return False
            session.delete(user)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def authenticate(username, password):
        """
        Autentica un usuario con nombre de usuario y contraseña.
        """
        session = get_session()
        try:
            user = session.query(User).filter_by(username=username).first()
            if user and PasswordManager.verify_password(password, user.password):
                return user
            return None
        finally:
            session.close()