![Banner](./assets/banner.webp)

A high-performance API for profanity detection powered by machine learning.

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Docker Build](https://github.com/valentinkolb/bad-words/actions/workflows/python-app.yml/badge.svg)](https://github.com/valentinkolb/bad-words/actions/workflows/python-app.yml)

---

. **[Quick Start](#quick-start)** . **[Features](#features)** . **[API Endpoints](#api-endpoints)** . **[Configuration](#configuration)** .
**[Local Development](#local-development)** . **[Docker Deployment](#docker-deployment)** . **[Testing](#testing)** . **[License](#license)** .

---

## Quick Start

The fastest way to run the Bad Words API is with Docker:

```bash
# Pull and run the latest version
docker run -p 8000:8000 ghcr.io/valentinkolb/bad-words:latest

# Test the API
curl -X POST "http://localhost:8000/api/v1/check" \
  -H "Content-Type: application/json" \
  -d '{"text": "This message contains bad language like sh*t"}'
```

## Features

- **Machine Learning-Based Detection**: Utilizes pre-trained transformer models for accurate profanity detection
- **High Performance**: Optimized for speed with asynchronous processing and caching
- **Language Support**: Works with multiple languages (currently optimized for German)
- **Configurable Settings**: Easily adjust detection thresholds, rate limits, and more
- **Containerized**: Fully dockerized for easy deployment in any environment
- **Well-Documented API**: Interactive documentation with Swagger UI
- **Rate Limiting**: Built-in protection against abuse
- **Model Caching**: Local model storage for fast startup times

## API Endpoints

### Check Text for Profanity

```http
POST /api/v1/check
```

#### Request

```json
{
  "text": "String to check for profanity"
}
```

#### Response

```json
{
  "is_profane": true,
  "confidence": 0.92,
  "original_text": "String to check for profanity"
}
```

### Health Check

```http
GET /api/v1/health
```

#### Response

```json
{
  "status": "ok",
  "version": "1.0.0"
}
```

### Configuration Info

```http
GET /api/v1/config
```

#### Response

```json
{
  "version": "1.0.0",
  "api_title": "Bad Words API",
  "api_description": "An API for profanity detection",
  "rate_limit": "10/minute",
  "max_text_length": 500,
  "model_name": "ml6team/distilbert-base-german-cased-toxic-comments"
}
```

## Configuration

The Bad Words API can be configured through environment variables:

| Environment Variable | Description | Default Value |
|---------------------|-------------|---------------|
| `LOG_LEVEL` | Logging level | `INFO` |
| `DATA_DIR` | Directory for storing model files | `/app/data` |
| `API_TITLE` | Name of the API | `Bad Words API` |
| `API_DESCRIPTION` | Description of the API | `An API for profanity detection` |
| `API_VERSION` | API version | `1.0.0` |
| `MAX_TEXT_LENGTH` | Maximum text length allowed | `500` |
| `RATE_LIMIT_DEFAULT` | Default rate limit | `10/minute` |
| `MODEL_NAME` | ML model for profanity detection | `ml6team/distilbert-base-german-cased-toxic-comments` |

## Local Development

### Prerequisites

- Python 3.9 or higher
- [UV](https://github.com/astral-sh/uv) (for package management)

### Setup

```bash
# Clone the repository
git clone https://github.com/valentinkolb/bad-words.git
cd bad-words

# Install dependencies
uv sync --locked --dev

# Run the API in development mode
python main.py
```

Visit `http://localhost:8000/docs` for the interactive API documentation.

### Development Commands

The project includes a Makefile for common development tasks:

```bash
# Install dependencies
make install-dev

# Format code
make format

# Lint code
make lint

# Run tests
make test

# Run development server
make dev

# Run production server
make run

# Clean up cache and temporary files
make clean
```

## Docker Deployment

### Docker

#### Use Pre-built Image

You can pull the pre-built Docker image from GitHub Container Registry:

```bash
# Pull the latest image
docker pull ghcr.io/valentinkolb/bad-words:latest

# Run the image
docker run -p 8000:8000 ghcr.io/valentinkolb/bad-words:latest
```

#### Build and Run

```bash
# Build the image
docker build -t bad-words-api .

# Run the container
docker run -p 8000:8000 bad-words-api

# Run with custom environment variables
docker run -p 8000:8000 \
  -e LOG_LEVEL=DEBUG \
  -e MAX_TEXT_LENGTH=1000 \
  -e RATE_LIMIT_DEFAULT=20/minute \
  bad-words-api
```

#### Using Docker Compose

```bash
# Set up and start the API with Docker Compose
docker compose up

# Run in detached mode
docker compose up -d

# Stop the API
docker compose down
```

### Docker Tags

The following tags are available on GitHub Container Registry:

- `latest`: The most recent stable release
- `x.y.z`: Specific version releases (e.g., `1.0.0`)
- `dev-xxxxx`: Development builds with short commit hash

## Testing

The project uses pytest for testing:

```bash
# Run all tests
make test

# Run tests with coverage
make test-cov
```

## Linting and Formatting

The project uses [ruff](https://github.com/astral-sh/ruff) for linting and formatting via the Makefile commands:

```bash
# Lint code
make lint

# Format code
make format
```
## CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment:

- **Linting**: Checks code quality with ruff
- **Testing**: Runs tests on multiple Python versions
- **Building**: Builds and publishes Docker images to GitHub Container Registry

## License

This project is distributed under the MIT License. See [LICENSE](LICENSE) for details.
