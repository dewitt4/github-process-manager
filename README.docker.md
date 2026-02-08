# Docker Setup Guide

This guide covers how to run the GitHub Process Manager using Docker.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed
- [Docker Compose](https://docs.docker.com/compose/install/) installed (usually comes with Docker Desktop)

## Quick Start

### 1. Configure Environment Variables

Copy the `.env.template` to `.env` and update with your API keys:

```bash
cp .env.template .env
```

Edit `.env` and add:
- `GEMINI_API_KEY` - Your Google Gemini API key
- `GITHUB_TOKEN` - Your GitHub personal access token (optional)
- `GITHUB_REPO_URL` - Your GitHub repository URL (optional)

### 2. Build and Run with Docker Compose

**Development Mode** (with hot reload):
```bash
docker-compose up -d
```

**Production Mode**:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### 3. Access the Application

Open your browser and navigate to:
- **Application**: http://localhost:5000
- **Health Check**: http://localhost:5000/health

## Docker Commands

### View Logs
```bash
docker-compose logs -f app
```

### Stop the Application
```bash
docker-compose down
```

### Rebuild After Code Changes
```bash
docker-compose up -d --build
```

### Access Container Shell
```bash
docker-compose exec app /bin/bash
```

### Clean Up Everything (including volumes)
```bash
docker-compose down -v
```

## VS Code Dev Container

### Prerequisites
- [VS Code](https://code.visualstudio.com/)
- [Remote - Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

### Setup

1. Open the project folder in VS Code
2. Press `F1` and select **"Remote-Containers: Reopen in Container"**
3. VS Code will build the container and set up the development environment
4. All dependencies will be installed automatically

### Features

The dev container includes:
- Python 3.11 environment
- All project dependencies pre-installed
- VS Code extensions for Python development
- Git and GitHub CLI
- Auto-formatting and linting configured

## Volume Persistence

Docker Compose uses named volumes to persist data:

- **chroma_data**: Vector database storage
- **uploads_data**: Uploaded documents
- **reports_data**: Generated Word documents

These volumes persist even when containers are stopped or removed.

## Troubleshooting

### Port Already in Use
If port 5000 is already in use, edit `docker-compose.yml`:
```yaml
ports:
  - "8080:5000"  # Change 8080 to any available port
```

### Permission Issues
If you encounter permission issues with volumes:
```bash
docker-compose exec app chown -R $(id -u):$(id -g) /app/chroma_db /app/uploads /app/generated_reports
```

### Container Won't Start
Check logs for errors:
```bash
docker-compose logs app
```

### Clean Slate
Remove all containers, volumes, and images:
```bash
docker-compose down -v
docker rmi github-process-manager_app
docker-compose up -d --build
```

## Production Deployment

For production deployment:

1. Use `docker-compose.prod.yml`
2. Set `FLASK_DEBUG=False` in `.env`
3. Use a reverse proxy (nginx/traefik) for HTTPS
4. Set up proper secret management
5. Configure resource limits

Example with resource limits:
```yaml
services:
  app:
    # ... other config
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

## Security Notes

- Never commit your `.env` file
- Use Docker secrets in production for sensitive data
- Keep the Docker image updated
- Run containers as non-root user in production
- Use read-only filesystem where possible

## Building for Different Architectures

Build for ARM64 (e.g., Apple Silicon, Raspberry Pi):
```bash
docker buildx build --platform linux/arm64 -t github-process-manager:arm64 .
```

Build multi-architecture image:
```bash
docker buildx build --platform linux/amd64,linux/arm64 -t github-process-manager:latest .
```
