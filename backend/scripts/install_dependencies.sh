#!/bin/bash
set -e

echo ">>> Installing dependencies..."

# CodeDeploy copies backend/ into /opt/chinook/backend
cd /opt/chinook/backend

# Create venv if not exists
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

# Install requirements
pip install --upgrade pip
pip install -r requirements.txt

# Install FastAPI systemd service
sudo cp scripts/fastapi.service /etc/systemd/system/fastapi.service
sudo systemctl daemon-reload

# Adjust permissions
sudo chown -R ubuntu:ubuntu /opt/chinook/backend

echo ">>> Dependencies installed."
