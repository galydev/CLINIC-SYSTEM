# Identity Service

Identity and Authentication microservice for the Clinic Management System, built with Clean Architecture principles.

## Architecture

This service follows Clean Architecture with the following layers:

### Domain Layer (`src/domain/`)
- **Entities**: Core business objects (User)
- **Value Objects**: Immutable objects with validation logic (Password)
- **Repositories**: Interface definitions for data access
- **Services**: Domain business logic (AuthService)

### Application Layer (`src/application/`)
- **Use Cases**: Application-specific business logic
  - `create_user.py`: User registration
  - `login_user.py`: User authentication
  - `validate_token.py`: Token validation
- **DTOs**: Data Transfer Objects for requests and responses

### Infrastructure Layer (`src/infrastructure/`)
- **Database**: SQLAlchemy models and repository implementations
- **API**: FastAPI routes and dependencies
- **Security**: JWT token handling

### Configuration (`src/config/`)
- **Settings**: Environment-based configuration
- **Database**: Database connection setup

## Features

- User registration with email and username uniqueness validation
- Password strength validation
- JWT-based authentication (access and refresh tokens)
- Token validation endpoint for other microservices
- Role-based access control (superuser support)
- CORS configuration for frontend integration
- Comprehensive error handling

## Technology Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with asyncpg
- **ORM**: SQLAlchemy (async)
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt (passlib)
- **Validation**: Pydantic v2

## Prerequisites

- Python 3.11+
- PostgreSQL 14+
- Docker and Docker Compose (optional)

## Setup

### 1. Clone the repository
```bash
cd identity-service
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 5. Run database migrations
```bash
# Database tables are created automatically on startup
# For production, use Alembic migrations
```

### 6. Run the service
```bash
cd src
python main.py
```

The service will be available at `http://localhost:8001`

## Docker Deployment

### Build and run with Docker Compose
```bash
docker-compose up -d
```

### Build Docker image manually
```bash
docker build -t identity-service:latest .
docker run -p 8001:8001 --env-file .env identity-service:latest
```

## API Documentation

Once the service is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc
- **OpenAPI JSON**: http://localhost:8001/openapi.json

## API Endpoints

### Authentication
- `POST /api/v1/register` - Register a new user
- `POST /api/v1/login` - Authenticate and get tokens
- `POST /api/v1/validate` - Validate JWT token
- `GET /api/v1/me` - Get current user information

### Health Check
- `GET /api/v1/health` - Service health status
- `GET /` - Root endpoint with service info

### Admin (Superuser only)
- `GET /api/v1/admin/test` - Test admin access

## Testing

### Run all tests
```bash
pytest
```

### Run with coverage
```bash
pytest --cov=. --cov-report=html
```

### Run specific test types
```bash
# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/
```

## Project Structure

```
identity-service/
├── src/
│   ├── domain/                 # Domain layer (business logic)
│   │   ├── entities/          # Core entities
│   │   ├── value_objects/     # Value objects
│   │   ├── repositories/      # Repository interfaces
│   │   └── services/          # Domain services
│   ├── application/           # Application layer
│   │   ├── use_cases/        # Use cases
│   │   └── dto/              # Data Transfer Objects
│   ├── infrastructure/        # Infrastructure layer
│   │   ├── database/         # Database models and repositories
│   │   ├── api/              # FastAPI routes and dependencies
│   │   └── security/         # Security utilities
│   ├── config/               # Configuration
│   └── main.py              # Application entry point
├── tests/                    # Test suite
│   ├── unit/                # Unit tests
│   ├── integration/         # Integration tests
│   └── conftest.py         # Test configuration
├── Dockerfile              # Docker image definition
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
└── README.md             # This file
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name | Identity Service |
| `DEBUG` | Enable debug mode | False |
| `HOST` | Server host | 0.0.0.0 |
| `PORT` | Server port | 8001 |
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `SECRET_KEY` | JWT secret key | Required |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token expiration | 30 |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token expiration | 7 |

## Security Considerations

1. **Change the SECRET_KEY**: Use a strong, random string in production
2. **Use HTTPS**: Always use HTTPS in production
3. **Database Credentials**: Never commit real credentials
4. **Token Expiration**: Adjust token expiration based on security requirements
5. **CORS Origins**: Restrict CORS origins to trusted domains

## Development

### Code Style
```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/
```

### Database Migrations (Alembic)
```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Troubleshooting

### Database Connection Issues
- Verify PostgreSQL is running
- Check DATABASE_URL format
- Ensure database exists

### Import Errors
- Verify virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### Token Issues
- Verify SECRET_KEY is set
- Check token expiration settings
- Ensure system clock is synchronized

## Contributing

1. Follow Clean Architecture principles
2. Write tests for new features
3. Update documentation
4. Follow PEP 8 style guide
5. Use type hints

## License

This project is part of the Clinic Management System.

## Support

For issues and questions, please contact the development team.
