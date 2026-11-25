# Partner A - Infrastructure and Networking

This folder contains screenshots documenting the infrastructure setup, deployment, networking, and security testing performed by Partner A (BSCS25053).

## Day 1 - 24 November 2026

- Ubuntu virtual machine setup
- Static IP configuration
- Network connectivity and ARP verification
- SSH connectivity
- PostgreSQL setup
- Flask Stub API testing
- NGINX reverse proxy testing
- Virtual machine snapshots

## Day 2 - 25 November 2026

### Application Deployment
- PostgreSQL database connection verification
- Backend deployment and service configuration
- Updated backend deployment
- React frontend deployment through NGINX

### HTTPS and Security
- Self-signed TLS certificate configuration
- Trusted HTTPS connection verification
- TLS certificate details verification
- Student registration and login over HTTPS
- JWT secure cookie verification

### Firewall and Network Analysis
- Pre-firewall Nmap port scanning
- Direct backend access before firewall configuration
- UFW firewall configuration on WEB and API VMs
- Post-firewall Nmap port scanning
- Verification of blocked direct backend access
- Verification of restricted SSH access
- Successful application access through the NGINX reverse proxy

### NGINX Rate Limiting
- Login endpoint rate limiting
- HTTP 429 Too Many Requests verification
- NGINX access log verification
- NGINX error log verification

### Docker VM Preparation
- Ubuntu Server installation on the third VM
- Static IP configuration (192.168.53.30)
- Network connectivity and SSH verification
- Docker Engine and Docker Compose installation
- Successful Docker hello-world container execution
- Docker VM snapshot creation

## Virtual Machine Configuration

| Virtual Machine | IP Address | Purpose |
|---|---|---|
| bscs25053-web | 192.168.53.10 | NGINX, frontend and HTTPS |
| bscs25053-api | 192.168.53.20 | Backend and PostgreSQL |
| bscs25053-docker | 192.168.53.30 | Docker environment |

Further application integration and final testing will be documented as the project progresses.
