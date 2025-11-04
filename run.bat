@echo off
REM Script para activar el entorno virtual y ejecutar la aplicación en Windows

echo 🔧 Activando entorno virtual...
call venv\Scripts\activate.bat

echo ✅ Entorno virtual activado
echo 📱 Ejecutando aplicación ConsultaHacienda...

python main.py
pause