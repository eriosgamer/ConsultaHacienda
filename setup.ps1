# Script de PowerShell para configurar el proyecto en Windows
Write-Host "🔧 Configurando proyecto ConsultaHacienda..." -ForegroundColor Green

# Verificar si Python está instalado
try {
    $pythonVersion = python --version
    Write-Host "✅ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python no está instalado. Instala Python desde python.org" -ForegroundColor Red
    exit 1
}

# Crear entorno virtual
Write-Host "🔧 Creando entorno virtual..." -ForegroundColor Yellow
python -m venv venv

# Activar entorno virtual
Write-Host "🔧 Activando entorno virtual..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# Actualizar pip
Write-Host "📦 Actualizando pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Instalar dependencias
Write-Host "📦 Instalando dependencias..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host "✅ ¡Configuración completada!" -ForegroundColor Green
Write-Host "💡 Para ejecutar la aplicación: .\run.ps1" -ForegroundColor Cyan
Write-Host "💡 Para compilar: .\compile.ps1" -ForegroundColor Cyan