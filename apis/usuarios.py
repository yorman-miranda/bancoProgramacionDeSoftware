"""
API de Usuarios - Endpoints para gestión de usuarios del sistema
"""

from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.config import get_db
from crud import UserCRUD
from auth import PasswordManager
from schemas import (
    UsuarioResponse,
    UsuarioCreate,
    UsuarioUpdate,
    RespuestaAPI,
    CambioContraseña,
)

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.get("/", response_model=List[UsuarioResponse])
async def obtener_usuarios(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Obtener todos los usuarios con paginación."""
    try:
        usuarios = UserCRUD.get_all()
        return usuarios[skip : skip + limit]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener usuarios: {str(e)}",
        )


@router.get("/{usuario_id}", response_model=UsuarioResponse)
async def obtener_usuario(usuario_id: UUID, db: Session = Depends(get_db)):
    """Obtener un usuario por ID."""
    try:
        usuario = UserCRUD.get_by_id(usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )
        return usuario
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener usuario: {str(e)}",
        )


@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario_data: UsuarioCreate, db: Session = Depends(get_db)):
    """Crear un nuevo usuario."""
    try:
        # Verificar si el usuario ya existe
        usuario_existente = UserCRUD.get_by_username(usuario_data.username)
        if usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de usuario ya está en uso",
            )

        usuario = UserCRUD.create(
            firstName=usuario_data.firstName,
            lastName=usuario_data.lastName,
            username=usuario_data.username,
            password=usuario_data.password,
            id_usuario_creacion=None,
        )
        return usuario
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear usuario: {str(e)}",
        )


@router.put("/{usuario_id}", response_model=UsuarioResponse)
async def actualizar_usuario(
    usuario_id: UUID, usuario_data: UsuarioUpdate, db: Session = Depends(get_db)
):
    """Actualizar un usuario existente."""
    try:
        # Verificar que el usuario existe
        usuario_existente = UserCRUD.get_by_id(usuario_id)
        if not usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )

        # Filtrar campos None para actualización
        campos_actualizacion = {
            k: v for k, v in usuario_data.dict().items() if v is not None
        }

        if not campos_actualizacion:
            return usuario_existente

        usuario_actualizado = UserCRUD.update(
            usuario_id,
            id_usuario_edicion=usuario_id,
            **campos_actualizacion,
        )
        return usuario_actualizado
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar usuario: {str(e)}",
        )


@router.delete("/{usuario_id}", response_model=RespuestaAPI)
async def eliminar_usuario(usuario_id: UUID, db: Session = Depends(get_db)):
    """Eliminar un usuario."""
    try:
        # Verificar que el usuario existe
        usuario_existente = UserCRUD.get_by_id(usuario_id)
        if not usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )

        eliminado = UserCRUD.delete(usuario_id)
        if eliminado:
            return RespuestaAPI(mensaje="Usuario eliminado exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar usuario",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar usuario: {str(e)}",
        )


@router.post("/{usuario_id}/cambiar-contraseña", response_model=RespuestaAPI)
async def cambiar_contraseña(
    usuario_id: UUID, cambio_data: CambioContraseña, db: Session = Depends(get_db)
):
    """Cambiar la contraseña de un usuario."""
    try:
        # Verificar que el usuario existe
        usuario_existente = UserCRUD.get_by_id(usuario_id)
        if not usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )

        # Verificar contraseña actual
        if not UserCRUD.authenticate(
            usuario_existente.username, cambio_data.contraseña_actual
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Contraseña actual incorrecta",
            )

        # Validar nueva contraseña
        es_valida, mensaje = PasswordManager.validate_password_strength(
            cambio_data.nueva_contraseña
        )
        if not es_valida:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=mensaje)

        # Actualizar contraseña
        usuario_actualizado = UserCRUD.update(
            usuario_id,
            id_usuario_edicion=usuario_id,
            password=cambio_data.nueva_contraseña,
        )

        if usuario_actualizado:
            return RespuestaAPI(mensaje="Contraseña cambiada exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al cambiar contraseña",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al cambiar contraseña: {str(e)}",
        )
