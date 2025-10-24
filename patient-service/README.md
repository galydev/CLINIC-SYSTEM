# Patient Service

Microservicio para gestión de pacientes del sistema de gestión clínica.
Implementado con **Clean Architecture**, **DDD** y **FastAPI**.

---

## 🚀 Inicio Rápido

### Setup

```bash
# 1. Entorno virtual
python -m venv venv
venv\Scripts\activate

# 2. Dependencias
pip install -r requirements.txt

# 3. Configurar .env
cp .env.example .env
# Editar DATABASE_URL

# 4. Base de datos
psql -U postgres -c "CREATE DATABASE patient_service;"
python scripts/init_db.py

# 5. Ejecutar
uvicorn src.main:app --reload --port 8002
```

### Verificar
- Swagger: http://localhost:8002/docs

---

## 📚 Funcionalidades

- ✅ Gestión de pacientes
- ✅ Contactos de emergencia
- ✅ Pólizas de seguro (**una por paciente**)
- ✅ Proveedores de seguros (normalizados)

---

## 📖 Documentación

| Documento | Contenido |
|-----------|-----------|
| [ARCHITECTURE.md](ARCHITECTURE.md) | Arquitectura, capas, modelo de datos, casos de uso |
| [DEBUG_GUIDE.md](DEBUG_GUIDE.md) | Configuración, debugging, troubleshooting |

---

## 🏗️ Arquitectura

```
src/
├── domain/           # Entidades, repositorios (interfaces)
├── application/      # Use cases, DTOs
├── infrastructure/   # ORM models, API routes
└── config/           # Settings
```

**Ver [ARCHITECTURE.md](ARCHITECTURE.md) para detalles.**

---

## 🔌 API Endpoints

### Patients
- POST `/api/v1/patients` - Registrar
- GET `/api/v1/patients/{id}` - Obtener
- PUT `/api/v1/patients/{id}` - Actualizar

### Insurance
- POST `/api/v1/patients/{id}/insurance-policies` - Agregar póliza
- GET `/api/v1/patients/{id}/insurance-policies/status` - Estado

**⚠️ IMPORTANTE**: Solo se permite **UNA póliza por paciente**.

---

## 💾 Base de Datos

### Inicializar

```bash
python scripts/init_db.py
```

Carga:
- 9 tablas
- 12 proveedores de seguros
- Catálogos (genders, blood_types, etc.)

### Verificar

```bash
python scripts/verify_database.py
```

---

## 📜 Scripts de Base de Datos

La carpeta [scripts/](scripts/) contiene utilidades para gestionar la base de datos:

### 1. `init_db.py` - Inicialización Completa

Inicializa la base de datos desde cero (crea tablas + carga datos iniciales):

```bash
python scripts/init_db.py
```

**Ejecuta automáticamente**:
- Creación de todas las tablas
- Carga de catálogos (géneros, tipos de sangre, etc.)
- Carga de 12 proveedores de seguros

### 2. `reset_database.py` - Reiniciar Base de Datos

Elimina y recrea todas las tablas (⚠️ **BORRA TODOS LOS DATOS**):

```bash
python scripts/reset_database.py
```

**Después de ejecutar, debes cargar los datos iniciales**:
```bash
python scripts/seed_catalogs.py
python scripts/seed_providers.py
```

### 3. `seed_catalogs.py` - Carga de Catálogos

Carga datos de catálogos del sistema:

```bash
python scripts/seed_catalogs.py
```

**Catálogos incluidos**:
- Géneros (3 registros: MALE, FEMALE, OTHER)
- Tipos de sangre (8 registros: A+, A-, B+, B-, AB+, AB-, O+, O-)
- Estados civiles (5 registros: SINGLE, MARRIED, DIVORCED, WIDOWED, SEPARATED)
- Tipos de relación (6 registros: SPOUSE, PARENT, CHILD, SIBLING, FRIEND, OTHER)
- Estados de seguros (4 registros: ACTIVE, INACTIVE, SUSPENDED, EXPIRED)

### 4. `seed_providers.py` - Carga de Proveedores de Seguros

Carga los 12 proveedores de seguros predefinidos:

```bash
python scripts/seed_providers.py
```

**Proveedores incluidos**: Triple-S, MMM, MAPFRE, First Medical, Plan de Salud Menonita, entre otros.

### 5. `verify_database.py` - Verificación del Estado

Verifica la estructura y datos de la base de datos:

```bash
python scripts/verify_database.py
```

**Muestra**:
- Tablas existentes (9 tablas esperadas)
- Conteo de registros en catálogos
- Conteo de proveedores de seguros
- Estado general del sistema

### Flujo de Trabajo Recomendado

**Setup inicial**:
```bash
# Opción 1: Todo en uno
python scripts/init_db.py

# Opción 2: Paso a paso
python scripts/reset_database.py
python scripts/seed_catalogs.py
python scripts/seed_providers.py
```

**Desarrollo**:
```bash
# Verificar estado
python scripts/verify_database.py

# Recargar catálogos si es necesario
python scripts/seed_catalogs.py

# Recargar proveedores si es necesario
python scripts/seed_providers.py
```

**Reset completo** (⚠️ desarrollo únicamente):
```bash
python scripts/reset_database.py
python scripts/init_db.py
```

---

## 🧪 Testing

### Ejecutar Pruebas Unitarias

```bash
# Ejecutar todas las pruebas unitarias
pytest tests/unit/ -v

# Con reporte de cobertura en terminal
pytest tests/unit/ --cov=src --cov-report=term-missing

# Generar reporte HTML de cobertura
pytest tests/unit/ --cov=src --cov-report=html --cov-report=term-missing

# Ver reporte HTML (Windows)
start htmlcov/index.html
```

### Pruebas por Componente

```bash
# Use Cases
pytest tests/unit/test_register_patient_use_case.py -v
pytest tests/unit/test_add_insurance_policy_use_case.py -v
pytest tests/unit/test_add_emergency_contact_use_case.py -v
pytest tests/unit/test_get_insurance_status_use_case.py -v

# Entidades
pytest tests/unit/test_patient_entity.py -v
pytest tests/unit/test_emergency_contact_entity.py -v
pytest tests/unit/test_insurance_provider_entity.py -v
```

### Cobertura Actual

- **121 pruebas unitarias** con mocks ✅ (+25 nuevas)
- **94% de cobertura** en Domain + Use Cases 🎯 (**¡Meta alcanzada!**)
- **56% de cobertura total** del código
- Reportes generados en `htmlcov/` y `coverage.json`

#### Cobertura por Capa

| Capa | Cobertura | Pruebas |
|------|-----------|---------|
| **Domain + Use Cases** | **94%** 🎯 | 121 |
| Use Cases | 95-100% | 38 |
| Entidades | 92-100% | 83 |
| Total del proyecto | 56% | 121 |

#### Pruebas Implementadas

**Use Cases (38 pruebas):**
- RegisterPatientUseCase (8) - 100%
- AddInsurancePolicyUseCase (7) - 100%
- GetInsuranceStatusUseCase (7) - 100%
- GetPatientUseCase (6) - 100%
- UpdatePatientUseCase (4) - 94%
- AddEmergencyContactUseCase (6) - 95%

**Entidades (83 pruebas):**
- Patient (16) - 92%
- EmergencyContact (18) - 100%
- InsuranceProvider (31) - 99%
- InsurancePolicy (18) - 100%

---

## 🐛 Debugging

**VSCode**: F5 → Seleccionar "Python: FastAPI"

**Ver queries SQL**:
```env
DATABASE_ECHO=True
```

**Ver [DEBUG_GUIDE.md](DEBUG_GUIDE.md) para más detalles.**

---

## 🔧 Stack Tecnológico

- Python 3.11+
- FastAPI 0.104+
- SQLAlchemy 2.0 (async)
- PostgreSQL 15+
- Pydantic 2.5+
- Pytest 7.4+

---

## ✨ Mejoras Recientes

### Proveedores Normalizados
Ahora `insurance_policies.provider_id` apunta a tabla `insurance_providers` (antes era string).

### Una Póliza por Paciente
Constraint UNIQUE en `patient_id` + validación en use case.

---

**Más información**: [ARCHITECTURE.md](ARCHITECTURE.md) | [DEBUG_GUIDE.md](DEBUG_GUIDE.md)

**Versión**: 1.1.0
