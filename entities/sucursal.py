from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from sqlalchemy.orm import relationship
from database.config import Base


class Sucursal(Base):
    """
    Entidad Sucursal: representa una oficina o
    sucursal física del banco.
    """

    __tablename__ = "sucursales"

    idSucursal = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombreSucursal = Column(String(100), nullable=False)
    ciudad = Column(String(100), nullable=False)
    direccion = Column(String(200), nullable=False)
    telefono = Column(String(20))

    id_usuario_creacion = Column(
        UUID(as_uuid=True), ForeignKey("users.idUser"), nullable=False
    )
    id_usuario_edicion = Column(
        UUID(as_uuid=True), ForeignKey("users.idUser"), nullable=True
    )
    fecha_creacion = Column(DateTime, default=datetime.now, nullable=False)
    fecha_actualizacion = Column(DateTime, default=None, onupdate=datetime.now)

    usuario_creacion = relationship("User", foreign_keys=[id_usuario_creacion])
    usuario_edicion = relationship("User", foreign_keys=[id_usuario_edicion])

    def __repr__(self):
        return f"<Sucursal {self.nombreSucursal} ({self.ciudad})>"