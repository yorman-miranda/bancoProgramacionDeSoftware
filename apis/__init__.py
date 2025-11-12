"""
Paquete de APIs para el Sistema de Gestión de Productos
"""

from .auth import router as auth_router
from .usuarios import router as usuarios_router
from .clientes import router as clientes_router
from .cuentas import router as cuentas_router
from .empleados import router as empleados_router
from .sucursales import router as sucursales_router
from .transacciones import router as transacciones_router
from .operaciones import router as operaciones_router

__all__ = [
    "auth_router",
    "usuarios_router",
    "clientes_router",
    "cuentas_router",
    "empleados_router",
    "sucursales_router",
    "transacciones_router",
    "operaciones_router",
]
