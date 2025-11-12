"""
API de Administración - Endpoints exclusivos para administradores
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.config import get_db
from auth.dependencies import get_current_admin
from crud import UserCRUD, ClienteCRUD, CuentaCRUD, TransaccionCRUD
from schemas import RespuestaAPI

router = APIRouter(prefix="/admin", tags=["administración"])


@router.get("/dashboard", response_model=RespuestaAPI)
async def panel_administracion(current_user=Depends(get_current_admin)):
    """Panel de administración (solo para admins)."""
    try:
        total_usuarios = len(UserCRUD.get_all())
        total_clientes = len(ClienteCRUD.get_all())
        total_cuentas = len(CuentaCRUD.get_all())
        total_transacciones = len(TransaccionCRUD.get_all())

        return RespuestaAPI(
            mensaje="Panel de administración",
            exito=True,
            datos={
                "estadisticas": {
                    "total_usuarios": total_usuarios,
                    "total_clientes": total_clientes,
                    "total_cuentas": total_cuentas,
                    "total_transacciones": total_transacciones,
                },
                "usuario": {
                    "id": str(current_user.idUser),
                    "nombre": f"{current_user.firstName} {current_user.lastName}",
                    "username": current_user.username,
                    "es_admin": current_user.es_admin,
                },
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al cargar panel de administración: {str(e)}",
        )


@router.get("/usuarios/inactivos", response_model=RespuestaAPI)
async def obtener_usuarios_inactivos(current_user=Depends(get_current_admin)):
    """Obtener usuarios inactivos (solo para admins)."""
    try:
        usuarios = UserCRUD.get_all()
        usuarios_inactivos = [user for user in usuarios if not user.activo]

        return RespuestaAPI(
            mensaje=f"Se encontraron {len(usuarios_inactivos)} usuarios inactivos",
            exito=True,
            datos={
                "usuarios_inactivos": [
                    {
                        "id": str(user.idUser),
                        "nombre": f"{user.firstName} {user.lastName}",
                        "username": user.username,
                        "fecha_creacion": (
                            user.fecha_creacion.isoformat()
                            if user.fecha_creacion
                            else None
                        ),
                    }
                    for user in usuarios_inactivos
                ]
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener usuarios inactivos: {str(e)}",
        )
