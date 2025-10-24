# Patient Service - Guía de Debugging y Troubleshooting

Guía completa para debuggear, configurar y troubleshoot el microservicio Patient Service.

---

## 📋 Tabla de Contenidos

1. [Configuración del Entorno](#configuración-del-entorno)
2. [Configuración de Base de Datos](#configuración-de-base-de-datos)
3. [Ejecución del Servicio](#ejecución-del-servicio)
4. [Debugging con VSCode](#debugging-con-vscode)
5. [Troubleshooting Común](#troubleshooting-común)
6. [Testing](#testing)

---

## Configuración del Entorno

### Requisitos Previos
- Python 3.11+
- PostgreSQL 15+
- Git

### Setup Inicial

```bash
# 1. Crear y activar entorno virtual
cd h:\GALYDEV\CLINIC-SYSTEM\patient-service
python -m venv venv
venv\Scripts\activate  # Windows

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales
```

### Variables de Entorno (.env)

```env
DATABASE_URL=postgresql+asyncpg://postgres:tu_password@localhost:5432/patient_service
DATABASE_ECHO=False
SERVICE_PORT=8002
ENVIRONMENT=development
```

---

## Configuración de Base de Datos

### 1. Crear Base de Datos

```bash
# Conectar a PostgreSQL
psql -U postgres

# Crear DB
CREATE DATABASE patient_service;
\q
```

### 2. Inicializar (OPCIÓN RECOMENDADA: ORM)

```bash
# Ejecuta TODO: drop tables, create tables, seed data
python scripts/init_db.py
```

Este script carga automáticamente:
- 9 tablas (patients, insurance_policies, insurance_providers, etc.)
- Catálogos (3 genders, 8 blood_types, 5 marital_statuses, etc.)
- 12 proveedores de seguros

### 3. Verificar

```bash
python scripts/verify_database.py
```

Deberías ver:
- 9 tablas creadas
- 12 insurance providers
- Constraints UNIQUE en patient_id (insurance_policies)

---

## Ejecución del Servicio

### Desarrollo Local

```bash
# Forma básica
python src/main.py

# Con hot-reload (recomendado)
uvicorn src.main:app --reload --host 0.0.0.0 --port 8002
```

### Verificar

- Swagger UI: http://localhost:8002/docs
- OpenAPI JSON: http://localhost:8002/openapi.json

---

## Debugging con VSCode

### Configuración (ya incluida en .vscode/launch.json)

```json
{
  "name": "Python: FastAPI (Patient Service)",
  "type": "python",
  "request": "launch",
  "module": "uvicorn",
  "args": ["src.main:app", "--reload", "--port", "8002"]
}
```

### Pasos para Debuggear

1. **Colocar breakpoints**: Clic en margen izquierdo del editor
2. **Iniciar debug**: Presionar `F5`
3. **Probar endpoint**: Ir a http://localhost:8002/docs y ejecutar request
4. **Inspeccionar**: Ver variables, call stack, etc.

### Lugares Comunes para Breakpoints

```python
# Use Cases
src/application/use_cases/add_insurance_policy.py:90  # Validación de duplicados
src/application/use_cases/register_patient.py:45      # Validación de paciente

# Routes
src/infrastructure/api/routes/insurance_policy_routes.py:58  # Endpoint handler

# Entities
src/domain/entities/patient.py:60  # Validaciones de dominio
```

---

## Troubleshooting Común

### 1. "psql: command not found"

**Solución Windows:**
```powershell
setx PATH "%PATH%;C:\Program Files\PostgreSQL\15\bin"
```

### 2. "database 'patient_service' does not exist"

```bash
psql -U postgres -c "CREATE DATABASE patient_service;"
```

### 3. "password authentication failed"

**Opción A:** Verificar `.env` tiene la contraseña correcta

**Opción B:** Configurar .pgpass
```bash
# Windows: %APPDATA%\postgresql\pgpass.conf
# Contenido:
localhost:5432:patient_service:postgres:tu_password
```

### 4. "ModuleNotFoundError: No module named 'fastapi'"

```bash
# Asegúrate de estar en el venv
pip install -r requirements.txt
```

### 5. "Port 8002 is already in use"

**Windows:**
```powershell
netstat -ano | findstr :8002
taskkill /PID <PID> /F
```

### 6. "UNIQUE constraint failed: insurance_policies.patient_id"

**Esto es ESPERADO**. El sistema permite **SOLO UNA póliza por paciente**.

Si intentas crear una segunda póliza, obtendrás HTTP 409 Conflict.

### 7. "ForeignKeyViolationError: provider_id"

El provider_id debe existir en `insurance_providers`.

**Ver proveedores disponibles:**
```bash
psql -U postgres -d patient_service -c "SELECT id, code, name FROM insurance_providers;"
```

### 8. DATABASE_ECHO=True para ver SQL queries

En `.env`:
```env
DATABASE_ECHO=True
```

Verás en consola:
```sql
INFO sqlalchemy.engine.Engine SELECT * FROM patients WHERE id = $1
```

---

## Testing

### Ejecutar Tests

```bash
# Todos
pytest

# Solo unidad
pytest tests/unit/

# Con coverage
pytest --cov=src tests/

# Verbose
pytest -v

# Con prints
pytest -s
```

### Debug de Tests en VSCode

1. Abrir archivo de test
2. Colocar breakpoint
3. Clic derecho en función de test → "Debug Test"

---

## Checklist de Debugging

Cuando algo falla, verifica:

- [ ] Venv activado
- [ ] Dependencias instaladas (`pip list`)
- [ ] PostgreSQL corriendo (`pg_isready`)
- [ ] DB existe (`psql -l`)
- [ ] Tablas creadas (`python scripts/verify_database.py`)
- [ ] `.env` configurado
- [ ] Puerto 8002 libre
- [ ] Logs sin errores
- [ ] Acceso a http://localhost:8002/docs

---

**Para más información:**
- Ver [ARCHITECTURE.md](ARCHITECTURE.md) para estructura del código
- Ver [README.md](README.md) para información general
