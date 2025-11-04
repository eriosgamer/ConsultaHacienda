#!/bin/bash
# Script para crear entorno virtual e instalar dependencias en Linux/macOS

echo "🔧 Configurando ConsultaHacienda..."

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no encontrado. Instala Python 3.8-3.12"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python: $PYTHON_VERSION"

# Crear entorno virtual
echo "📦 Creando entorno virtual..."
if [ -d "venv" ]; then
    rm -rf venv
fi
python3 -m venv venv

# Activar y instalar dependencias
echo "📥 Instalando dependencias..."
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

# Verificar instalación
echo "🧪 Verificando instalación..."
if python -c "import PySide6, requests; print('✅ Todo instalado correctamente')" 2>/dev/null; then
    echo "✅ ¡Listo! Usa ./run.sh para ejecutar la aplicación"
else
    echo "❌ Error en la instalación"
    echo "💡 Asegúrate de usar Python 3.8-3.12 (NO 3.13+)"
    exit 1
fi