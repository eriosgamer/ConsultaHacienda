#!/bin/bash
# Script para activar el entorno virtual y ejecutar la aplicación

echo "🔧 Activando entorno virtual..."
source venv/bin/activate

echo "✅ Entorno virtual activado"
echo "📱 Ejecutando aplicación ConsultaHacienda..."

python main.py