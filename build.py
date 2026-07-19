#!/usr/bin/env python3
"""
Script para compilar la aplicación ConsultaHacienda como un ejecutable único
"""
import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path

# Qt plugins to remove before building to reduce binary size
# These are not used by the app and some pull in heavy system libraries
# (e.g., GTK3 theme pulls in libgtk-3 + libicudata.so ~40MB)
_UNNECESSARY_QT_PLUGINS = [
    "platformthemes/libqgtk3.so",
    "platforms/libqeglfs.so",
    "platforms/libqminimalegl.so",
    "platforms/libqlinuxfb.so",
    "platforms/libqoffscreen.so",
    "platforms/libqvnc.so",
    "platforms/libqminimal.so",
    "platforminputcontexts/libqtvirtualkeyboardplugin.so",
    "networkinformation/libqconnman.so",
    "networkinformation/libqglib.so",
    "networkinformation/libqnetworkmanager.so",
]
_UNNECESSARY_QT_DIRS = [
    "egldeviceintegrations",
]


def _strip_unused_plugins(venv_dir: Path) -> list[Path]:
    """Remove unnecessary Qt plugins before building. Returns list of removed files."""
    qt_plugins = venv_dir / "lib" / "site-packages" / "PySide6" / "Qt" / "plugins"
    if not qt_plugins.exists():
        # Try alternative path for different Python versions
        for p in venv_dir.glob("lib/python*/site-packages/PySide6/Qt/plugins"):
            qt_plugins = p
            break
        else:
            return []

    removed = []
    for plugin_rel in _UNNECESSARY_QT_PLUGINS:
        plugin_path = qt_plugins / plugin_rel
        if plugin_path.exists():
            plugin_path.unlink()
            removed.append(plugin_path)

    for dir_name in _UNNECESSARY_QT_DIRS:
        dir_path = qt_plugins / dir_name
        if dir_path.exists():
            shutil.rmtree(dir_path)
            removed.append(dir_path)

    return removed


def main():
    """Función principal para compilar la aplicación"""
    
    # Directorio actual
    current_dir = Path(__file__).parent
    main_script = current_dir / "main.py"
    venv_dir = current_dir / "venv"
    
    if not main_script.exists():
        print("❌ Error: No se encontró el archivo main.py")
        return False
    
    if not venv_dir.exists():
        print("❌ Error: No se encontró el entorno virtual. Ejecuta: python3 -m venv venv")
        return False
    
    print("🔧 Compilando aplicación ConsultaHacienda...")
    print(f"💻 Sistema operativo detectado: {platform.system()}")
    print("-" * 50)
    
    # Strip unnecessary Qt plugins to reduce binary size
    removed = _strip_unused_plugins(venv_dir)
    if removed:
        print(f"🧹 Plugins innecesarios eliminados: {len(removed)}")
    
    # Configuración específica por SO
    is_windows = platform.system() == "Windows"
    separator = ";" if is_windows else ":"
    
    # Excluir módulos Qt que la app no usa (reducen ~40-50MB)
    exclude_modules = [
        "PySide6.QtQml",
        "PySide6.QtQuick",
        "PySide6.QtPdf",
        "PySide6.QtWebEngine",
        "PySide6.QtWebEngineCore",
        "PySide6.QtWebEngineWidgets",
        "PySide6.QtVirtualKeyboard",
        "PySide6.QtMultimedia",
        "PySide6.Qt3D",
        "PySide6.QtQuick3D",
        "PySide6.QtDesigner",
        "PySide6.QtOpenGL",
        "PySide6.QtSvg",
        "PySide6.QtHelp",
    ]
    exclude_flags = []
    for mod in exclude_modules:
        exclude_flags.extend(["--exclude-module", mod])

    # Comando de PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",                    # Crear un solo archivo ejecutable
        "--windowed",                   # No mostrar consola
        "--name=ConsultaHacienda",      # Nombre del ejecutable
        f"--add-data=requirements.txt{separator}.", # Incluir requirements
        "--hidden-import=requests",     # Asegurar que requests se incluya
        "--hidden-import=PySide6.QtCore",      # Asegurar que PySide6 se incluya
        "--hidden-import=PySide6.QtWidgets",   # Widgets de PySide6
        "--hidden-import=PySide6.QtGui",       # GUI de PySide6
        "--clean",                      # Limpiar cache antes de compilar
    ] + exclude_flags + [
        str(main_script)
    ]
    
    # Agregar icono si existe (específico para Windows)
    icon_file = current_dir / "icon.ico"
    if icon_file.exists():
        cmd.insert(-1, f"--icon={icon_file}")
    
    # En Windows, agregar opciones adicionales para evitar problemas
    if is_windows:
        cmd.append("--noconfirm")
    
    try:
        # Ejecutar PyInstaller
        print("⏳ Ejecutando PyInstaller...")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print("✅ Compilación exitosa!")
        
        # Buscar el ejecutable generado
        dist_dir = current_dir / "dist"
        if dist_dir.exists():
            # Buscar el ejecutable con extensión correcta según el SO
            exe_pattern = "ConsultaHacienda.exe" if is_windows else "ConsultaHacienda"
            executables = list(dist_dir.glob(exe_pattern))
            if not executables:
                # Buscar cualquier archivo con el nombre base
                executables = list(dist_dir.glob("ConsultaHacienda*"))
            
            if executables:
                exe_path = executables[0]
                print(f"📦 Ejecutable generado: {exe_path}")
                print(f"📁 Tamaño: {exe_path.stat().st_size / (1024*1024):.1f} MB")
                print(f"🖥️  Compatible con: {platform.system()}")
                
                # Crear directorio de release si no existe
                release_dir = current_dir / "release"
                release_dir.mkdir(exist_ok=True)
                
                # Copiar ejecutable a directorio release
                release_exe = release_dir / exe_path.name
                shutil.copy2(exe_path, release_exe)
                print(f"📋 Copiado a: {release_exe}")
                
                # Crear script de ejecución adicional en release
                if is_windows:
                    run_script = release_dir / "Ejecutar_ConsultaHacienda.bat"
                    run_script.write_text(f"@echo off\n{exe_path.name}\npause")
                    print(f"📝 Script creado: {run_script}")
                
                return True
        
        print("⚠️  Advertencia: No se encontró el ejecutable en dist/")
        return False
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error durante la compilación:")
        print(f"Código de salida: {e.returncode}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False
    
    except FileNotFoundError:
        print("❌ Error: PyInstaller no está instalado.")
        print("💡 Instala PyInstaller con: pip install pyinstaller")
        return False


def clean():
    """Limpiar archivos temporales de compilación"""
    current_dir = Path(__file__).parent
    
    dirs_to_clean = ["build", "dist", "__pycache__"]
    files_to_clean = ["*.spec"]
    
    print("🧹 Limpiando archivos temporales...")
    
    for dir_name in dirs_to_clean:
        dir_path = current_dir / dir_name
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"🗑️  Eliminado: {dir_path}")
    
    for file_pattern in files_to_clean:
        for file_path in current_dir.glob(file_pattern):
            file_path.unlink()
            print(f"🗑️  Eliminado: {file_path}")
    
    print("✅ Limpieza completada")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "clean":
        clean()
    else:
        success = main()
        
        if success:
            print("\n🎉 ¡Aplicación compilada exitosamente!")
            print("💡 Puedes encontrar el ejecutable en la carpeta 'release'")
            print("🔧 Para limpiar archivos temporales: python build.py clean")
        else:
            print("\n💥 La compilación falló. Revisa los errores arriba.")
            sys.exit(1)