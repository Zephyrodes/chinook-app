#!/bin/bash
set -e

echo ">>> Starting FastAPI service..."

sudo systemctl daemon-reload
sudo systemctl enable fastapi
sudo systemctl restart fastapi

echo ">>> FastAPI started."
