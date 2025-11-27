#!/usr/bin/env bash
set -euo pipefail

echo "Stopping uvicorn processes..."
pkill -f "uvicorn" || true
echo "Stopped."
