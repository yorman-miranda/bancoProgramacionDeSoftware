"""
API de Autenticación - Endpoints para login y registro
"""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.config import get_db
from auth import PasswordManager
from schemas import UsuarioLogin, UsuarioCreate, UsuarioResponse, RespuestaAPI
from crud import UserCRUD

router = APIRouter(prefix="/auth", tags=["autenticación"])


@router.post("/login", response_model=UsuarioResponse)
async def login(login_data: UsuarioLogin, db: Session = Depends(get_db)):
    """Autenticar un usuario con nombre de usuario y contraseña."""
    try:
        user = UserCRUD.authenticate(login_data.username, login_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas",
            )
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error durante el login: {str(e)}",
        )


@router.post(
    "/registro", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED
)
async def registrar_usuario(usuario_data: UsuarioCreate, db: Session = Depends(get_db)):
    """Registrar un nuevo usuario."""
    try:
        # Verificar si el usuario ya existe
        usuario_existente = UserCRUD.get_by_username(usuario_data.username)
        if usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de usuario ya está en uso",
            )

        # Validar fortaleza de la contraseña
        es_valida, mensaje = PasswordManager.validate_password_strength(
            usuario_data.password
        )
        if not es_valida:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=mensaje)

        # Crear usuario (usando un ID de creación por defecto para el primer usuario)
        usuario = UserCRUD.create(
            firstName=usuario_data.firstName,
            lastName=usuario_data.lastName,
            username=usuario_data.username,
            password=usuario_data.password,
            id_usuario_creacion=UUID(
                "00000000-0000-0000-0000-000000000000"
            ),  # ID por defecto
        )

        return usuario
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al registrar usuario: {str(e)}",
        )


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
            },
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al verificar usuario: {str(e)}",
        )
