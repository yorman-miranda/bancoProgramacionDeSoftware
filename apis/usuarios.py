"""
API de Usuarios - Endpoints para gestión de usuarios del sistema
"""

from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.config import get_db
from crud import UserCRUD
from auth.security import PasswordManager
from auth.dependencies import get_current_user, get_current_admin
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
    skip: int = 0,
    limit: int = 100,
    current_user=Depends(get_current_admin),  # Solo admin
    db: Session = Depends(get_db),
):
    """Obtener todos los usuarios con paginación (solo administradores)."""
    try:
        usuarios = UserCRUD.get_all()
        return usuarios[skip : skip + limit]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener usuarios: {str(e)}",
        )


@router.get("/{usuario_id}", response_model=UsuarioResponse)
async def obtener_usuario(
    usuario_id: UUID,
    current_user=Depends(get_current_user),  # Cualquier usuario autenticado
    db: Session = Depends(get_db),
):
    """Obtener un usuario por ID."""
    try:
        # Usuarios normales solo pueden ver su propio perfil
        if not current_user.es_admin and str(current_user.idUser) != str(usuario_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No puede ver información de otros usuarios",
            )

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
async def crear_usuario(
    usuario_data: UsuarioCreate,
    current_user=Depends(get_current_admin),  # Solo admin
    db: Session = Depends(get_db),
):
    """Crear un nuevo usuario (solo administradores)."""
    try:
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
            id_usuario_creacion=current_user.idUser,  # ID del admin que crea
            es_admin=(
                usuario_data.es_admin if hasattr(usuario_data, "es_admin") else False
            ),
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
    usuario_id: UUID,
    usuario_data: UsuarioUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Actualizar un usuario existente."""
    try:
        # Usuarios normales solo pueden actualizar su propio perfil
        if not current_user.es_admin and str(current_user.idUser) != str(usuario_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No puede actualizar otros usuarios",
            )

        # Verificar que el usuario existe
        usuario_existente = UserCRUD.get_by_id(usuario_id)
        if not usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )

        # Usuarios normales no pueden cambiar el campo es_admin
        if not current_user.es_admin and hasattr(usuario_data, "es_admin"):
            usuario_data.es_admin = None

        # Filtrar campos None para actualización
        campos_actualizacion = {
            k: v
            for k, v in usuario_data.dict(exclude_unset=True).items()
            if v is not None
        }

        if not campos_actualizacion:
            return usuario_existente

        usuario_actualizado = UserCRUD.update(
            usuario_id,
            id_usuario_edicion=current_user.idUser,  # ID del usuario que modifica
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
async def eliminar_usuario(
    usuario_id: UUID,
    current_user=Depends(get_current_admin),  # Solo admin
    db: Session = Depends(get_db),
):
    """Eliminar un usuario (solo administradores)."""
    try:
        # No permitir auto-eliminación
        if str(current_user.idUser) == str(usuario_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No puede eliminarse a sí mismo",
            )

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
    usuario_id: UUID,
    cambio_data: CambioContraseña,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Cambiar la contraseña de un usuario."""
    try:
        # Usuarios normales solo pueden cambiar su propia contraseña
        if not current_user.es_admin and str(current_user.idUser) != str(usuario_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No puede cambiar contraseña de otros usuarios",
            )

        usuario_existente = UserCRUD.get_by_id(usuario_id)
        if not usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )

        # Si no es admin, verificar contraseña actual
        if not current_user.es_admin:
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
            id_usuario_edicion=current_user.idUser,
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
