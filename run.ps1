# Script de PowerShell para ejecutar la aplicación
Write-Host "🔧 Activando entorno virtual..." -ForegroundColor Yellow

# Activar entorno virtual
& "venv\Scripts\Activate.ps1"

Write-Host "✅ Entorno virtual activado" -ForegroundColor Green
Write-Host "📱 Ejecutando aplicación ConsultaHacienda..." -ForegroundColor Green

python main.py