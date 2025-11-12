from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from sqlalchemy.orm import relationship
from database.config import Base


class Cliente(Base):
    """
    Entidad Cliente: representa un cliente del banco.
    Se asocia con un usuario del sistema y opcionalmente
    con una sucursal.
    """

    __tablename__ = "clientes"

    idCliente = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(100), nullable=False)
    documento = Column(String(50), unique=True, nullable=False)
    telefono = Column(String(20))
    direccion = Column(String(200))
    email = Column(String(100))

    idUsuario = Column(UUID(as_uuid=True), ForeignKey("users.idUser"))
    idSucursal = Column(
        UUID(as_uuid=True), ForeignKey("sucursales.idSucursal"), nullable=True
    )

    id_usuario_creacion = Column(
        UUID(as_uuid=True), ForeignKey("users.idUser"), nullable=False
    )
    id_usuario_edicion = Column(
        UUID(as_uuid=True), ForeignKey("users.idUser"), nullable=True
    )
    fecha_creacion = Column(DateTime, default=datetime.now, nullable=False)
    fecha_actualizacion = Column(DateTime, default=None, onupdate=datetime.now)

    usuario = relationship("User", foreign_keys=[idUsuario])
    sucursal = relationship("Sucursal")
    usuario_creacion = relationship("User", foreign_keys=[id_usuario_creacion])
    usuario_edicion = relationship("User", foreign_keys=[id_usuario_edicion])

    def __repr__(self):
        return f"<Cliente {self.nombre} ({self.documento})>"
