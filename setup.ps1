# Script de PowerShell para configurar el proyecto en Windows
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "   ConsultaHacienda - Configuración Windows" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

# Verificar si Python está instalado
Write-Host "🔍 Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersionOutput = python --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Python no encontrado"
    }
    
    # Extraer versión
    $pythonVersion = $pythonVersionOutput -replace "Python ", ""
    Write-Host "✅ Python encontrado: $pythonVersion" -ForegroundColor Green
    
    # Verificar versión mínima (3.8)
    $version = [Version]$pythonVersion
    $minVersion = [Version]"3.8.0"
    
    if ($version -lt $minVersion) {
        Write-Host "❌ Error: Python $pythonVersion es muy antiguo" -ForegroundColor Red
        Write-Host "💡 Se requiere Python 3.8 o superior" -ForegroundColor Yellow
        Write-Host "💡 Descarga desde: https://python.org" -ForegroundColor Yellow
        exit 1
    }
    
} catch {
    Write-Host "❌ Python no está instalado o no está en PATH" -ForegroundColor Red
    Write-Host "💡 Descarga Python desde: https://python.org" -ForegroundColor Yellow
    Write-Host "💡 Asegurate de marcar 'Add Python to PATH' durante la instalación" -ForegroundColor Yellow
    exit 1
}

# Verificar si el entorno virtual ya existe
if (Test-Path "venv") {
    Write-Host "⚠️  El entorno virtual ya existe." -ForegroundColor Yellow
    $recreate = Read-Host "¿Recrear el entorno virtual? (S/N)"
    if ($recreate -match "^[Ss]") {
        Write-Host "🗑️  Eliminando entorno virtual existente..." -ForegroundColor Yellow
        Remove-Item -Recurse -Force "venv" -ErrorAction SilentlyContinue
    } else {
        Write-Host "📂 Usando entorno virtual existente..." -ForegroundColor Green
        & "venv\Scripts\Activate.ps1"
        Write-Host "✅ Entorno virtual activado" -ForegroundColor Green
        exit 0
    }
}

# Crear entorno virtual
Write-Host "🔧 Creando entorno virtual..." -ForegroundColor Yellow
try {
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        throw "Error creando entorno virtual"
    }
} catch {
    Write-Host "❌ Error creando entorno virtual: $_" -ForegroundColor Red
    exit 1
}

# Activar entorno virtual
Write-Host "🔧 Activando entorno virtual..." -ForegroundColor Yellow
try {
    & "venv\Scripts\Activate.ps1"
    if ($LASTEXITCODE -ne 0) {
        throw "Error activando entorno virtual"
    }
} catch {
    Write-Host "❌ Error activando entorno virtual: $_" -ForegroundColor Red
    Write-Host "💡 Intenta ejecutar: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Yellow
    exit 1
}

# Actualizar pip
Write-Host "📦 Actualizando pip..." -ForegroundColor Yellow
try {
    python -m pip install --upgrade pip
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠️  Advertencia: No se pudo actualizar pip, continuando..." -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️  Advertencia: Error actualizando pip: $_" -ForegroundColor Yellow
}

# Instalar dependencias una por una
Write-Host "📦 Instalando dependencias..." -ForegroundColor Yellow
Write-Host "   Esto puede tardar varios minutos..." -ForegroundColor Gray

# PySide6
Write-Host "📥 Instalando PySide6..." -ForegroundColor Cyan
try {
    pip install "PySide6>=6.5.0"
    if ($LASTEXITCODE -ne 0) {
        throw "Error instalando PySide6"
    }
} catch {
    Write-Host "❌ Error instalando PySide6: $_" -ForegroundColor Red
    Write-Host "💡 Tu versión de Python podría no ser compatible" -ForegroundColor Yellow
    Write-Host "💡 Versiones soportadas: Python 3.8-3.12" -ForegroundColor Yellow
    Write-Host "💡 Considera actualizar Python o usar una versión compatible" -ForegroundColor Yellow
    exit 1
}

# requests
Write-Host "📥 Instalando requests..." -ForegroundColor Cyan
try {
    pip install "requests>=2.31.0"
    if ($LASTEXITCODE -ne 0) {
        throw "Error instalando requests"
    }
} catch {
    Write-Host "❌ Error instalando requests: $_" -ForegroundColor Red
    exit 1
}

# PyInstaller
Write-Host "📥 Instalando PyInstaller..." -ForegroundColor Cyan
try {
    pip install "pyinstaller>=5.13.0"
    if ($LASTEXITCODE -ne 0) {
        throw "Error instalando PyInstaller"
    }
} catch {
    Write-Host "❌ Error instalando PyInstaller: $_" -ForegroundColor Red
    exit 1
}

# Verificar instalación
Write-Host "🧪 Verificando instalación..." -ForegroundColor Yellow
try {
    $pysideVersion = python -c "import PySide6; print(PySide6.__version__)" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ PySide6: $pysideVersion" -ForegroundColor Green
    } else {
        throw "PySide6 no se instaló correctamente"
    }
    
    $requestsVersion = python -c "import requests; print(requests.__version__)" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ requests: $requestsVersion" -ForegroundColor Green
    } else {
        throw "requests no se instaló correctamente"
    }
} catch {
    Write-Host "❌ Error en la verificación: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✅ ¡Configuración completada exitosamente!" -ForegroundColor Green
Write-Host ""
Write-Host "� Información del sistema:" -ForegroundColor Cyan
Write-Host "   Python: $pythonVersion" -ForegroundColor White
Write-Host "   Entorno: venv\Scripts\python.exe" -ForegroundColor White
Write-Host ""
Write-Host "🚀 Próximos pasos:" -ForegroundColor Cyan
Write-Host "   💡 Ejecutar aplicación: .\run.ps1" -ForegroundColor Yellow
Write-Host "   💡 Compilar ejecutable: .\compile.ps1" -ForegroundColor Yellow
Write-Host ""