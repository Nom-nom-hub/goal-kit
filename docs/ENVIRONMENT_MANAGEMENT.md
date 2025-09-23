# Environment Management for Goal-Dev-Spec

This document outlines the advanced environment management capabilities for Goal-Dev-Spec that exceed spec-kit functionality.

## Environment Directory Structure

```
.environments/
├── development/
│   ├── .env
│   ├── config.yaml
│   └── services.yaml
├── staging/
│   ├── .env
│   ├── config.yaml
│   └── services.yaml
├── production/
│   ├── .env
│   ├── config.yaml
│   └── services.yaml
└── testing/
    ├── unit-tests/
    │   ├── .env
    │   └── config.yaml
    ├── integration-tests/
    │   ├── .env
    │   └── config.yaml
    └── e2e-tests/
        ├── .env
        └── config.yaml
```

## Environment Configuration Files

### .env Files

Environment variables are stored in `.env` files with the following structure:

```bash
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp_dev
DB_USER=developer
DB_PASSWORD=securepassword

# API Keys
API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here

# Service URLs
API_BASE_URL=http://localhost:3000/api
FRONTEND_URL=http://localhost:3001

# Feature Flags
FEATURE_NEW_UI=true
FEATURE_BETA_ACCESS=false
```

### config.yaml Files

Structured configuration is stored in `config.yaml` files:

```yaml
# Application Configuration
app:
  name: "My Application"
  version: "1.0.0"
  debug: true

# Database Configuration
database:
  host: "localhost"
  port: 5432
  name: "myapp_dev"
  user: "developer"
  password: "securepassword"

# Logging Configuration
logging:
  level: "debug"
  format: "json"
  output: "console"

# Cache Configuration
cache:
  provider: "redis"
  host: "localhost"
  port: 6379
  ttl: 3600

# Security Configuration
security:
  jwt_secret: "your_jwt_secret_here"
  password_salt: "your_password_salt_here"
  rate_limit:
    requests_per_minute: 100
```

### services.yaml Files

Service configurations for microservices or external dependencies:

```yaml
# Services Configuration
services:
  authentication:
    url: "http://auth-service:3000"
    timeout: 5000
    retries: 3
  
  payment:
    url: "http://payment-service:3001"
    timeout: 10000
    retries: 2
    api_key: "payment_service_api_key"
  
  email:
    provider: "sendgrid"
    api_key: "sendgrid_api_key"
    from_email: "noreply@myapp.com"
  
  storage:
    provider: "aws_s3"
    region: "us-west-2"
    bucket: "myapp-storage"
    access_key: "aws_access_key"
    secret_key: "aws_secret_key"
```

## Environment Management Commands

The Goal-Dev-Spec CLI provides commands for environment management:

### Initialize Environments

```bash
# Initialize all environments
goal env init

# Initialize specific environment
goal env init --environment development
```

### Switch Environments

```bash
# Switch to development environment
goal env switch development

# Switch to staging environment
goal env switch staging

# Switch to production environment
goal env switch production
```

### List Environments

```bash
# List all environments
goal env list

# List with details
goal env list --verbose
```

### Validate Environments

```bash
# Validate current environment
goal env validate

# Validate specific environment
goal env validate --environment staging
```

## Environment Variables Management

### Loading Environment Variables

Environment variables are loaded in the following priority order:

1. Command-line arguments
2. Environment-specific `.env` file
3. Default values in configuration files
4. Built-in defaults

### Environment Variable Validation

The system validates environment variables against a schema:

```yaml
# Environment Variable Schema
DB_HOST:
  required: true
  type: string
  default: "localhost"

DB_PORT:
  required: true
  type: integer
  default: 5432
  min: 1
  max: 65535

API_KEY:
  required: true
  type: string
  pattern: "^[a-zA-Z0-9]{32}$"

FEATURE_NEW_UI:
  required: false
  type: boolean
  default: false
```

## Multi-Environment Workflows

### Development Workflow

1. Developer initializes development environment
2. Environment variables are loaded from `.environments/development/.env`
3. Services are configured from `.environments/development/services.yaml`
4. Application runs with development-specific settings

### Testing Workflow

1. Test runner initializes testing environment
2. Environment variables are loaded from `.environments/testing/unit-tests/.env`
3. Mock services are configured
4. Tests run with isolated environment

### Staging Workflow

1. Deployment pipeline initializes staging environment
2. Environment variables are loaded from `.environments/staging/.env`
3. Production-like services are configured
4. Application is deployed and validated

### Production Workflow

1. Deployment pipeline initializes production environment
2. Environment variables are loaded from `.environments/production/.env`
3. Production services are configured
4. Application is deployed with production settings

## Environment Security

### Sensitive Data Protection

1. Sensitive data is stored in encrypted form
2. Environment files are added to `.gitignore`
3. Access to environment files is restricted
4. Rotation policies are implemented for secrets

### Encryption at Rest

```yaml
# Encrypted Configuration
database:
  host: "localhost"
  port: 5432
  name: "myapp_dev"
  user: "developer"
  password: 
    encrypted: true
    value: "encrypted_password_here"
    algorithm: "AES-256-GCM"
```

### Access Control

Environment access is controlled through:

1. Role-based permissions
2. Audit logging
3. Time-based access
4. IP restrictions

## Environment Versioning

Environment configurations are versioned alongside the application:

```
.environments/
├── v1.0.0/
│   ├── development/
│   ├── staging/
│   └── production/
├── v1.1.0/
│   ├── development/
│   ├── staging/
│   └── production/
└── current -> v1.1.0/
```

This allows for:

1. Rollback to previous environment configurations
2. Parallel testing of environment changes
3. Audit trail of environment modifications
4. Consistent environments across deployments