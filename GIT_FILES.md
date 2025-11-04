# 📁 Control de Archivos - ConsultaHacienda

## ✅ Archivos incluidos en el repositorio

### Código fuente
- `main.py` - Aplicación principal
- `build.py` - Script de compilación
- `requirements.txt` - Dependencias de Python

### Scripts de ejecución
- `run.sh` / `run.bat` / `run.ps1` - Ejecutar aplicación
- `compile.sh` / `compile.bat` / `compile.ps1` - Compilar aplicación  
- `setup.bat` / `setup.ps1` - Configuración inicial (Windows)

### Documentación
- `README.md` - Documentación principal
- `WINDOWS.md` - Instrucciones específicas para Windows
- `GIT_FILES.md` - Este archivo

### Configuración
- `.gitignore` - Archivos a ignorar
- `.gitattributes` - Configuración de archivos de texto
- `.github/workflows/build.yml` - GitHub Actions para CI/CD

## ❌ Archivos ignorados (no subidos a GitHub)

### Entornos virtuales
```
venv/                    # Entorno virtual principal
env/                     # Entornos alternativos
.venv/                   # Entornos ocultos
ENV/                     # Variante mayúsculas
```

### Archivos de compilación
```
build/                   # Archivos temporales de PyInstaller
dist/                    # Ejecutables generados
release/                 # Ejecutables finales
*.spec                   # Archivos de configuración de PyInstaller
ConsultaHacienda.spec   # Spec file específico
```

### Cache de Python
```
__pycache__/            # Cache de bytecode
*.pyc                   # Archivos compilados
*.pyo                   # Archivos optimizados
*.pyd                   # Extensiones de Python
```

### Archivos del sistema
```
.DS_Store               # Archivos de macOS
Thumbs.db              # Cache de Windows
Desktop.ini            # Configuración de Windows
$RECYCLE.BIN/          # Papelera de Windows
```

### IDEs y editores
```
.vscode/               # Visual Studio Code (excepto algunas configuraciones)
.idea/                 # PyCharm/IntelliJ
*.swp, *.swo          # Vim
.#*, \#*#             # Emacs
```

### Logs y temporales
```
*.log                  # Archivos de log
*.tmp                  # Archivos temporales
*.backup               # Respaldos
*.bak                  # Respaldos alternativos
```

### Archivos de seguridad
```
*.pem, *.key          # Certificados y claves
*.crt, *.cer          # Certificados
.env                  # Variables de entorno
config.local.json     # Configuraciones locales
```

## 🔧 ¿Por qué estos archivos están ignorados?

### Entornos virtuales
- **Tamaño**: Pueden ser de 100+ MB
- **Específicos del sistema**: No funcionan entre diferentes máquinas
- **Recreables**: Se pueden regenerar con `pip install -r requirements.txt`

### Archivos de compilación
- **Tamaño**: Los ejecutables pueden ser de 50-100+ MB
- **Específicos de plataforma**: Un .exe no funciona en Linux
- **Regenerables**: Se pueden compilar desde el código fuente

### Cache y temporales
- **Innecesarios**: Se regeneran automáticamente
- **Específicos de máquina**: Contienen rutas absolutas
- **Pueden causar conflictos**: Entre diferentes versiones de Python

## 💡 Buenas prácticas

### ✅ Hacer
- Subir solo código fuente y documentación
- Incluir `requirements.txt` actualizado
- Documentar dependencias del sistema en README
- Usar releases de GitHub para distribuir ejecutables

### ❌ No hacer
- Subir entornos virtuales o cache
- Incluir ejecutables en el repo (usar releases)
- Subir configuraciones personales o claves
- Ignorar archivos de documentación

## 🚀 Distribución

### Para desarrolladores
- Clonar el repositorio
- Ejecutar `setup.bat` (Windows) o crear venv manualmente
- Desarrollar y compilar localmente

### Para usuarios finales
- Descargar ejecutables desde GitHub Releases
- O seguir instrucciones de instalación en README
- No necesitan clonar el repositorio completo