#!/bin/bash
set -e
cd /opt/chinook/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# ensure permissions
chown -R ubuntu:ubuntu /opt/chinook/backend