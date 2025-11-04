@echo off
REM Script para crear entorno virtual e instalar dependencias en Windows
echo ============================================
echo   ConsultaHacienda - Configuracion Windows
echo ============================================

REM Verificar si Python está disponible
echo 🔍 Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python no está instalado o no está en PATH
    echo 💡 Descarga Python desde: https://python.org
    echo � Asegurate de marcar "Add Python to PATH" durante la instalación
    pause
    exit /b 1
)

REM Mostrar versión de Python
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python encontrado: %PYTHON_VERSION%

REM Verificar que la versión sea compatible (3.8+)
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set MAJOR=%%a
    set MINOR=%%b
)
if %MAJOR% LSS 3 (
    echo ❌ Error: Python %PYTHON_VERSION% es muy antiguo
    echo 💡 Se requiere Python 3.8 o superior
    pause
    exit /b 1
)
if %MAJOR% EQU 3 if %MINOR% LSS 8 (
    echo ❌ Error: Python %PYTHON_VERSION% es muy antiguo  
    echo 💡 Se requiere Python 3.8 o superior
    pause
    exit /b 1
)

echo �🔧 Creando entorno virtual...
if exist venv (
    echo ⚠️  El entorno virtual ya existe. ¿Recrearlo? (S/N)
    choice /c SN /n /m "Presiona S para Sí, N para No: "
    if errorlevel 2 goto :activate_existing
    echo 🗑️  Eliminando entorno virtual existente...
    rmdir /s /q venv
)

python -m venv venv
if errorlevel 1 (
    echo ❌ Error creando entorno virtual
    pause
    exit /b 1
)

:activate_existing
echo 🔧 Activando entorno virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Error activando entorno virtual
    pause
    exit /b 1
)

echo 📦 Actualizando pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo ⚠️  Advertencia: No se pudo actualizar pip, continuando...
)

echo 📦 Instalando dependencias...
echo    Esto puede tardar varios minutos...

REM Instalar dependencias una por una para mejor manejo de errores
echo 📥 Instalando PySide6...
pip install "PySide6>=6.5.0"
if errorlevel 1 (
    echo ❌ Error instalando PySide6
    echo 💡 Tu versión de Python podría no ser compatible
    echo 💡 Versiones soportadas: Python 3.8-3.12
    echo 💡 Considera actualizar Python o usar una versión compatible
    pause
    exit /b 1
)

echo 📥 Instalando requests...
pip install "requests>=2.31.0"
if errorlevel 1 (
    echo ❌ Error instalando requests
    pause
    exit /b 1
)

echo 📥 Instalando PyInstaller...
pip install "pyinstaller>=5.13.0"
if errorlevel 1 (
    echo ❌ Error instalando PyInstaller
    pause
    exit /b 1
)

echo 🧪 Verificando instalación...
python -c "import PySide6; print('✅ PySide6:', PySide6.__version__)"
if errorlevel 1 (
    echo ❌ Error: PySide6 no se instaló correctamente
    pause
    exit /b 1
)

python -c "import requests; print('✅ requests:', requests.__version__)"
if errorlevel 1 (
    echo ❌ Error: requests no se instaló correctamente
    pause
    exit /b 1
)

echo.
echo ✅ ¡Instalación completada exitosamente!
echo.
echo � Información del sistema:
echo    Python: %PYTHON_VERSION%
echo    Entorno: venv\Scripts\python.exe
echo.
echo 🚀 Próximos pasos:
echo    💡 Ejecutar aplicación: run.bat
echo    💡 Compilar ejecutable: compile.bat
echo.
pause