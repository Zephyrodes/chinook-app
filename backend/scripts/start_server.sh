<<<<<<< HEAD
#!/usr/bin/env bash
set -euo pipefail

# Ejecuta uvicorn con workers. Asume env vars definidas: DATABASE_URL, etc.
# En producción usa un process manager (systemd, supervisor) y/o nginx reverse proxy.

APP_MODULE="backend.app.main:app"
WORKERS=${UVM_WORKERS:-4}
HOST=${UVM_HOST:-0.0.0.0}
PORT=${UVM_PORT:-8000}
LOG_LEVEL=${UVM_LOG_LEVEL:-info}

source .venv/bin/activate

exec uvicorn "$APP_MODULE" --host "$HOST" --port "$PORT" --workers "$WORKERS" --log-level "$LOG_LEVEL"
=======
#!/bin/bash
set -e

echo ">>> Starting FastAPI service..."

sudo systemctl daemon-reload
sudo systemctl enable fastapi
sudo systemctl restart fastapi

echo ">>> FastAPI started."
>>>>>>> ee8c1818a32ab4cfd07ded81a17c3b4ee60310e5
