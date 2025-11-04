@echo off
REM Script de diagnóstico para problemas en Windows
echo ============================================
echo   ConsultaHacienda - Diagnóstico Windows
echo ============================================

echo 🔍 Información del sistema:
echo    SO: %OS%
echo    Arquitectura: %PROCESSOR_ARCHITECTURE%
ver

echo.
echo 🐍 Información de Python:
python --version 2>nul
if errorlevel 1 (
    echo ❌ Python no encontrado en PATH
    echo 💡 Verifica que Python esté instalado y en PATH
) else (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo ✅ Versión: %PYTHON_VERSION%
    
    echo    Ubicación: 
    where python 2>nul
    
    echo    Módulos pip disponibles:
    python -m pip --version 2>nul
    if errorlevel 1 (
        echo ❌ pip no disponible
    ) else (
        echo ✅ pip disponible
    )
)

echo.
echo 📦 Estado del entorno virtual:
if exist venv (
    echo ✅ Entorno virtual existe: venv\
    if exist venv\Scripts\python.exe (
        echo ✅ Python en venv: venv\Scripts\python.exe
        venv\Scripts\python.exe --version
    ) else (
        echo ❌ Python no encontrado en venv
    )
    
    if exist venv\Scripts\pip.exe (
        echo ✅ pip en venv disponible
    ) else (
        echo ❌ pip no encontrado en venv
    )
) else (
    echo ❌ Entorno virtual no existe
)

echo.
echo 📋 Dependencias instaladas:
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    
    echo    Verificando PySide6...
    python -c "import PySide6; print('✅ PySide6:', PySide6.__version__)" 2>nul
    if errorlevel 1 echo ❌ PySide6 no instalado
    
    echo    Verificando requests...
    python -c "import requests; print('✅ requests:', requests.__version__)" 2>nul
    if errorlevel 1 echo ❌ requests no instalado
    
    echo    Verificando PyInstaller...
    python -c "import PyInstaller; print('✅ PyInstaller:', PyInstaller.__version__)" 2>nul
    if errorlevel 1 echo ❌ PyInstaller no instalado
    
    echo    Lista completa de paquetes:
    pip list --format=freeze 2>nul | findstr -i "pyside6 requests pyinstaller"
) else (
    echo ❌ No se puede activar entorno virtual
)

echo.
echo 🔧 Archivos del proyecto:
if exist main.py (
    echo ✅ main.py existe
) else (
    echo ❌ main.py no encontrado
)

if exist requirements.txt (
    echo ✅ requirements.txt existe
    echo    Contenido:
    type requirements.txt
) else (
    echo ❌ requirements.txt no encontrado
)

echo.
echo 💡 Sugerencias de solución:
echo.
echo Si Python no está en PATH:
echo    - Reinstala Python desde python.org
echo    - Marca "Add Python to PATH" durante la instalación
echo.
echo Si PySide6 falla al instalar:
echo    - Verifica que tu Python sea 3.8-3.12
echo    - Intenta: pip install --upgrade pip setuptools wheel
echo    - Usa requirements-alt.txt: pip install -r requirements-alt.txt
echo.
echo Si el entorno virtual falla:
echo    - Elimina la carpeta venv manualmente
echo    - Ejecuta setup.bat nuevamente
echo.
echo Para más ayuda, revisa WINDOWS.md
echo.
pause