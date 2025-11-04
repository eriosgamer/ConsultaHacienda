@echo off
REM Script de instalación de emergencia para Windows
echo ============================================
echo   ConsultaHacienda - Instalación de Emergencia
echo ============================================

echo 🚨 Este script instala versiones específicas conocidas por funcionar
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no encontrado. Instala Python primero desde python.org
    pause
    exit /b 1
)

REM Obtener versión de Python
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo 🐍 Python detectado: %PYTHON_VERSION%

REM Crear entorno si no existe
if not exist venv (
    echo 🔧 Creando entorno virtual...
    python -m venv venv
)

echo 🔧 Activando entorno virtual...
call venv\Scripts\activate.bat

echo 📦 Actualizando herramientas básicas...
python -m pip install --upgrade pip setuptools wheel

echo 📦 Instalando versiones específicas compatibles...

REM Determinar versiones según Python
echo %PYTHON_VERSION% | findstr "3.8" >nul
if not errorlevel 1 (
    echo 📥 Python 3.8 detectado - usando PySide6 6.5.3
    pip install PySide6==6.5.3
    goto install_rest
)

echo %PYTHON_VERSION% | findstr "3.9" >nul
if not errorlevel 1 (
    echo 📥 Python 3.9 detectado - usando PySide6 6.6.3
    pip install PySide6==6.6.3
    goto install_rest
)

echo %PYTHON_VERSION% | findstr "3.10" >nul
if not errorlevel 1 (
    echo 📥 Python 3.10 detectado - usando PySide6 6.7.2
    pip install PySide6==6.7.2
    goto install_rest
)

REM Para 3.11, 3.12 y otros
echo 📥 Usando PySide6 más reciente compatible
pip install PySide6==6.8.0

:install_rest
if errorlevel 1 (
    echo ❌ Error instalando PySide6
    echo 💡 Intenta instalar Visual C++ Redistributable
    echo 💡 O usa una versión diferente de Python
    pause
    exit /b 1
)

echo 📥 Instalando requests...
pip install requests==2.31.3
if errorlevel 1 (
    echo ❌ Error instalando requests
    pause
    exit /b 1
)

echo 📥 Instalando PyInstaller...
pip install pyinstaller==6.3.0
if errorlevel 1 (
    echo ❌ Error instalando PyInstaller
    pause
    exit /b 1
)

echo 🧪 Verificando instalación...
python -c "import PySide6; print('✅ PySide6 OK')"
python -c "import requests; print('✅ requests OK')"
python -c "import PyInstaller; print('✅ PyInstaller OK')"

if errorlevel 1 (
    echo ❌ Alguna verificación falló
    pause
    exit /b 1
)

echo.
echo ✅ ¡Instalación de emergencia completada!
echo 💡 Prueba ejecutar: run.bat
echo.
pause