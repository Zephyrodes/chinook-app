<<<<<<< HEAD
#!/usr/bin/env bash
set -euo pipefail

echo "Stopping uvicorn processes..."
pkill -f "uvicorn" || true
echo "Stopped."
=======
#!/bin/bash
set -e

echo ">>> Stopping FastAPI service..."

sudo systemctl stop fastapi || true

echo ">>> FastAPI stopped."
>>>>>>> ee8c1818a32ab4cfd07ded81a17c3b4ee60310e5
