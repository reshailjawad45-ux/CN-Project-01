
# Docker Deployment Runbook

## CN Project 01 — Partner A Deployment Guide

Target VM: bscs25053-docker
IP Address: 192.168.53.30
Operating System: Ubuntu Server 24.04

## 1. Prerequisites

Docker Engine and Docker Compose must be installed.

Verify:

```bash
docker --version
docker compose version
docker run hello-world
```

The project repository must contain:

- backend/Dockerfile
- backend/.dockerignore
- docker/docker-compose.yml
- docker/.env.example
- docker/nginx/default.conf
- deploy/frontend-dist/

## 2. Download the Latest Project

If the repository is already cloned:

```bash
cd ~/CN-Project-01
git pull --rebase origin main
```

Otherwise:

```bash
cd ~
git clone https://github.com/reshailjawad45-ux/CN-Project-01.git
cd CN-Project-01
```

Verify the project files are present.

## 3. Generate the TLS Certificate

```bash
mkdir -p docker/certs

openssl req -x509 -newkey rsa:2048 -nodes -days 365 \
  -keyout docker/certs/web.key \
  -out docker/certs/web.crt \
  -subj "/CN=bscs25053-docker" \
  -addext "subjectAltName=DNS:bscs25053-docker,IP:192.168.53.30"

chmod 600 docker/certs/web.key
```

Verify:

```bash
openssl x509 -in docker/certs/web.crt \
  -noout -subject -issuer -dates
```

These files must not be committed to GitHub.

## 4. Configure Environment Variables

```bash
cd docker
cp .env.example .env
chmod 600 .env
nano .env
```

Generate secret values separately:

```bash
openssl rand -hex 24
openssl rand -hex 32
openssl rand -base64 32
```

Use them for:

- POSTGRES_PASSWORD (first command)
- JWT_SECRET (second command)
- ENC_KEY (third command)

Ensure DATABASE_URL contains the same PostgreSQL
password and uses host `db`, not 127.0.0.1.

Other required settings:

- POSTGRES_USER=labuser
- POSTGRES_DB=labdb
- LAB_IP=192.168.53.30
- COOKIE_SECURE=true

Save the file.

Never share or commit real passwords, JWT secrets,
encryption keys or the .env file.

## 5. Validate Docker Compose

From the docker/ directory:

```bash
docker compose config --quiet
```

No errors should appear.

## 6. Build and Start Containers

```bash
docker compose up -d --build
```

Check the containers:

```bash
docker compose ps
```

Expected services:

- web — NGINX
- api — Flask/Gunicorn
- db — PostgreSQL

Verify that NGINX configuration is valid:

```bash
docker compose exec web nginx -t
```

## 7. Verify Backend and Database

```bash
curl -k -i https://127.0.0.1/api/v1/health
```

Expected:

- HTTP 200
- db: true
- Docker VM IP: 192.168.53.30

If there is a problem:

```bash
docker compose logs --tail 50 api
docker compose logs --tail 50 db
docker compose logs --tail 50 web
```

Remove secrets or tokens before sharing logs.

## 8. Verify Container Network

```bash
docker network ls
docker network inspect lab-net
```

Verify internal service name resolution:

```bash
docker compose exec web getent hosts api
docker compose exec web getent hosts db
```

Only port 443 should be published to the host.

Verify:

```bash
docker compose ps
sudo ss -tulnp
```

Ports 8000 and 5432 must not be published externally.

## 9. Verify HTTPS From Windows

From the Windows host:

```powershell
curl.exe -k -i https://192.168.53.30/api/v1/health
```

Expected HTTP 200 and db: true.

Open:

https://192.168.53.30

A browser warning is expected for an untrusted
self-signed certificate unless it is trusted locally.

## 10. Test Application Features

Through the Docker HTTPS application, verify:

1. User registration
2. Login
3. Create, read, update and delete records
4. AES-encrypted phone storage in PostgreSQL
5. Password change
6. Logout
7. Admin access: 401, 403 and 200
8. Login rate limiting: HTTP 429

Collect screenshots and command outputs.

## 11. Verify Database Persistence

Create a test record through the application.

Stop the containers without deleting volumes:

```bash
docker compose down
```

Start them again:

```bash
docker compose up -d
```

Log in and confirm the test record still exists.

IMPORTANT:
Do NOT run `docker compose down -v` during this
test because it removes the named database volume.

## 12. Troubleshooting

Check all containers:

```bash
docker compose ps -a
```

Check API logs:

```bash
docker compose logs --tail 100 api
```

Check database logs:

```bash
docker compose logs --tail 100 db
```

Check NGINX logs:

```bash
docker compose logs --tail 100 web
```

If a deployment fails, share the command and
relevant sanitized terminal output with Partner B.

## 13. Required Evidence

Capture:

- Docker Compose services running
- HTTPS health endpoint with db: true
- Docker network inspection
- Internal DNS resolution
- Container ports and published port 443
- CRUD and admin test results
- Encrypted PostgreSQL phone field
- Login rate-limiting response
- Database persistence after recreation
- Relevant Docker logs

All evidence should include identifiable VM context
where practical.
