# Patient Service - Clean Architecture

Microservicio para la gestión de pacientes del sistema de gestión clínica. Implementado siguiendo los principios de **Clean Architecture** y **Domain-Driven Design**.

---

## 📋 Tabla de Contenidos

1. [Estructura del Proyecto](#estructura-del-proyecto)
2. [Capas de la Arquitectura](#capas-de-la-arquitectura)
3. [Modelo de Datos](#modelo-de-datos)
4. [Casos de Uso](#casos-de-uso)
5. [API Endpoints](#api-endpoints)
6. [Validaciones](#validaciones)
7. [Base de Datos](#base-de-datos)
8. [Tecnologías](#tecnologías)
9. [Principios Aplicados](#principios-aplicados)
10. [Testing](#testing)

---

## Estructura del Proyecto

```
patient-service/
├── src/
│   ├── domain/                          # DOMAIN LAYER (Capa de Dominio)
│   │   ├── entities/                    # Entidades del dominio
│   │   │   ├── patient.py              # ✓ Patient entity con validaciones
│   │   │   ├── emergency_contact.py    # ✓ EmergencyContact entity
│   │   │   ├── insurance_policy.py     # ✓ InsurancePolicy entity
│   │   │   ├── insurance_provider.py   # ✓ InsuranceProvider entity (normalizada)
│   │   │   └── __init__.py
│   │   ├── repositories/                # Interfaces de repositorios
│   │   │   ├── patient_repository.py                # ✓ PatientRepository interface
│   │   │   ├── emergency_contact_repository.py      # ✓ EmergencyContactRepository interface
│   │   │   ├── insurance_policy_repository.py       # ✓ InsurancePolicyRepository interface
│   │   │   ├── insurance_provider_repository.py     # ✓ InsuranceProviderRepository interface
│   │   │   ├── catalog_repository.py                # ✓ CatalogRepository interfaces
│   │   │   └── __init__.py
│   │   └── __init__.py
│   │
│   ├── application/                     # APPLICATION LAYER (Capa de Aplicación)
│   │   ├── dto/                         # Data Transfer Objects
│   │   │   ├── patient_request.py              # ✓ RegisterPatientRequest, UpdatePatientRequest
│   │   │   ├── patient_response.py             # ✓ PatientResponse
│   │   │   ├── emergency_contact_request.py    # ✓ AddEmergencyContactRequest
│   │   │   ├── emergency_contact_response.py   # ✓ EmergencyContactResponse
│   │   │   ├── insurance_policy_request.py     # ✓ AddInsurancePolicyRequest
│   │   │   ├── insurance_policy_response.py    # ✓ InsurancePolicyResponse, InsuranceStatusResponse
│   │   │   ├── error_response.py               # ✓ ErrorResponse
│   │   │   └── __init__.py
│   │   ├── use_cases/                   # Casos de uso
│   │   │   ├── register_patient.py            # ✓ RegisterPatientUseCase
│   │   │   ├── update_patient.py              # ✓ UpdatePatientUseCase
│   │   │   ├── get_patient.py                 # ✓ GetPatientUseCase
│   │   │   ├── add_emergency_contact.py       # ✓ AddEmergencyContactUseCase
│   │   │   ├── add_insurance_policy.py        # ✓ AddInsurancePolicyUseCase
│   │   │   ├── get_insurance_status.py        # ✓ GetInsuranceStatusUseCase
│   │   │   └── __init__.py
│   │   └── __init__.py
│   │
│   ├── infrastructure/                  # INFRASTRUCTURE LAYER (Capa de Infraestructura)
│   │   ├── database/
│   │   │   ├── models/                  # SQLAlchemy ORM models
│   │   │   │   ├── base.py                         # ✓ Base model
│   │   │   │   ├── patient_model.py                # ✓ PatientModel
│   │   │   │   ├── emergency_contact_model.py      # ✓ EmergencyContactModel
│   │   │   │   ├── insurance_policy_model.py       # ✓ InsurancePolicyModel
│   │   │   │   ├── insurance_provider_model.py     # ✓ InsuranceProviderModel
│   │   │   │   ├── catalog_models.py               # ✓ Catalog models (Gender, BloodType, etc.)
│   │   │   │   └── __init__.py
│   │   │   ├── repositories/            # Repository implementations
│   │   │   │   ├── patient_repository_impl.py                # ✓ PatientRepositoryImpl
│   │   │   │   ├── emergency_contact_repository_impl.py      # ✓ EmergencyContactRepositoryImpl
│   │   │   │   ├── insurance_policy_repository_impl.py       # ✓ InsurancePolicyRepositoryImpl
│   │   │   │   ├── insurance_provider_repository_impl.py     # ✓ InsuranceProviderRepositoryImpl
│   │   │   │   ├── catalog_repository_impl.py                # ✓ CatalogRepositoryImpl
│   │   │   │   └── __init__.py
│   │   │   ├── init_database.py         # ✓ ORM database initialization
│   │   │   ├── seed_data.py             # ✓ Seed catalog data
│   │   │   ├── seed_insurance_providers.py  # ✓ Seed insurance providers
│   │   │   └── __init__.py
│   │   ├── api/
│   │   │   ├── routes/                  # FastAPI routes
│   │   │   │   ├── patient_routes.py              # ✓ Patient endpoints
│   │   │   │   ├── emergency_contact_routes.py    # ✓ EmergencyContact endpoints
│   │   │   │   ├── insurance_policy_routes.py     # ✓ InsurancePolicy endpoints
│   │   │   │   └── __init__.py
│   │   │   ├── dependencies.py          # ✓ Dependency injection
│   │   │   └── __init__.py
│   │   └── __init__.py
│   │
│   ├── config/                          # Configuration
│   │   ├── settings.py                 # ✓ Application settings (Pydantic)
│   │   ├── database.py                 # ✓ Database configuration (SQLAlchemy async)
│   │   └── __init__.py
│   │
│   ├── main.py                         # ✓ Application entry point (FastAPI app)
│   └── __init__.py
│
├── scripts/                             # Database scripts
│   ├── init_db.py                      # ✓ Master initialization script (ORM)
│   ├── reset_database.py               # ✓ Drop and create tables
│   ├── seed_catalogs.py                # ✓ Seed catalog data
│   ├── seed_providers.py               # ✓ Seed insurance providers
│   └── verify_database.py              # ✓ Verify database setup
│
├── tests/                              # Tests
│   ├── unit/
│   │   ├── test_patient_entity.py     # ✓ Patient entity tests
│   │   └── __init__.py
│   ├── integration/
│   │   └── __init__.py
│   ├── conftest.py                    # ✓ Pytest configuration
│   └── __init__.py
│
├── requirements.txt                    # ✓ Python dependencies
├── Dockerfile                          # ✓ Docker configuration
├── .env.example                        # ✓ Environment variables example
├── .gitignore                          # ✓ Git ignore rules
├── .dockerignore                       # ✓ Docker ignore rules
├── pytest.ini                          # ✓ Pytest configuration
├── README.md                           # ✓ Project documentation
├── ARCHITECTURE.md                     # ✓ This file
└── DEBUG_GUIDE.md                      # ✓ Debugging guide
```

---

## Capas de la Arquitectura

### 1. Domain Layer (Capa de Dominio)

**Responsabilidad**: Lógica de negocio pura, independiente de frameworks y tecnologías externas.

#### Entities (Entidades)

Modelos de dominio ricos en comportamiento con lógica de negocio encapsulada.

##### **Patient (Paciente)**

Entidad principal que representa a un paciente del sistema.

```python
@dataclass
class Patient:
    id: UUID
    national_id_number: str  # 6-10 dígitos, único
    full_name: str           # máximo 100 caracteres
    birth_date: date         # no futuro, máximo 150 años
    gender_id: UUID          # referencia a catálogo
    blood_type_id: UUID      # referencia a catálogo (opcional)
    marital_status_id: UUID  # referencia a catálogo
    phone: str               # 7-15 dígitos
    email: str               # formato válido, único
    address: str             # máximo 200 caracteres
    occupation: str | None   # máximo 100 caracteres
    allergies: list[str]
    chronic_conditions: list[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
```

**Métodos principales**:
- `create()`: Factory method para crear nuevo paciente
- `update_contact_info()`: Actualizar información de contacto
- `update_medical_info()`: Actualizar información médica
- `deactivate()`: Desactivar paciente (soft delete)
- `validate()`: Validar todas las reglas de negocio

##### **InsurancePolicy (Póliza de Seguro)**

Gestión de pólizas de seguro médico.

```python
@dataclass
class InsurancePolicy:
    id: UUID
    patient_id: UUID
    provider_id: UUID        # ⭐ Referencia a insurance_providers
    policy_number: str       # único, máximo 50 caracteres
    coverage_details: str    # máximo 500 caracteres
    valid_from: date
    valid_until: date
    status: str              # ACTIVE, INACTIVE, EXPIRED, SUSPENDED
    created_at: datetime
    updated_at: datetime
```

**Métodos principales**:
- `create()`: Factory method para crear póliza
- `update_status()`: Actualizar estado según fechas
- `is_currently_active()`: Verificar si está activa
- `extend_validity()`: Extender vigencia

**⚠️ IMPORTANTE**: **Solo UNA póliza por paciente está permitida**. Esta restricción se aplica en:
- Constraint UNIQUE en `patient_id` a nivel de base de datos
- Validación en `AddInsurancePolicyUseCase`

##### **InsuranceProvider (Proveedor de Seguros)**

Entidad normalizada para proveedores de seguros.

```python
@dataclass
class InsuranceProvider:
    id: UUID
    name: str           # máximo 100 caracteres
    code: str           # código único alfanumérico (ej: SALUDTOTAL)
    phone: str | None   # máximo 15 caracteres
    email: str | None   # formato válido
    website: str | None
    address: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime
```

**Métodos principales**:
- `create()`: Factory method para crear proveedor
- `update_info()`: Actualizar información
- `activate()`: Activar proveedor
- `deactivate()`: Desactivar proveedor

##### **EmergencyContact (Contacto de Emergencia)**

Contactos de emergencia del paciente.

```python
@dataclass
class EmergencyContact:
    id: UUID
    patient_id: UUID
    full_name: str             # máximo 100 caracteres
    phone: str                 # 7-15 dígitos
    relationship_type_id: UUID # referencia a catálogo
    created_at: datetime
    updated_at: datetime
```

#### Repositories (Interfaces de Repositorios)

Definen los contratos para el acceso a datos, sin especificar la implementación.

```python
class PatientRepository(ABC):
    @abstractmethod
    async def save(self, patient: Patient) -> Patient: pass

    @abstractmethod
    async def get_by_id(self, patient_id: UUID) -> Patient | None: pass

    @abstractmethod
    async def get_by_national_id(self, national_id: str) -> Patient | None: pass

    @abstractmethod
    async def update(self, patient: Patient) -> Patient: pass

    @abstractmethod
    async def exists_by_email(self, email: str) -> bool: pass

    @abstractmethod
    async def exists_by_national_id(self, national_id: str) -> bool: pass
```

Otros repositorios:
- `InsurancePolicyRepository`
- `InsuranceProviderRepository` ⭐ (nuevo)
- `EmergencyContactRepository`
- `CatalogRepository` (genérico para catálogos)

---

### 2. Application Layer (Capa de Aplicación)

**Responsabilidad**: Casos de uso y orquestación de la lógica de negocio.

#### DTOs (Data Transfer Objects)

**Request DTOs**: Validación de entrada con Pydantic

```python
class RegisterPatientRequest(BaseModel):
    national_id_number: str = Field(..., min_length=6, max_length=10)
    full_name: str = Field(..., max_length=100)
    birth_date: date
    gender_id: UUID
    blood_type_id: UUID | None = None
    marital_status_id: UUID
    phone: str = Field(..., min_length=7, max_length=15)
    email: EmailStr
    address: str = Field(..., max_length=200)
    occupation: str | None = Field(None, max_length=100)
    allergies: list[str] = []
    chronic_conditions: list[str] = []
```

```python
class AddInsurancePolicyRequest(BaseModel):
    provider_id: UUID  # ⭐ UUID del proveedor (no nombre)
    policy_number: str = Field(..., max_length=50)
    coverage_details: str = Field(..., max_length=500)
    valid_from: date
    valid_until: date
```

**Response DTOs**: Formato de salida

```python
class InsuranceStatusResponse(BaseModel):
    patient_id: UUID
    has_active_insurance: bool
    active_policy: InsurancePolicyResponse | None  # ⭐ UNA sola póliza
    has_policy: bool
```

#### Use Cases (Casos de Uso)

Cada caso de uso implementa un flujo de negocio específico.

##### **AddInsurancePolicyUseCase**

Flujo de validación completo:

1. ✅ Verificar que el paciente existe
2. ✅ **Verificar que el paciente NO tiene póliza previa** (regla de negocio)
3. ✅ Verificar que el proveedor de seguros existe
4. ✅ Verificar unicidad del número de póliza
5. ✅ Validar status ACTIVE en catálogos
6. ✅ Crear entidad y persistir

**Excepciones lanzadas**:
- `PatientNotFoundError` → HTTP 404
- `InsuranceProviderNotFoundError` → HTTP 404
- `DuplicatePolicyError` → HTTP 409
- `ValidationError` → HTTP 400

##### **GetInsuranceStatusUseCase**

Retorna el estado del seguro del paciente:

```python
async def execute(self, patient_id: UUID) -> InsuranceStatusResponse:
    # 1. Verificar paciente
    # 2. Obtener póliza (solo una permitida)
    # 3. Actualizar estado según fechas
    # 4. Retornar response con active_policy o None
```

---

### 3. Infrastructure Layer (Capa de Infraestructura)

**Responsabilidad**: Implementaciones concretas de interfaces y detalles técnicos.

#### Database Models (SQLAlchemy ORM)

##### **InsurancePolicyModel**

```python
class InsurancePolicyModel(Base):
    __tablename__ = "insurance_policies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(
        UUID(as_uuid=True),
        ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
        unique=True  # ⭐ CONSTRAINT: UNA póliza por paciente
    )
    provider_id = Column(
        UUID(as_uuid=True),
        ForeignKey("insurance_providers.id", ondelete="RESTRICT"),  # ⭐ No permitir eliminar proveedor con pólizas
        nullable=False
    )
    policy_number = Column(String(50), unique=True, nullable=False, index=True)
    # ... otros campos

    # Relationships
    patient = relationship("PatientModel", back_populates="insurance_policies")
    provider = relationship("InsuranceProviderModel", back_populates="insurance_policies")
    status = relationship("InsuranceStatusModel")
```

##### **InsuranceProviderModel** ⭐ (Nueva)

```python
class InsuranceProviderModel(Base):
    __tablename__ = "insurance_providers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, nullable=False, index=True)  # ⭐ Código único
    phone = Column(String(15))
    email = Column(String(100))
    website = Column(String(200))
    address = Column(String(200))
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    insurance_policies = relationship("InsurancePolicyModel", back_populates="provider")
```

#### Repository Implementations

Implementaciones concretas usando SQLAlchemy con async/await.

```python
class InsurancePolicyRepositoryImpl(InsurancePolicyRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, policy: InsurancePolicy, status_id: UUID) -> InsurancePolicy:
        model = InsurancePolicyModel(
            id=policy.id,
            patient_id=policy.patient_id,
            provider_id=policy.provider_id,  # ⭐ UUID del proveedor
            policy_number=policy.policy_number,
            coverage_details=policy.coverage_details,
            valid_from=policy.valid_from,
            valid_until=policy.valid_until,
            status_id=status_id
        )
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model, ["provider", "status"])  # ⭐ Eager load
        return self._to_entity(model)
```

#### API Routes

Endpoints de FastAPI con manejo completo de excepciones.

```python
@router.post(
    "/",
    response_model=InsurancePolicyResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request - Validation error"},
        404: {"model": ErrorResponse, "description": "Not Found - Patient or insurance provider not found"},
        409: {"model": ErrorResponse, "description": "Conflict - Insurance policy already exists or patient already has a policy"}
    }
)
async def add_insurance_policy(
    patient_id: UUID,
    request: AddInsurancePolicyRequest,
    use_case: AddInsurancePolicyUseCase = Depends(get_add_insurance_policy_use_case)
):
    try:
        return await use_case.execute(patient_id, request)
    except PatientNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InsuranceProviderNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DuplicatePolicyError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {str(e)}")
```

---

### 4. Configuration Layer

**Responsabilidad**: Configuración centralizada de la aplicación.

#### Settings (Pydantic BaseSettings)

```python
class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    DATABASE_ECHO: bool = False

    # Application
    APP_NAME: str = "Patient Service"
    APP_VERSION: str = "1.0.0"
    SERVICE_PORT: int = 8002

    # CORS
    CORS_ORIGINS: list[str] = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = True
```

#### Database Configuration

```python
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    future=True
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)
```

---

## Modelo de Datos

### Diagrama de Entidades

```
┌─────────────────┐
│    PATIENTS     │
├─────────────────┤
│ id (PK)         │
│ national_id ★   │
│ email ★         │
│ gender_id (FK)  │
│ blood_type_id   │
│ marital_id (FK) │
└─────────────────┘
        │
        │ 1:N
        ├──────────────────┐
        │                  │
        ▼                  ▼
┌──────────────────┐  ┌───────────────────┐
│ EMERGENCY_       │  │ INSURANCE_        │
│ CONTACTS         │  │ POLICIES          │
├──────────────────┤  ├───────────────────┤
│ id (PK)          │  │ id (PK)           │
│ patient_id (FK)  │  │ patient_id ★ (FK) │ ← UNIQUE
│ relationship(FK) │  │ provider_id (FK)  │
└──────────────────┘  │ policy_number ★   │
                      │ status_id (FK)    │
                      └───────────────────┘
                               │
                               │ N:1
                               ▼
                      ┌────────────────────┐
                      │ INSURANCE_         │
                      │ PROVIDERS          │
                      ├────────────────────┤
                      │ id (PK)            │
                      │ code ★             │ ← UNIQUE
                      │ name               │
                      │ is_active          │
                      └────────────────────┘
```

★ = UNIQUE constraint

### Tablas de Catálogo

- `genders`: 3 registros (MALE, FEMALE, OTHER)
- `blood_types`: 8 registros (A+, A-, B+, B-, AB+, AB-, O+, O-)
- `marital_statuses`: 5 registros (SINGLE, MARRIED, DIVORCED, WIDOWED, SEPARATED)
- `relationship_types`: 6 registros (SPOUSE, PARENT, CHILD, SIBLING, FRIEND, OTHER)
- `insurance_statuses`: 4 registros (ACTIVE, INACTIVE, SUSPENDED, EXPIRED)
- `insurance_providers`: 12 registros precargados

---

## Casos de Uso

### 1. RegisterPatient

**Descripción**: Registrar un nuevo paciente en el sistema.

**Validaciones**:
1. National ID único
2. Email único
3. Edad válida (no futuro, máximo 150 años)
4. Catálogos existen (gender, blood_type, marital_status)

**Excepciones**:
- `DuplicateEmailError` → HTTP 409
- `DuplicateNationalIdError` → HTTP 409
- `ValidationError` → HTTP 400

### 2. UpdatePatient

**Descripción**: Actualizar información del paciente.

**Campos actualizables**:
- full_name
- phone
- email
- address
- marital_status_id
- occupation
- allergies
- chronic_conditions

**Excepciones**:
- `PatientNotFoundError` → HTTP 404
- `DuplicateEmailError` → HTTP 409
- `ValidationError` → HTTP 400

### 3. GetPatient

**Descripción**: Obtener información completa del paciente.

**Métodos**:
- Por ID (UUID)
- Por national_id_number

**Excepciones**:
- `PatientNotFoundError` → HTTP 404

### 4. AddEmergencyContact

**Descripción**: Agregar un contacto de emergencia al paciente.

**Validaciones**:
1. Paciente existe
2. Tipo de relación válido (catálogo)

**Excepciones**:
- `PatientNotFoundError` → HTTP 404
- `ValidationError` → HTTP 400

### 5. AddInsurancePolicy

**Descripción**: Agregar póliza de seguro al paciente.

**Validaciones** (en orden):
1. ✅ Paciente existe
2. ✅ **Paciente NO tiene póliza previa** ⭐
3. ✅ Proveedor de seguros existe
4. ✅ Número de póliza es único
5. ✅ Status ACTIVE existe
6. ✅ Fechas válidas (valid_from < valid_until)

**Excepciones**:
- `PatientNotFoundError` → HTTP 404
- `InsuranceProviderNotFoundError` → HTTP 404 ⭐
- `DuplicatePolicyError` → HTTP 409
- `ValidationError` → HTTP 400

### 6. GetInsuranceStatus

**Descripción**: Obtener estado del seguro del paciente.

**Retorna**:
- `has_active_insurance`: bool
- `active_policy`: InsurancePolicyResponse | None (solo si ACTIVE)
- `has_policy`: bool (tiene póliza, activa o no)

**Excepciones**:
- `PatientNotFoundError` → HTTP 404

---

## API Endpoints

### Patients

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/patients` | Registrar paciente |
| GET | `/api/v1/patients/{patient_id}` | Obtener por ID |
| GET | `/api/v1/patients/national-id/{national_id}` | Obtener por cédula |
| PUT | `/api/v1/patients/{patient_id}` | Actualizar paciente |

### Emergency Contacts

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/patients/{patient_id}/emergency-contacts` | Agregar contacto |
| GET | `/api/v1/patients/{patient_id}/emergency-contacts` | Listar contactos |

### Insurance Policies

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/patients/{patient_id}/insurance-policies` | Agregar póliza ⭐ (una por paciente) |
| GET | `/api/v1/patients/{patient_id}/insurance-policies` | Listar pólizas |
| GET | `/api/v1/patients/{patient_id}/insurance-policies/status` | Estado de seguro |

---

## Validaciones

### Patient (Paciente)

| Campo | Validación |
|-------|------------|
| national_id_number | 6-10 dígitos, solo números, UNIQUE |
| email | Formato válido, UNIQUE |
| phone | 7-15 dígitos, solo números |
| birth_date | No futuro, máximo 150 años |
| full_name | Máximo 100 caracteres |
| address | Máximo 200 caracteres |
| occupation | Máximo 100 caracteres (opcional) |

### EmergencyContact

| Campo | Validación |
|-------|------------|
| full_name | Máximo 100 caracteres |
| phone | 7-15 dígitos, solo números |
| relationship_type_id | Debe existir en catálogo |

### InsurancePolicy

| Campo | Validación |
|-------|------------|
| patient_id | **UNIQUE** (solo una póliza por paciente) ⭐ |
| provider_id | Debe existir en insurance_providers |
| policy_number | UNIQUE, máximo 50 caracteres |
| coverage_details | Máximo 500 caracteres |
| valid_from, valid_until | valid_from < valid_until |

### InsuranceProvider

| Campo | Validación |
|-------|------------|
| code | UNIQUE, alfanumérico, máximo 20 caracteres |
| name | Máximo 100 caracteres |
| phone | Máximo 15 caracteres (opcional) |
| email | Formato válido (opcional) |

---

## Base de Datos

### Configuración

- **Motor**: PostgreSQL 15+
- **ORM**: SQLAlchemy 2.0 (async)
- **Nombre**: `patient_service`
- **Pool**: AsyncEngine con pool de conexiones

### Inicialización

**Inicialización con ORM (Python)**

```bash
# Desde la raíz del patient-service
python scripts/init_db.py
```

Este script:
1. Elimina todas las tablas existentes
2. Crea las 9 tablas desde los modelos ORM
3. Carga datos de catálogos
4. Carga 12 proveedores de seguros

### Scripts Disponibles

| Script | Descripción |
|--------|-------------|
| `scripts/init_db.py` | Inicialización completa (ORM) |
| `scripts/reset_database.py` | Drop y create tables |
| `scripts/seed_catalogs.py` | Cargar catálogos |
| `scripts/seed_providers.py` | Cargar proveedores |
| `scripts/verify_database.py` | Verificar setup |

---

## Tecnologías

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| Python | 3.11+ | Lenguaje de programación |
| FastAPI | 0.104+ | Framework web async |
| SQLAlchemy | 2.0+ | ORM async |
| Pydantic | 2.5+ | Validación de datos |
| PostgreSQL | 15+ | Base de datos relacional |
| Uvicorn | 0.24+ | Servidor ASGI |
| Pytest | 7.4+ | Testing framework |
| asyncpg | 0.29+ | Driver PostgreSQL async |
| Docker | 24+ | Containerización |

---

## Principios Aplicados

### SOLID

1. **Single Responsibility**: Cada clase tiene una única responsabilidad
   - `AddInsurancePolicyUseCase`: Solo agregar póliza
   - `InsuranceProviderRepository`: Solo acceso a proveedores

2. **Open/Closed**: Abierto a extensión, cerrado a modificación
   - Nuevos casos de uso sin modificar existentes
   - Nuevas validaciones sin cambiar entidades

3. **Liskov Substitution**: Las implementaciones respetan los contratos
   - `InsurancePolicyRepositoryImpl` implementa `InsurancePolicyRepository`

4. **Interface Segregation**: Interfaces específicas y cohesivas
   - Repositorios separados por entidad

5. **Dependency Inversion**: Dependencias hacia abstracciones
   - Use cases dependen de interfaces, no implementaciones

### Clean Architecture

- ✅ Independencia de frameworks (domain no conoce FastAPI)
- ✅ Independencia de UI (puede ser REST, GraphQL, CLI)
- ✅ Independencia de base de datos (domain no conoce SQLAlchemy)
- ✅ Testeable (entidades y use cases sin infraestructura)
- ✅ Reglas de negocio en el dominio

### Domain-Driven Design (DDD)

- **Entidades**: Modelos ricos con comportamiento (`Patient`, `InsurancePolicy`)
- **Value Objects**: Enums para conceptos del dominio
- **Repository Pattern**: Abstracción del acceso a datos
- **Ubiquitous Language**: Términos del negocio en el código

---

## Testing

### Estructura de Tests

```
tests/
├── unit/                   # Tests de unidad (entidades, domain logic)
│   ├── test_patient_entity.py
│   └── test_insurance_policy_entity.py
├── integration/            # Tests de integración (API, database)
│   └── test_patient_api.py
└── conftest.py            # Fixtures compartidas
```

### Ejecutar Tests

```bash
# Todos los tests
pytest

# Tests de unidad
pytest tests/unit/

# Tests de integración
pytest tests/integration/

# Con coverage
pytest --cov=src tests/
```

### Fixtures Disponibles

- `db_session`: Sesión de base de datos de prueba
- `test_patient`: Paciente de prueba
- `test_provider`: Proveedor de seguros de prueba

---

## Referencias

- [README.md](README.md) - Información general del proyecto y guía de inicio
- [DEBUG_GUIDE.md](DEBUG_GUIDE.md) - Guía de debugging y troubleshooting

---

## Próximos Pasos

1. ✅ Normalización de proveedores de seguros
2. ✅ Restricción de una póliza por paciente
3. ⏳ Tests de integración completos
4. ⏳ Autenticación/autorización con Identity Service
5. ⏳ Búsqueda avanzada de pacientes (filters, pagination)
6. ⏳ Soft delete completo en todas las entidades
7. ⏳ Logging estructurado (JSON logs)
8. ⏳ Circuit breaker para servicios externos
9. ⏳ Métricas y monitoring (Prometheus)
10. ⏳ Cache layer (Redis)

---

**Última actualización**: 2025-10-23
**Versión**: 1.1.0
