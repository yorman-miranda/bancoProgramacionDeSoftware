# 🏦 Sistema Bancario - Documentación Completa

## 📋 Descripción del Proyecto
Sistema bancario completo desarrollado en **Python** con arquitectura modular, base de datos **PostgreSQL** y API REST con **FastAPI**.  
El sistema gestiona usuarios, clientes, empleados, sucursales, cuentas bancarias y transacciones financieras.

---

## 🏗️ Arquitectura del Sistema

```
sistema_bancario/
├── entities/ <br>
│   ├── user.py <br>
│   ├── cliente.py <br>
│   ├── empleado.py <br>
│   ├── sucursal.py <br>
│   ├── cuenta.py <br>
│   └── transaccion.py <br>
├── crud/ <br> 
│   ├── user_crud.py <br>
│   ├── cliente_crud.py <br>
│   ├── empleado_crud.py <br>
│   ├── sucursal_crud.py <br>
│   ├── cuenta_crud.py <br>
│   └── transaccion_crud.py <br>
├── database/ <br>
│   ├── config.py <br>
│   └── base.py <br>
├── auth/ <br>
│   └── security.py <br>
├── apis/               # Endpoints FastAPI (REST API)
│   ├── auth.py
│   ├── clientes.py
│   ├── cuentas.py
│   ├── empleados.py
│   ├── operaciones.py
│   ├── sucursales.py
│   ├── transacciones.py
│   └── usuarios.py
├── migrations/         
├── main.py             
├── schemas.py          # Esquemas Pydantic para validación
├── requirements.txt    # Dependencias del proyecto
├── .env                # Variables de entorno
└── .gitignore          # Archivos ignorados por Git
```

---

## 🎯 Roles del Sistema

### 👑 Administrador
- Crear empleados y sucursales  
- Gestionar usuarios del sistema  
- Ver reportes generales  
- Acceso completo al sistema  

### 👷 Empleado
- Gestión de clientes  
- Apertura de cuentas bancarias  
- Operaciones bancarias para clientes  
- Consultas de sucursal  

### 👤 Cliente
- Gestión de cuentas propias  
- Operaciones bancarias personales  
- Consulta de movimientos  
- Información personal  

---

## 🚀 Instalación y Configuración

### ⚙️ Prerrequisitos
- Python 3.8+  


### Ejecutar la aplicación
```bash
[control]+[shift]+ñ # ingresar a la terminal en VS code
python .\main.py # escribir este codigo en la terminal y ahi mismo el main suelta el enlace para visualizar la pagina
```

## 📊 Estructura de la Base de Datos

### Tablas Principales

**users** - Usuarios del sistema  
- idUser (UUID, PK)  
- firstName, lastName (String)  
- username (String, Unique)  
- password (String, Hash)  
- activo (Boolean)  
- es_admin (Boolean)

**clientes** - Clientes del banco  
- idCliente (UUID, PK)  
- nombre, documento (String, Unique)  
- telefono, email, direccion  
- idUsuario (FK → users)  
- idSucursal (FK → sucursales)

**empleados** - Empleados del banco  
- idEmpleado (UUID, PK)  
- nombre, apellido, cargo  
- idSucursal (FK → sucursales)  
- idUsuario (FK → users)

**sucursales** - Sucursales bancarias  
- idSucursal (UUID, PK)  
- nombreSucursal, ciudad  
- direccion, telefono

**cuentas** - Cuentas bancarias  
- idCuenta (UUID, PK)  
- numeroCuenta (String, Unique)  
- saldo (Float)  
- tipoCuenta (AHORRO / CORRIENTE / CREDITO)  
- estado (ACTIVA / BLOQUEADA / SUSPENDIDA)  
- idCliente (FK → clientes)

**transacciones** - Transacciones bancarias  
- idTransaccion (UUID, PK)  
- tipo (String)  
- monto (Float)  
- fecha (DateTime)  
- idCuenta (FK → cuentas)

---

## 🔄 Endpoints FastAPI Disponibles

### Autenticación (`/auth`)
- `POST /auth/login` → Iniciar sesión  
- `POST /auth/register` → Registrar usuario  
- `POST /auth/refresh` → Refrescar token  

### Usuarios (`/usuarios`)
- `GET /usuarios/` → Listar usuarios (Admin)  
- `GET /usuarios/{id}` → Obtener usuario por ID  
- `PUT /usuarios/{id}` → Actualizar usuario  
- `DELETE /usuarios/{id}` → Desactivar usuario  

### Clientes (`/clientes`)
- `GET /clientes/` → Listar clientes  
- `POST /clientes/` → Crear cliente  
- `GET /clientes/{id}` → Obtener cliente por ID  
- `PUT /clientes/{id}` → Actualizar cliente  

### Empleados (`/empleados`)
- `GET /empleados/` → Listar empleados  
- `POST /empleados/` → Crear empleado  
- `GET /empleados/{id}` → Obtener empleado por ID  
- `PUT /empleados/{id}` → Actualizar empleado  

### Sucursales (`/sucursales`)
- `GET /sucursales/` → Listar sucursales  
- `POST /sucursales/` → Crear sucursal  
- `GET /sucursales/{id}` → Obtener sucursal por ID  
- `PUT /sucursales/{id}` → Actualizar sucursal  

### Cuentas (`/cuentas`)
- `GET /cuentas/` → Listar cuentas  
- `POST /cuentas/` → Crear cuenta  
- `GET /cuentas/{id}` → Obtener cuenta por ID  
- `PUT /cuentas/{id}/estado` → Cambiar estado de cuenta  

### Transacciones (`/transacciones`)
- `POST /transacciones/deposito` → Realizar depósito  
- `POST /transacciones/retiro` → Realizar retiro  
- `POST /transacciones/transferencia` → Realizar transferencia  
- `GET /transacciones/cuenta/{id}` → Historial de transacciones  

### Operaciones (`/operaciones`)
- `GET /operaciones/reportes` → Generar reportes  
- `GET /operaciones/estadisticas` → Estadísticas del sistema

---

## 🛠️ Tecnologías Utilizadas

- **Python 3.8+**
- **FastAPI**
- **SQLAlchemy**
- **PostgreSQL**
- **JWT**
- **Pydantic**
- **Uvicorn**
- **python-dotenv**
- **bcrypt**
- **python-multipart**

---

