# AI Model Marketplace

A production-grade platform where developers can publish, monetize, and consume AI models via simple APIs.

## 🎯 Project Overview

**What we're building:**
- Model publishers upload and monetize their ML models
- Consumers discover and use models via REST APIs
- Usage-based billing with Stripe
- Real-time inference at scale
- Event-driven microservices architecture

## 🏗️ Architecture
```
┌─────────────┐
│ API Gateway │ ← All requests enter here
└──────┬──────┘
       │
   ┌───┴───────────────────────┐
   │                           │
┌──▼───────┐         ┌────────▼────────┐
│   Auth   │         │ Model Registry  │
│ Service  │         │    Service      │
└──────────┘         └─────────────────┘
       │                     │
       └──────┬──────────────┘
              │
      ┌───────▼────────┐
      │   Inference    │
      │    Service     │
      └────────────────┘
```

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python 3.11+)
- **Databases**: PostgreSQL, MongoDB, Redis, TimescaleDB
- **Message Queue**: Kafka, RabbitMQ
- **Storage**: MinIO (S3-compatible)
- **Search**: Elasticsearch
- **Monitoring**: Prometheus, Grafana, Jaeger
- **ML**: ONNX Runtime, PyTorch, TensorFlow
- **Payments**: Stripe

## 📋 Prerequisites

- Python 3.11 or 3.12
- Poetry (Python dependency manager)
- Docker Desktop
- Git
- 8GB+ RAM (for running all services)

## 🚀 Getting Started

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd "AI MARKET PLACE"
```

### 2. Install Dependencies
```bash
# Install Poetry if you haven't
# Windows (PowerShell):
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -

# Mac/Linux:
curl -sSL https://install.python-poetry.org | python3 -

# Install project dependencies
poetry install

# Activate virtual environment
poetry shell
```

### 3. Setup Environment Variables
```bash
# Copy example env file
copy .env.example infrastructure\docker\.env

# Edit the .env file with your values
notepad infrastructure\docker\.env
```

### 4. Start Infrastructure Services
```bash
# Navigate to docker directory
cd infrastructure\docker

# Start all services (first time takes 5-10 minutes)
docker-compose up -d

# Check all services are running
docker-compose ps

# View logs
docker-compose logs -f
```

### 5. Verify Services
```bash
# PostgreSQL
docker exec -it ai-marketplace-postgres psql -U postgres -c "SELECT version();"

# MongoDB
docker exec -it ai-marketplace-mongodb mongosh --eval "db.version()"

# Redis
docker exec -it ai-marketplace-redis redis-cli -a redis123 ping

# Elasticsearch
curl http://localhost:9200
```

## 🌐 Access Service UIs

Once Docker is running, access these URLs:

| Service | URL | Credentials |
|---------|-----|-------------|
| RabbitMQ Management | http://localhost:15672 | admin / admin123 |
| MinIO Console | http://localhost:9001 | minioadmin / minioadmin123 |
| Kibana | http://localhost:5601 | - |
| Prometheus | http://localhost:9090 | - |
| Grafana | http://localhost:3000 | admin / admin123 |
| Jaeger | http://localhost:16686 | - |

## 📁 Project Structure
```
AI MARKET PLACE/
├── services/                 # Microservices
│   ├── gateway/             # API Gateway (entry point)
│   ├── auth/                # Authentication & Authorization
│   ├── model-registry/      # Model upload & management
│   ├── inference/           # Run model predictions
│   ├── billing/             # Stripe integration
│   ├── usage-tracking/      # Track API usage
│   ├── marketplace/         # Browse & discover models
│   ├── notification/        # Emails, webhooks
│   ├── analytics/           # Usage analytics
│   └── storage/             # File storage (MinIO)
│
├── shared/                   # Shared code
│   ├── common/              # Common utilities
│   ├── schemas/             # Shared Pydantic schemas
│   └── utils/               # Helper functions
│
├── infrastructure/           # Infrastructure configs
│   ├── docker/              # Docker Compose
│   ├── kubernetes/          # K8s manifests (future)
│   └── terraform/           # Infrastructure as Code (future)
│
├── tests/                    # All tests
├── docs/                     # Documentation
├── scripts/                  # Utility scripts
├── pyproject.toml           # Poetry dependencies
└── README.md                # This file
```

## 🔧 Development Commands

### Install Dependencies
```bash
poetry install
```

### Format Code
```bash
poetry run black services/ shared/ tests/
poetry run isort services/ shared/ tests/
```

### Run Linters
```bash
poetry run flake8 services/ shared/ tests/
poetry run mypy services/ shared/
```

### Run Tests
```bash
# All tests
poetry run pytest

# With coverage
poetry run pytest --cov

# Specific test file
poetry run pytest tests/test_auth.py

# Specific test
poetry run pytest tests/test_auth.py::test_user_login
```

### Docker Commands
```bash
# Start all services
cd infrastructure\docker
docker-compose up -d

# Stop all services
docker-compose down

# View logs (all services)
docker-compose logs -f

# View logs (specific service)
docker-compose logs -f postgres

# Restart a service
docker-compose restart postgres

# Stop and remove everything (including data)
docker-compose down -v
```

## 📚 Development Workflow

### Daily Workflow
```bash
# 1. Start Docker services
cd infrastructure\docker
docker-compose up -d

# 2. Activate Poetry environment
cd ..\..
poetry shell

# 3. Run your service
cd services\auth
uvicorn api.main:app --reload --port 8001

# 4. In another terminal, run tests
poetry run pytest tests/

# 5. Before committing
poetry run black .
poetry run isort .
poetry run pytest
```

### Adding a New Dependency
```bash
# Production dependency
poetry add package-name

# Development dependency
poetry add --group dev package-name

# Update all dependencies
poetry update
```

## 🧪 Testing

### Test Structure
```
tests/
├── unit/                    # Unit tests (fast, isolated)
│   ├── test_auth.py
│   ├── test_models.py
│   └── test_schemas.py
├── integration/             # Integration tests (with database)
│   ├── test_auth_flow.py
│   └── test_payment_flow.py
└── e2e/                     # End-to-end tests (full system)
    └── test_user_journey.py
```

### Running Different Test Types
```bash
# Unit tests only (fast)
poetry run pytest tests/unit/

# Integration tests (slower)
poetry run pytest tests/integration/

# End-to-end tests (slowest)
poetry run pytest tests/e2e/

# Run with specific markers
poetry run pytest -m "not slow"
```

## 🐛 Debugging

### View Service Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f postgres
docker-compose logs -f mongodb
docker-compose logs -f kafka

# Last 100 lines
docker-compose logs --tail=100 postgres
```

### Access Database
```bash
# PostgreSQL
docker exec -it ai-marketplace-postgres psql -U postgres -d ai_marketplace

# MongoDB
docker exec -it ai-marketplace-mongodb mongosh -u admin -p admin123

# Redis
docker exec -it ai-marketplace-redis redis-cli -a redis123
```

### Check Service Health
```bash
# All services status
docker-compose ps

# Specific service
docker-compose ps postgres

# Restart unhealthy service
docker-compose restart postgres
```

## 🚨 Common Issues

### Issue: Port Already in Use
```bash
# Find what's using the port (Windows)
netstat -ano | findstr :5432

# Kill the process
taskkill /PID <process_id> /F

# Or change port in docker-compose.yml
```

### Issue: Docker Services Won't Start
```bash
# Clean everything and restart
docker-compose down -v
docker system prune -a
docker-compose up -d
```

### Issue: Poetry Install Fails
```bash
# Clear Poetry cache
poetry cache clear pypi --all

# Reinstall
poetry install
```

## 📖 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## 🗺️ Development Roadmap

- [x] Project setup & infrastructure
- [ ] Auth service (Week 2-3)
- [ ] API Gateway (Week 3-4)
- [ ] Model Registry (Week 5-6)
- [ ] Inference Service (Week 6-7)
- [ ] Billing Service (Week 8-9)
- [ ] Event-driven architecture (Week 10-11)
- [ ] Testing & documentation (Week 13-14)
- [ ] Deployment (Week 15-16)

## 📄 License

MIT

## 👥 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Format code (`poetry run black . && poetry run isort .`)
4. Run tests (`poetry run pytest`)
5. Commit changes (`git commit -m 'Add amazing feature'`)
6. Push to branch (`git push origin feature/amazing-feature`)
7. Open Pull Request

## 📧 Contact

Your Name - your.email@example.com

Project Link: [https://github.com/yourusername/ai-marketplace](https://github.com/yourusername/ai-marketplace)
```

**Explanation:**
- Complete documentation for your project
- Clear setup instructions
- Common commands reference
- Troubleshooting guide
- Makes onboarding new developers easy

---

## ✅ Checkpoint: What You Should Have Now
```
AI MARKET PLACE/
├── services/          ✅ Created
├── shared/            ✅ Created
├── infrastructure/    ✅ Created
├── tests/             ✅ Created
├── .gitignore         ✅ Created
├── .env.example       ✅ Created
├── README.md          ✅ Created
└── pyproject.toml     ✅ Updated with configs