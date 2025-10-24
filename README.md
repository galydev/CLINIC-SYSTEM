# Clinic Management System

Sistema de gestión clínica basado en microservicios para administrar pacientes, historias clínicas, órdenes médicas, inventario y facturación.

## Arquitectura

Este proyecto está construido utilizando una arquitectura de microservicios, donde cada servicio maneja un dominio específico del negocio:

### Microservicios

- **identity-service**: Gestión de autenticación y autorización de usuarios
- **patient-service**: Gestión de información de pacientes
- **medical-records-service**: Gestión de historias clínicas y registros médicos
- **orders-service**: Gestión de órdenes médicas (laboratorio, imagenología, procedimientos)
- **inventory-service**: Gestión de inventario de medicamentos y suministros médicos
- **billing-service**: Gestión de facturación y pagos

## Estructura del Proyecto

```
Clinic-Management-System/
├── identity-service/           # Servicio de identidad y autenticación
├── patient-service/            # Servicio de gestión de pacientes
├── medical-records-service/    # Servicio de historias clínicas
├── orders-service/             # Servicio de órdenes médicas
├── inventory-service/          # Servicio de inventario
├── billing-service/            # Servicio de facturación
├── infrastructure/             # Configuraciones de Docker y orquestación
├── docs/                       # Documentación del proyecto
├── docker-compose.yml          # Orquestación de servicios
└── README.md                   # Este archivo
```

## Tecnologías

- **Backend**: Python (FastAPI/Flask)
- **Base de datos**: PostgreSQL
- **Message Broker**: RabbitMQ/Kafka
- **Containerización**: Docker
- **Orquestación**: Docker Compose

## Requisitos Previos

- Docker 20.10+
- Docker Compose 2.0+
- Python 3.11+

## Inicio Rápido

1. Clonar el repositorio:

```bash
git clone <repository-url>
cd Clinic-Management-System
```

2. Construir y ejecutar los servicios:

```bash
docker-compose up --build
```

3. Los servicios estarán disponibles en:

- Identity Service: http://localhost:8001
- Patient Service: http://localhost:8002
- Medical Records Service: http://localhost:8003
- Orders Service: http://localhost:8004
- Inventory Service: http://localhost:8005
- Billing Service: http://localhost:8006

## Desarrollo

Cada microservicio tiene su propio README con instrucciones específicas de desarrollo.

## Documentación

La documentación detallada del proyecto se encuentra en la carpeta `docs/`.

## Licencia

Este proyecto es privado y de uso interno.
