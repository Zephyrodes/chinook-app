#!/bin/bash
set -e

echo ">>> Stopping FastAPI service..."

sudo systemctl stop fastapi || true

echo ">>> FastAPI stopped."
