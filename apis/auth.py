"""
API de Autenticación - Endpoints para login y registro
"""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.config import get_db
from auth.security import PasswordManager
from auth.jwt_handler import create_access_token
from schemas import UsuarioLogin, UsuarioCreate, UsuarioResponse, RespuestaAPI
from crud import UserCRUD
from auth.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["autenticación"])


@router.post("/login")
async def login(login_data: UsuarioLogin, db: Session = Depends(get_db)):
    """Autenticar un usuario y devolver token."""
    try:
        user = UserCRUD.authenticate(login_data.username, login_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas",
            )

        if not user.activo:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario inactivo",
            )

        # Crear token
        access_token = create_access_token(
            data={
                "sub": user.username,
                "user_id": str(user.idUser),
                "es_admin": user.es_admin,
            }
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": str(user.idUser),
                "username": user.username,
                "firstName": user.firstName,
                "lastName": user.lastName,
                "es_admin": user.es_admin,
            },
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error durante el login: {str(e)}",
        )


@router.post(
    "/registro", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED
)
async def registrar_usuario(usuario_data: UsuarioCreate, db: Session = Depends(get_db)):
    """Registrar un nuevo usuario (público)."""
    try:
        usuario_existente = UserCRUD.get_by_username(usuario_data.username)
        if usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de usuario ya está en uso",
            )

        es_valida, mensaje = PasswordManager.validate_password_strength(
            usuario_data.password
        )
        if not es_valida:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=mensaje)

        usuario = UserCRUD.create(
            firstName=usuario_data.firstName,
            lastName=usuario_data.lastName,
            username=usuario_data.username,
            password=usuario_data.password,
            id_usuario_creacion=None,  # NULL para usuarios que se auto-registran
            es_admin=False,  # Por defecto no es admin
        )

        return usuario
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al registrar usuario: {str(e)}",
        )


@router.get("/me", response_model=UsuarioResponse)
async def obtener_usuario_actual(current_user=Depends(get_current_user)):
    """Obtener información del usuario actual."""
    return current_user


@router.get("/verificar/{usuario_id}", response_model=RespuestaAPI)
async def verificar_usuario(usuario_id: UUID, db: Session = Depends(get_db)):
    """Verificar si un usuario existe."""
    try:
        usuario = UserCRUD.get_by_id(usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )

        return RespuestaAPI(
            mensaje="Usuario verificado exitosamente",
            exito=True,
            datos={
                "usuario_id": str(usuario.idUser),
                "nombre": f"{usuario.firstName} {usuario.lastName}",
                "username": usuario.username,
                "activo": usuario.activo,
                "es_admin": usuario.es_admin,
            },
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al verificar usuario: {str(e)}",
        )
