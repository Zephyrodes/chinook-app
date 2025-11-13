#!/bin/bash
set -e
# Start systemd service (systemd file must exist)
sudo systemctl daemon-reload
sudo systemctl restart fastapi || sudo systemctl start fastapi
