"""
Módulo de autenticación para el sistema bancario.
"""

from crud.user_crud import UserCRUD


class AuthSystem:
    """
    Sistema de autenticación para usuarios.
    """

    @staticmethod
    def login(username, password):
        """
        Autentica a un usuario.
        """
        return UserCRUD.authenticate(username, password)

    @staticmethod
    def register(firstName, lastName, username, password, id_usuario_creacion=None):
        """
        Registra un nuevo usuario.
        """
        if UserCRUD.get_by_username(username):
            return None

        return UserCRUD.create(
            firstName=firstName,
            lastName=lastName,
            username=username,
            password=password,
            id_usuario_creacion=id_usuario_creacion,
        )
