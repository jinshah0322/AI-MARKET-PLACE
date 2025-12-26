# AI Model Marketplace

A production-grade platform for publishing, discovering, and consuming AI models via APIs.

## Features

- Multi-vendor AI model marketplace
- Real-time inference APIs
- Usage-based billing with Stripe
- Event-driven microservices architecture
- Advanced search with Elasticsearch
- Distributed tracing and monitoring

## Tech Stack

- **Backend**: FastAPI (Python)
- **Databases**: PostgreSQL, MongoDB, Redis, TimescaleDB
- **Message Queue**: Kafka, RabbitMQ
- **Storage**: MinIO (S3-compatible)
- **Search**: Elasticsearch
- **Monitoring**: Prometheus, Grafana, Jaeger
- **ML**: ONNX Runtime, TorchServe

## Getting Started

### Prerequisites

- Docker & Docker Compose
- Python 3.11+
- Git

### Installation

1. Clone the repository
```bash
git clone <your-repo-url>
cd ai-marketplace
```

2. Start infrastructure services
```bash
cd infrastructure/docker
docker-compose up -d
```

3. Verify all services are running
```bash
docker-compose ps
```

4. Access service UIs:
- MongoDB Express: http://localhost:8081
- RabbitMQ Management: http://localhost:15672 (admin/admin123)
- Kibana: http://localhost:5601
- MinIO Console: http://localhost:9001 (minioadmin/minioadmin123)
- Grafana: http://localhost:3000 (admin/admin123)
- Prometheus: http://localhost:9090
- Jaeger: http://localhost:16686

## Project Structure
```
ai-marketplace/
├── services/           # Microservices
├── shared/            # Shared code
├── infrastructure/    # Docker, K8s configs
├── tests/            # Tests
└── docs/             # Documentation
```

## Development

Coming soon...

## License

MIT