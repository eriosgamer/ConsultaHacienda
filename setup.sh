#!/bin/bash
# Script para crear entorno virtual e instalar dependencias en Linux/macOS

echo "🔧 Configurando ConsultaHacienda..."


# Priorizar python3.12 en el PATH
if command -v python3.12 &> /dev/null; then
    export PATH="$(dirname $(command -v python3.12)):$PATH"
    PYTHON_CMD=python3.12
else
    echo "❌ Python 3.12 no encontrado. Instala Python 3.8-3.12."
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo "✅ Python: $PYTHON_VERSION"

# Crear entorno virtual
echo "📦 Creando entorno virtual..."
if [ -d "venv" ]; then
    rm -rf venv
fi
$PYTHON_CMD -m venv venv

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