from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from sqlalchemy.orm import relationship
from database.config import Base


class Empleado(Base):
    __tablename__ = "empleados"

    idEmpleado = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    cargo = Column(String(100), nullable=False)

    idSucursal = Column(UUID(as_uuid=True), ForeignKey("sucursales.idSucursal"))
    idUsuario = Column(UUID(as_uuid=True), ForeignKey("users.idUser"))

    id_usuario_creacion = Column(
        UUID(as_uuid=True), ForeignKey("users.idUser"), nullable=False
    )
    id_usuario_edicion = Column(
        UUID(as_uuid=True), ForeignKey("users.idUser"), nullable=True
    )
    fecha_creacion = Column(DateTime, default=datetime.now, nullable=False)
    fecha_actualizacion = Column(DateTime, default=None, onupdate=datetime.now)

    sucursal = relationship("Sucursal")
    usuario = relationship("User", foreign_keys=[idUsuario])
    usuario_creacion = relationship("User", foreign_keys=[id_usuario_creacion])
    usuario_edicion = relationship("User", foreign_keys=[id_usuario_edicion])

    def __repr__(self):
        return f"<Empleado {self.nombre} {self.apellido} - {self.cargo}>"
