#!/bin/bash
# Script para compilar la aplicación activando el entorno virtual

echo "🔧 Activando entorno virtual..."
source venv/bin/activate

echo "✅ Entorno virtual activado"
echo "📦 Compilando aplicación..."

python build.py