from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from sqlalchemy.orm import relationship
from database.config import Base


class Cuenta(Base):
    """
    Entidad Cuenta: representa una cuenta bancaria
    que pertenece a un cliente. Puede ser de tipo
    ahorro, corriente o crédito.
    """

    __tablename__ = "cuentas"

    idCuenta = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    numeroCuenta = Column(String(20), unique=True, nullable=False)
    saldo = Column(Float, default=0.0)
    fechaApertura = Column(DateTime, default=datetime.now)
    estado = Column(String(20), nullable=False)
    tipoCuenta = Column(String(20), nullable=False)

    idCliente = Column(UUID(as_uuid=True), ForeignKey("clientes.idCliente"))

    id_usuario_creacion = Column(
        UUID(as_uuid=True), ForeignKey("users.idUser"), nullable=False
    )
    id_usuario_edicion = Column(
        UUID(as_uuid=True), ForeignKey("users.idUser"), nullable=True
    )
    fecha_creacion = Column(DateTime, default=datetime.now, nullable=False)
    fecha_actualizacion = Column(DateTime, default=None, onupdate=datetime.now)

    cliente = relationship("Cliente")
    usuario_creacion = relationship("User", foreign_keys=[id_usuario_creacion])
    usuario_edicion = relationship("User", foreign_keys=[id_usuario_edicion])

    def __repr__(self):
        return f"<Cuenta {self.numeroCuenta} ({self.tipoCuenta}) - Saldo: {self.saldo}>"
