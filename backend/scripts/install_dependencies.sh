#!/usr/bin/env bash
set -euo pipefail

# Este script se ejecuta en la instancia (Ubuntu). No contiene credenciales.
# Requisitos: python3.10+, pip disponible, usuario con permisos.

echo "==> Actualizando apt y instalando dependencias de sistema..."
sudo apt-get update -y
sudo apt-get install -y build-essential python3-venv python3-dev libpq-dev

# (Si usas pymysql no necesitas client lib; si usas mysqlclient, necesitarás libmysqlclient-dev)
sudo apt-get install -y default-libmysqlclient-dev

# Crear venv local si no existe
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

# Activar e instalar pip requirements
source .venv/bin/activate
pip install --upgrade pip
pip install -r backend/requirements.txt

echo "==> Dependencias instaladas."
