from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from sqlalchemy.orm import relationship
from database.config import Base


class Transaccion(Base):
    """
    Entidad Transaccion: representa una operación
    realizada sobre una cuenta (depósito, retiro,
    transferencia, etc.).
    """

    __tablename__ = "transacciones"

    idTransaccion = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tipo = Column(String(50), nullable=False)
    monto = Column(Float, nullable=False)
    fecha = Column(DateTime, default=datetime.now)

    idCuenta = Column(UUID(as_uuid=True), ForeignKey("cuentas.idCuenta"))

    id_usuario_creacion = Column(
        UUID(as_uuid=True), ForeignKey("users.idUser"), nullable=False
    )
    id_usuario_edicion = Column(
        UUID(as_uuid=True), ForeignKey("users.idUser"), nullable=True
    )
    fecha_creacion = Column(DateTime, default=datetime.now, nullable=False)
    fecha_actualizacion = Column(DateTime, default=None, onupdate=datetime.now)

    cuenta = relationship("Cuenta")
    usuario_creacion = relationship("User", foreign_keys=[id_usuario_creacion])
    usuario_edicion = relationship("User", foreign_keys=[id_usuario_edicion])

    def __repr__(self):
        return f"<Transacción {self.tipo} - Monto: {self.monto}>"
