# 🪟 Instrucciones para Windows

## Configuración inicial (Solo una vez)

### Opción 1: Automática (Recomendada)
1. **Abrir terminal** (CMD o PowerShell)
2. **Navegar** a la carpeta del proyecto
3. **Ejecutar**:
   ```cmd
   setup.bat
   ```
   
   O con PowerShell:
   ```powershell
   .\setup.ps1
   ```

### Opción 2: Manual
1. **Crear entorno virtual**:
   ```cmd
   python -m venv venv
   ```
2. **Activar entorno**:
   ```cmd
   venv\Scripts\activate
   ```
3. **Instalar dependencias**:
   ```cmd
   pip install -r requirements.txt
   ```

## Uso diario

### Ejecutar la aplicación
```cmd
run.bat
```

O con PowerShell:
```powershell
.\run.ps1
```

### Compilar ejecutable
```cmd
compile.bat
```

El ejecutable se generará en la carpeta `release\ConsultaHacienda.exe`

## Solución de problemas

### 🚨 Script de diagnóstico
Si tienes problemas, ejecuta primero:
```cmd
diagnostico.bat
```
Este script te mostrará información detallada del sistema y sugerencias.

### Error: "python no se reconoce"
- **Instalar Python** desde [python.org](https://python.org)
- **Marcar la casilla** "Add Python to PATH" durante la instalación
- **Versiones recomendadas**: Python 3.9, 3.10, 3.11, o 3.12
- **Evitar**: Python 3.13+ (muy nuevo) o 3.7- (muy antiguo)

### Error: "Se ignoraron versiones que requerían una versión diferente de Python"
Este es el problema más común. **Soluciones**:

1. **Verificar versión de Python**:
   ```cmd
   python --version
   ```

2. **Si tienes Python 3.8**: Usar requirements alternativos:
   ```cmd
   pip install -r requirements-alt.txt
   ```

3. **Actualizar herramientas de construcción**:
   ```cmd
   python -m pip install --upgrade pip setuptools wheel
   ```

4. **Instalar dependencias individualmente**:
   ```cmd
   pip install PySide6==6.7.2
   pip install requests>=2.31.0
   pip install pyinstaller>=5.13.0
   ```

### Error de permisos en PowerShell
Ejecutar una vez como administrador:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### PySide6 no se instala
**Causas comunes**:
- Python muy antiguo (< 3.8) o muy nuevo (> 3.12)
- Falta Visual C++ Redistributable
- pip desactualizado

**Soluciones**:
1. **Actualizar pip**:
   ```cmd
   python -m pip install --upgrade pip
   ```

2. **Instalar Visual C++ Redistributable** desde Microsoft

3. **Usar versión específica**:
   ```cmd
   pip install PySide6==6.7.2
   ```

### El entorno virtual no se activa
1. **Eliminar y recrear**:
   ```cmd
   rmdir /s venv
   setup.bat
   ```

2. **Verificar permisos** de la carpeta del proyecto

### El ejecutable no funciona
- **Verificar antivirus**: Algunos antivirus bloquean ejecutables de PyInstaller
- **Agregar excepción** para la carpeta del proyecto
- **Usar Windows Defender** en lugar de antivirus de terceros si es posible
- **Ejecutar como administrador** si es necesario

### Problemas de interfaz gráfica
- **Actualizar drivers gráficos**
- **Instalar Visual C++ Redistributable** desde Microsoft
- **Verificar que tengas Windows 10/11** (recomendado)

### Error: "No module named 'PySide6'"
1. **Verificar que el entorno esté activado**:
   ```cmd
   venv\Scripts\activate
   ```

2. **Reinstalar en el entorno correcto**:
   ```cmd
   venv\Scripts\pip.exe install PySide6
   ```

### Problemas de red durante instalación
1. **Usar proxy si es necesario**:
   ```cmd
   pip install --proxy http://proxy:puerto PySide6
   ```

2. **Usar mirror alternativo**:
   ```cmd
   pip install -i https://pypi.douban.com/simple/ PySide6
   ```

3. **Descargar wheels manualmente** desde PyPI

## Ventajas en Windows

- ✅ **Interfaz nativa**: Se integra perfectamente con el tema de Windows
- ✅ **Un solo archivo**: El ejecutable compilado no requiere instalación
- ✅ **Compatibilidad**: Funciona desde Windows 7 en adelante
- ✅ **Sin dependencias**: El ejecutable incluye todo lo necesario

## Archivos importantes para Windows

- `setup.bat` / `setup.ps1` - Configuración inicial
- `run.bat` / `run.ps1` - Ejecutar aplicación  
- `compile.bat` / `compile.ps1` - Compilar ejecutable
- `release\ConsultaHacienda.exe` - Ejecutable compilado
- `release\Ejecutar_ConsultaHacienda.bat` - Atajo para ejecutar