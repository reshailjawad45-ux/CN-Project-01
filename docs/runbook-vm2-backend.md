
# VM2 Backend Deployment Runbook

Prepared by: Partner B (Roll No. 99)

Target VM: bscs25053-api
IP: 192.168.53.20
API Port: 8000
Database: PostgreSQL (labdb)

## Prerequisites

Partner A has already configured:
- Ubuntu Server VM2 and its static IP
- PostgreSQL database labdb
- PostgreSQL user labuser
- Network connectivity between VM1 and VM2

## Step 1: Get latest code

On VM2, clone the repository if not already cloned:

git clone https://github.com/reshailjawad45-ux/CN-Project-01.git

cd CN-Project-01

If already cloned, use git pull instead.

## Step 2: Copy backend

sudo mkdir -p /opt/backend
sudo cp -a backend/. /opt/backend/
sudo chown -R "$USER:$USER" /opt/backend

## Step 3: Install Python dependencies

cd /opt/backend

sudo apt update
sudo apt install -y python3-venv python3-pip

python3 -m venv venv
./venv/bin/python -m pip install -r requirements.txt gunicorn

## Step 4: Configure environment

sudo mkdir -p /etc/lab
sudo cp ~/CN-Project-01/deploy/app.env.example /etc/lab/app.env
sudo nano /etc/lab/app.env

Replace all placeholders with VM2's own credentials
and independently generated JWT and encryption keys.

DATABASE_URL must point to:
127.0.0.1:5432/labdb

Set COOKIE_SECURE=true.

sudo chmod 600 /etc/lab/app.env

Never commit real secrets to GitHub.

## Step 5: Configure systemd service

sudo cp ~/CN-Project-01/deploy/systemd/backend.service /etc/systemd/system/backend.service

sudo nano /etc/systemd/system/backend.service

Replace REPLACE_VM_USERNAME with the Ubuntu username.


## Step 6: Initialize database tables

Run these commands on VM2:

cd /opt/backend

sudo env PYTHONDONTWRITEBYTECODE=1 ./venv/bin/python -c "from dotenv import load_dotenv; load_dotenv('/etc/lab/app.env'); from app import create_app, db; import models; from sqlalchemy import inspect; app=create_app(); ctx=app.app_context(); ctx.push(); db.create_all(); print(inspect(db.engine).get_table_names()); ctx.pop()"

Expected output:

['records', 'users']

Both tables must exist in PostgreSQL labdb.

## Step 7: Start backend service

sudo systemctl daemon-reload
sudo systemctl enable --now backend
sudo systemctl status backend --no-pager

## Step 8: Verify backend

sudo ss -tulnp

Expected:
- Backend listening on 192.168.53.20:8000
- PostgreSQL listening on 127.0.0.1:5432

curl -i http://192.168.53.20:8000/api/v1/health

Expected JSON:
- hostname: bscs25053-api
- ip: 192.168.53.20
- db: true

## Troubleshooting

If the backend fails:

sudo journalctl -u backend -n 50 --no-pager

Share the command and full error output with Partner B.
Do not share passwords or secret keys.
