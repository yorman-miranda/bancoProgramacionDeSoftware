from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from database.config import Base


class User(Base):
    """
    Entidad User: representa un usuario del sistema.
    Incluye datos personales, credenciales de acceso
    y campos de auditoría.
    """

    __tablename__ = "users"

    idUser = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    firstName = Column(String(100), nullable=False)
    lastName = Column(String(100), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    activo = Column(Boolean, default=True)  # <-- New
    es_admin = Column(Boolean, default=False)  # <-- New

    id_usuario_creacion = Column(
        UUID(as_uuid=True), ForeignKey("users.idUser"), nullable=True
    )
    id_usuario_edicion = Column(
        UUID(as_uuid=True), ForeignKey("users.idUser"), nullable=True
    )
    fecha_creacion = Column(DateTime, default=datetime.now, nullable=False)
    fecha_actualizacion = Column(DateTime, default=None, onupdate=datetime.now)

    def __repr__(self):
        return f"<User {self.firstName} {self.lastName} ({self.username})>"
