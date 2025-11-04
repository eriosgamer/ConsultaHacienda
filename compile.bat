@echo off
REM Script para compilar la aplicación activando el entorno virtual en Windows

echo 🔧 Activando entorno virtual...
call venv\Scripts\activate.bat

echo ✅ Entorno virtual activado
echo 📦 Compilando aplicación...

python build.py
pause