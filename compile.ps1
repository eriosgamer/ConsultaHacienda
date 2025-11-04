# Script de PowerShell para compilar la aplicación
Write-Host "🔧 Activando entorno virtual..." -ForegroundColor Yellow

# Activar entorno virtual
& "venv\Scripts\Activate.ps1"

Write-Host "✅ Entorno virtual activado" -ForegroundColor Green
Write-Host "📦 Compilando aplicación..." -ForegroundColor Green

python build.py

Write-Host "🎉 ¡Compilación completada!" -ForegroundColor Green