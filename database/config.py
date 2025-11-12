# """
# Configuración de la base de datos PostgreSQL con Neon
# """

# import os
# from dotenv import load_dotenv
# from sqlalchemy import create_engine, text
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, scoped_session


# load_dotenv()


# DATABASE_URL = os.getenv("DATABASE_URL")

# if not DATABASE_URL:
#     raise ValueError("Se requiere DATABASE_URL en las variables de entorno")


# engine = create_engine(
#     DATABASE_URL,
#     echo=True,
#     pool_pre_ping=True,
#     pool_recycle=300,
#     connect_args={"sslmode": "require"},
# )


# Base = declarative_base()


# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# SessionScoped = scoped_session(SessionLocal)


# def get_session():
#     """
#     Obtiene una nueva sesión de base de datos
#     """
#     return SessionLocal()


# def get_session_context():
#     """
#     Context manager para sesiones de base de datos
#     """
#     session = SessionLocal()
#     try:
#         yield session
#     finally:
#         session.close()


# def check_connection():
#     try:
#         with engine.connect() as conn:

#             result = conn.execute(text("SELECT 1"))

#             data = result.fetchone()
#             print(f"Conexión exitosa: {data[0]}")
#         return True
#     except Exception as e:
#         print(f"Error de conexión: {e}")
#         return False


# def create_tables():
#     """
#     Crear todas las tablas definidas en los modelos
#     """
#     try:

#         from entities.user import User
#         from entities.cliente import Cliente
#         from entities.cuenta import Cuenta
#         from entities.empleado import Empleado
#         from entities.sucursal import Sucursal
#         from entities.transaccion import Transaccion

#         print(
#             "Eliminando tablas existentes (¡Paso temporal para corregir el esquema!)..."
#         )
#         Base.metadata.drop_all(engine)

#         print("Creando tablas...")
#         Base.metadata.create_all(engine)
#         print("Tablas creadas exitosamente")
#     except Exception as e:
#         print(f"Error al crear tablas: {e}")
#         raise e


"""
Configuración de la base de datos PostgreSQL con Neon
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from typing import Generator

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("Se requiere DATABASE_URL en las variables de entorno")

engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={"sslmode": "require"},
)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

SessionScoped = scoped_session(SessionLocal)


def get_session():
    """
    Obtiene una nueva sesión de base de datos
    """
    return SessionLocal()


def get_session_context():
    """
    Context manager para sesiones de base de datos
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


# ✅ AGREGAR ESTE MÉTODO PARA FASTAPI
def get_db() -> Generator:
    """
    Dependencia de FastAPI para inyectar sesiones de base de datos
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_connection():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            data = result.fetchone()
            print(f"Conexión exitosa: {data[0]}")
        return True
    except Exception as e:
        print(f"Error de conexión: {e}")
        return False


def create_tables():
    """
    Crear todas las tablas definidas en los modelos
    """
    try:
        from entities.user import User
        from entities.cliente import Cliente
        from entities.cuenta import Cuenta
        from entities.empleado import Empleado
        from entities.sucursal import Sucursal
        from entities.transaccion import Transaccion

        print(
            "Eliminando tablas existentes (¡Paso temporal para corregir el esquema!)..."
        )
        Base.metadata.drop_all(engine)

        print("Creando tablas...")
        Base.metadata.create_all(engine)
        print("Tablas creadas exitosamente")
    except Exception as e:
        print(f"Error al crear tablas: {e}")
        raise e
