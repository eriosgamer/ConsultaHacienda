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

### Error: "python no se reconoce"
- **Instalar Python** desde [python.org](https://python.org)
- **Marcar la casilla** "Add Python to PATH" durante la instalación

### Error de permisos en PowerShell
Ejecutar una vez:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### El ejecutable no funciona
- **Verificar antivirus**: Algunos antivirus bloquean ejecutables de PyInstaller
- **Agregar excepción** para la carpeta del proyecto
- **Usar Windows Defender** en lugar de antivirus de terceros si es posible

### Problemas de interfaz gráfica
- **Actualizar drivers gráficos**
- **Instalar Visual C++ Redistributable** desde Microsoft

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