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


## Day 3 - 26 November 2026

### Updated Application Deployment
- Synchronized WEB and API VMs with the updated GitHub code (commit a8612d6).
- Created backups of the existing backend and frontend.
- Verified encryption key compatibility and Python dependencies.
- Deployed the updated Flask backend and React frontend.
- Verified PostgreSQL connectivity and NGINX configuration.

### CRUD and Encryption Testing
- Successful record creation (HTTP 201).
- Successful record retrieval (HTTP 200).
- Successful record update (HTTP 200).
- Successful record deletion (HTTP 200).
- Verified encrypted phone number storage in PostgreSQL and correct decryption in the frontend.

### Role-Based Access Control (RBAC)
- Unauthenticated access rejected (HTTP 401).
- Normal student access to admin API rejected (HTTP 403).
- Authorized admin access successful (HTTP 200).
- Verified student and admin roles in PostgreSQL.

### Authentication Testing
- Successful password change.
- Old password rejected.
- New password accepted.
- Successful logout and rejection of protected API access after logout.

### Network and API Evidence
- NGINX authentication and RBAC status codes.
- NGINX CRUD request status codes.
- NGINX password change and login verification.

## Day 4 – TLS, Firewall and Application Security Verification

**Date:** 27 November 2026  
**Contributor:** Partner A (BSCS25053)

### Completed Work

- Verified REST API error responses (400, 401 and 404).
- Verified corresponding NGINX status code logs.
- Updated the TLS certificate with the required hostname and IP SAN entries.
- Verified TLS 1.3, certificate trust and HTTPS connectivity.
- Verified HTTP-to-HTTPS redirection.
- Verified UFW rules on both WEB and API VMs.
- Completed firewall connectivity tests.
- Performed post-firewall Nmap scans from the Windows host.
- Verified bcrypt password hashing.
- Verified JWT cookie security flags and decoded JWT header and payload.
- Verified backend service startup logs.
- Compared encrypted database storage with decrypted frontend data.
- Verified network addressing, routing, ARP tables, listening ports and bidirectional connectivity.
- Generated and verified the Docker VM TLS certificate with hostname and IP SAN entries, secured the private key, and saved a VM snapshot.

### Firewall Configuration Evidence

- `deploy/ufw/vm1_ufw.txt`
- `deploy/ufw/vm2_ufw.txt`

### Pending Work

- Remaining TLS command evidence and pre-firewall scan evidence.
- Backend HTTP access log evidence.
- Docker application deployment and verification.
- Network packet analysis and Break & Fix troubleshooting tasks.

### Pending Observation
- Previously loaded records remained visible in the frontend after an authentication failure. Backend access was correctly denied. Frontend session handling requires review by Partner B.

A total of 16 evidence screenshots were collected for Day 3.


## Day 5 – Docker Deployment and Security Verification (28 November 2026)

### Completed Tasks – Partner A (BSCS25053)

- Successfully deployed NGINX, Flask API and PostgreSQL using Docker Compose on VM3 (192.168.53.30).
- Verified container startup, database health and HTTPS API connectivity.
- Configured certificate trust and hostname resolution on the Windows client.
- Verified registration, login and complete CRUD operations.
- Verified bcrypt password hashing and AES-encrypted database fields.
- Verified JWT cookie security flags.
- Tested role-based access control with HTTP 200, 401 and 403 responses.
- Verified NGINX rate limiting with HTTP 429 responses and corresponding logs.
- Confirmed that only HTTPS port 443 is published, while ports 80, 8000 and 5432 are inaccessible from the Windows client.
- Verified internal Docker bridge networking and service-name resolution.
- Successfully tested password change, old password rejection, new password login and logout.

### Docker Network

| Container | Internal IP | Service Name |
|---|---|---|
| NGINX | 172.18.0.4 | web |
| Flask API | 172.18.0.3 | api |
| PostgreSQL | 172.18.0.2 | db |

Network: `lab-net` (bridge)

Container IP addresses may change when containers are recreated. Internal communication uses Docker service names.

### Security Notes

- Only HTTPS port 443 is published externally.
- Backend and database ports are not published.
- Environment secrets and TLS private keys are stored locally and excluded from Git.
- Security verification screenshots are available in the evidence directory.

### Result

Docker deployment and core application security tests completed successfully. Remaining network analysis, troubleshooting and final comparison documentation are pending.
