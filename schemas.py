"""
Modelos Pydantic para el Sistema Bancario
"""

from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, EmailStr


# Modelos base para Usuario
class UsuarioBase(BaseModel):
    firstName: str
    lastName: str
    username: str


class UsuarioCreate(UsuarioBase):
    password: str


class UsuarioUpdate(BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    activo: Optional[bool] = None
    es_admin: Optional[bool] = None


class UsuarioResponse(UsuarioBase):
    idUser: UUID
    activo: bool
    es_admin: bool
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True


class UsuarioLogin(BaseModel):
    username: str
    password: str


class CambioContraseña(BaseModel):
    contraseña_actual: str
    nueva_contraseña: str


# Modelos para Cliente
class ClienteBase(BaseModel):
    nombre: str
    documento: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    email: Optional[str] = None
    idUsuario: UUID
    idSucursal: Optional[UUID] = None


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    documento: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    email: Optional[str] = None
    idSucursal: Optional[UUID] = None


class ClienteResponse(ClienteBase):
    idCliente: UUID
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True


# Modelos para Cuenta
class CuentaBase(BaseModel):
    numeroCuenta: str
    saldo: float = 0.0
    estado: str
    tipoCuenta: str
    idCliente: UUID


class CuentaCreate(CuentaBase):
    pass


class CuentaUpdate(BaseModel):
    numeroCuenta: Optional[str] = None
    estado: Optional[str] = None
    tipoCuenta: Optional[str] = None
    idCliente: Optional[UUID] = None


class CuentaResponse(CuentaBase):
    idCuenta: UUID
    fechaApertura: datetime
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True


# Modelos para Empleado
class EmpleadoBase(BaseModel):
    nombre: str
    apellido: str
    cargo: str
    idSucursal: UUID
    idUsuario: UUID


class EmpleadoCreate(EmpleadoBase):
    pass


class EmpleadoUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    cargo: Optional[str] = None
    idSucursal: Optional[UUID] = None


class EmpleadoResponse(EmpleadoBase):
    idEmpleado: UUID
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True


# Modelos para Sucursal
class SucursalBase(BaseModel):
    nombreSucursal: str
    ciudad: str
    direccion: str
    telefono: Optional[str] = None


class SucursalCreate(SucursalBase):
    pass


class SucursalUpdate(BaseModel):
    nombreSucursal: Optional[str] = None
    ciudad: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None


class SucursalResponse(SucursalBase):
    idSucursal: UUID
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True


# Modelos para Transacción
class TransaccionBase(BaseModel):
    tipo: str
    monto: float
    idCuenta: UUID


class TransaccionCreate(TransaccionBase):
    pass


class TransaccionUpdate(BaseModel):
    tipo: Optional[str] = None
    monto: Optional[float] = None
    idCuenta: Optional[UUID] = None


class TransaccionResponse(TransaccionBase):
    idTransaccion: UUID
    fecha: datetime
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True


# Modelos de respuesta para la API
class RespuestaAPI(BaseModel):
    mensaje: str
    exito: bool = True
    datos: Optional[dict] = None


class RespuestaError(BaseModel):
    mensaje: str
    exito: bool = False
    error: str
    codigo: int


# Modelos para operaciones bancarias
class OperacionBancaria(BaseModel):
    monto: float
    idCuenta: UUID
    descripcion: Optional[str] = None


class Transferencia(BaseModel):
    monto: float
    idCuentaOrigen: UUID
    idCuentaDestino: UUID
    descripcion: Optional[str] = None
