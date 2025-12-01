# Docker Lab

This folder contains a small multi-service demo composed with Docker Compose: a Flask API, a static frontend, an Nginx reverse proxy, a background worker, PostgreSQL and Redis.

Contents
- `api/` - Flask backend, `Dockerfile`, database initialization script `init.sql`.
- `frontend/` - static frontend and production Dockerfile.
- `nginx/` - reverse-proxy configuration and `Dockerfile`.
- `worker/` - background worker image and `worker.py`.
- `docker-compose.yml` - orchestrates all services.
- `env` - example environment variables for the stack.

Overview

- Nginx is the public entrypoint. It listens on host port 80 (`nginx` service) and forwards traffic to the frontend and API.
- The `frontend` is built as a static app and served through Nginx.
- The `api` is a Flask app (internal port `5000`) — Nginx proxies to it and a healthcheck is defined.
- `worker` runs asynchronous/background tasks and connects to the same DB/Redis instances as the API.
- `db` is PostgreSQL (image `postgres:15-alpine`) and runs the `api/init.sql` on first startup.
- `cache` is Redis (image `redis:7-alpine`) used for caching and as a queue backend.

Prerequisites

- Docker Desktop (Windows) or Docker Engine + Docker Compose
- PowerShell (examples below use PowerShell commands on Windows)

Quick start (PowerShell)

1. Copy the `env` file into a `.env` file that Docker Compose will pick up:

```powershell
Copy-Item .\env .env
```

2. Build and bring the stack up (two options):

- Using legacy Docker Compose:

```powershell
docker-compose up --build
```

- Using Docker CLI Compose (v2+):

```powershell
docker compose up --build
```

3. Detach mode (run in background):

```powershell
docker compose up --build -d
```

4. Stop and remove containers, networks and volumes (data will be removed):

```powershell
docker compose down -v
```

Useful commands

- Follow logs for a service (e.g., api or nginx):

```powershell
docker compose logs -f api
docker compose logs -f nginx
```

- List running containers:

```powershell
docker ps
```

- Run a one-off command in the worker image (e.g., to process a job manually):

```powershell
docker compose run --rm worker python worker.py
```

- Connect to the database container (replace container id/name as needed):

```powershell
# find container name
docker ps
# then exec into the container (example name: labs_dockerlab_db_1)
docker exec -it <db_container_name> psql -U $env:DB_USER -d $env:DB_NAME
```

Healthchecks & verification

- Nginx is published on host port `80` per `docker-compose.yml`.
- API healthcheck is defined; you can verify by curling the health endpoint through Nginx or directly (if you run port forwarding):

```powershell
curl http://localhost/health
```