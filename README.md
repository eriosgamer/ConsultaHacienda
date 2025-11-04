# ConsultaHacienda - Aplicación de Consulta Tributaria

Una aplicación de escritorio desarrollada con PySide6 para consultar información tributaria de Costa Rica a través de la API de Hacienda.

## Características

- **Interfaz gráfica moderna**: Desarrollada con PySide6/Qt6
- **Consultas asíncronas**: No bloquea la interfaz durante las consultas
- **Manejo de errores**: Validación de entrada y manejo robusto de errores
- **Compilación a ejecutable**: Se puede compilar como un archivo único ejecutable
- **Información completa**: Muestra nombre, estado tributario y actividades económicas

## Información mostrada

La aplicación consulta y muestra:

- **Nombre** del contribuyente
- **Estado tributario** (Inscrito, etc.)
- **Actividades económicas**:
  - Código de actividad
  - Descripción
  - Estado (Activo/Inactivo)
  - Tipo (Principal/Secundaria)
- **Régimen tributario**
- **Situación tributaria** (moroso, omiso, administración)

## Instalación y uso

### Opción 1: Ejecutar desde código fuente

#### En Windows:
1. **Clonar o descargar** el proyecto
2. **Ejecutar setup**:
   ```cmd
   setup.bat
   ```
   O con PowerShell:
   ```powershell
   .\setup.ps1
   ```
3. **Ejecutar la aplicación**:
   ```cmd
   run.bat
   ```

#### En Linux/macOS:
1. **Clonar o descargar** el proyecto
2. **Ejecutar setup**:
   ```bash
   ./setup.sh
   ```
3. **Ejecutar la aplicación**:
   ```bash
   ./run.sh
   ```

### Opción 2: Compilar ejecutable

#### En Windows:
1. **Ejecutar setup** (si no lo has hecho):
   ```cmd
   setup.bat
   ```
2. **Compilar**:
   ```cmd
   compile.bat
   ```
   O con PowerShell:
   ```powershell
   .\compile.ps1
   ```
3. **Encontrar el ejecutable** `ConsultaHacienda.exe` en la carpeta `release/`

#### En Linux/macOS:
1. **Configurar entorno**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Compilar**:
   ```bash
   ./compile.sh
   ```
3. **Encontrar el ejecutable** en la carpeta `release/`

### Opción 3: Usar ejecutable precompilado

Si tienes acceso al ejecutable precompilado, simplemente:
1. Descarga `ConsultaHacienda` (o `ConsultaHacienda.exe` en Windows)
2. Ejecuta el archivo directamente

## Uso de la aplicación

1. **Abrir la aplicación**
2. **Ingresar número de identificación** en el campo correspondiente
3. **Hacer clic en "Consultar"** o presionar Enter
4. **Ver los resultados** en el área de texto
5. **Usar "Limpiar"** para borrar los datos y hacer una nueva consulta

## Estructura del proyecto

```
ConsultaHacienda/
├── main.py              # Aplicación principal
├── requirements.txt     # Dependencias
├── build.py            # Script de compilación
├── README.md           # Documentación
├── .github/workflows/  # GitHub Actions para CI/CD
│
├── Scripts Linux/macOS:
├── setup.sh            # Configuración inicial
├── run.sh              # Ejecutar aplicación
├── compile.sh          # Compilar aplicación
│
└── Scripts Windows:
    ├── setup.bat       # Configuración inicial
    ├── run.bat         # Ejecutar aplicación
    ├── compile.bat     # Compilar aplicación
    ├── setup.ps1       # Configuración PowerShell
    ├── run.ps1         # Ejecutar con PowerShell
    └── compile.ps1     # Compilar con PowerShell
```

## Dependencias

- **PySide6**: Framework de interfaz gráfica
- **requests**: Para realizar consultas HTTP a la API
- **PyInstaller**: Para compilar a ejecutable (solo para desarrollo)

## API utilizada

La aplicación utiliza la API pública de Hacienda de Costa Rica:
```
https://api.hacienda.go.cr/fe/ae?identificacion={numero}
```

## Mantenimiento

Para limpiar archivos temporales de compilación:
```bash
python build.py clean
```

## Notas técnicas

- La aplicación maneja consultas en un hilo separado para no bloquear la interfaz
- Incluye validación de entrada (solo números)
- Manejo robusto de errores de red y de formato
- Timeout de 10 segundos para las consultas HTTP
- Compatible con Windows, macOS y Linux

## Notas importantes

- **Requiere Python 3.8-3.12** (Python 3.13+ aún no es compatible con PySide6)
- **Conexión a internet** necesaria para consultar la API
- **API oficial** del Ministerio de Hacienda de Costa Rica