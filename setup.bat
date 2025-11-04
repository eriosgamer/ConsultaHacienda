@echo off
REM Script para crear entorno virtual e instalar dependencias en Windows

echo 🔧 Configurando ConsultaHacienda...

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no encontrado. Descarga desde python.org
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python: %PYTHON_VERSION%

REM Crear entorno virtual
echo 📦 Creando entorno virtual...
if exist venv rmdir /s /q venv
python -m venv venv

# Activar y instalar dependencias
echo 📥 Instalando dependencias...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

echo 🧪 Verificando instalación...
python -c "import PySide6, requests; print('✅ Todo instalado correctamente')"
if errorlevel 1 (
    echo ❌ Error en la instalación
    echo 💡 Asegúrate de usar Python 3.8-3.12 (NO 3.13+)
    pause
    exit /b 1
)

echo ✅ ¡Listo! Usa run.bat para ejecutar la aplicación
pause