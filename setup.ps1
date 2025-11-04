# Script de PowerShell para configurar el proyecto en Windows

Write-Host "🔧 Configurando ConsultaHacienda..." -ForegroundColor Green

# Verificar Python
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -ne 0) { throw "Python no encontrado" }
    Write-Host "✅ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python no encontrado. Descarga desde python.org" -ForegroundColor Red
    exit 1
}

# Crear entorno virtual
Write-Host "📦 Creando entorno virtual..." -ForegroundColor Yellow
if (Test-Path "venv") { Remove-Item -Recurse -Force "venv" }
python -m venv venv

# Activar y instalar dependencias
Write-Host "📥 Instalando dependencias..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"
python -m pip install --upgrade pip
pip install -r requirements.txt# Verificar instalación
Write-Host "🧪 Verificando instalación..." -ForegroundColor Yellow
try {
    python -c "import PySide6, requests; print('✅ Todo instalado correctamente')"
    Write-Host "✅ ¡Listo! Usa .\run.ps1 para ejecutar" -ForegroundColor Green
} catch {
    Write-Host "❌ Error en la instalación" -ForegroundColor Red
    Write-Host "💡 Asegúrate de usar Python 3.8-3.12 (NO 3.13+)" -ForegroundColor Yellow
}