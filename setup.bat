@echo off
REM Script para crear entorno virtual e instalar dependencias en Windows

echo 🔧 Creando entorno virtual...
python -m venv venv

echo 🔧 Activando entorno virtual...
call venv\Scripts\activate.bat

echo 📦 Actualizando pip...
python -m pip install --upgrade pip

echo 📦 Instalando dependencias...
pip install -r requirements.txt

echo ✅ ¡Instalación completada!
echo 💡 Ahora puedes usar: run.bat para ejecutar la aplicación
echo 💡 O usar: compile.bat para compilar un ejecutable
pause