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
    
    # Configuración específica por SO
    is_windows = platform.system() == "Windows"
    separator = ";" if is_windows else ":"
    
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
        str(main_script)
    ]
    
    # Agregar icono si existe (específico para Windows)
    icon_file = current_dir / "icon.ico"
    if icon_file.exists():
        cmd.insert(-1, f"--icon={icon_file}")
    
    # En Windows, agregar opciones adicionales para evitar problemas
    if is_windows:
        cmd.extend([
            "--collect-all=PySide6",
            "--noconfirm"
        ])
    
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