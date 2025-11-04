import sys
import json
import requests
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                               QWidget, QLabel, QLineEdit, QPushButton, QTextEdit,
                               QMessageBox, QProgressBar)
from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtGui import QFont, QIcon


class ApiWorker(QThread):
    """Worker thread para realizar la consulta a la API sin bloquear la interfaz"""
    finished = Signal(dict)
    error = Signal(str)
    
    def __init__(self, identificacion):
        super().__init__()
        self.identificacion = identificacion
    
    def run(self):
        try:
            url = f"https://api.hacienda.go.cr/fe/ae?identificacion={self.identificacion}"
            
            # Headers adicionales para evitar bloqueos de antivirus
            headers = {
                'User-Agent': 'ConsultaHacienda/1.0 (https://github.com/eriosgamer/ConsultaHacienda)',
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(url, timeout=15, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                self.finished.emit(data)
            else:
                self.error.emit(f"Error HTTP {response.status_code}: {response.text}")
                
        except requests.exceptions.Timeout:
            self.error.emit("Timeout: La consulta tardó demasiado. Verifica tu conexión a internet.")
        except requests.exceptions.ConnectionError as e:
            error_msg = "Error de conexión. Posibles causas:\n"
            error_msg += "• Sin conexión a internet\n"
            error_msg += "• API de Hacienda no disponible\n"
            error_msg += f"\nDetalle técnico: {str(e)}"
            self.error.emit(error_msg)
        except requests.exceptions.RequestException as e:
            self.error.emit(f"Error de conexión: {str(e)}")
        except json.JSONDecodeError as e:
            self.error.emit(f"Error al procesar respuesta: {str(e)}")
        except Exception as e:
            self.error.emit(f"Error inesperado: {str(e)}")


class ConsultaHaciendaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.init_ui()
        
    def init_ui(self):
        """Inicializar la interfaz de usuario"""
        self.setWindowTitle("Consulta Hacienda Costa Rica")
        self.setGeometry(100, 100, 600, 500)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        layout = QVBoxLayout(central_widget)
        
        # Título
        title_label = QLabel("Consulta de Información Tributaria")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Layout para entrada de datos
        input_layout = QHBoxLayout()
        
        # Campo de identificación
        id_label = QLabel("Identificación:")
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Ingrese el número de identificación")
        self.id_input.returnPressed.connect(self.consultar)
        
        # Botón de consulta
        self.consulta_btn = QPushButton("Consultar")
        self.consulta_btn.clicked.connect(self.consultar)
        
        input_layout.addWidget(id_label)
        input_layout.addWidget(self.id_input)
        input_layout.addWidget(self.consulta_btn)
        
        layout.addLayout(input_layout)
        
        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Área de resultados
        result_label = QLabel("Resultados:")
        result_label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(result_label)
        
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setFont(QFont("Courier", 10))
        layout.addWidget(self.result_text)
        
        # Botón para limpiar
        clear_btn = QPushButton("Limpiar")
        clear_btn.clicked.connect(self.limpiar)
        layout.addWidget(clear_btn)
        
    def consultar(self):
        """Realizar consulta a la API de Hacienda"""
        identificacion = self.id_input.text().strip()
        
        if not identificacion:
            QMessageBox.warning(self, "Advertencia", "Por favor ingrese un número de identificación.")
            return
            
        if not identificacion.isdigit():
            QMessageBox.warning(self, "Advertencia", "La identificación debe contener solo números.")
            return
        
        # Deshabilitar botón y mostrar progreso
        self.consulta_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Barra indeterminada
        
        # Crear y ejecutar worker thread
        self.worker = ApiWorker(identificacion)
        self.worker.finished.connect(self.mostrar_resultados)
        self.worker.error.connect(self.mostrar_error)
        self.worker.start()
    
    def mostrar_resultados(self, data):
        """Mostrar los resultados de la consulta"""
        try:
            # Procesar datos
            nombre = data.get('nombre', 'No disponible')
            situacion = data.get('situacion', {})
            estado = situacion.get('estado', 'No disponible')
            actividades = data.get('actividades', [])
            
            # Formatear resultado
            resultado = f"NOMBRE: {nombre}\n"
            resultado += f"ESTADO: {estado}\n\n"
            
            if actividades:
                resultado += "ACTIVIDADES:\n"
                resultado += "=" * 50 + "\n"
                for i, actividad in enumerate(actividades, 1):
                    codigo = actividad.get('codigo', 'Sin código')
                    descripcion = actividad.get('descripcion', 'Sin descripción')
                    estado_act = actividad.get('estado', 'N/A')
                    tipo = actividad.get('tipo', 'N/A')
                    
                    resultado += f"{i}. Código: {codigo}\n"
                    resultado += f"   Descripción: {descripcion}\n"
                    resultado += f"   Estado: {estado_act} | Tipo: {tipo}\n\n"
            else:
                resultado += "ACTIVIDADES: Sin actividad\n"
            
            # Agregar información adicional
            if 'regimen' in data:
                regimen = data['regimen']
                resultado += f"\nRÉGIMEN: {regimen.get('descripcion', 'No disponible')}\n"
            
            if situacion:
                resultado += f"\nSITUACIÓN TRIBUTARIA:\n"
                resultado += f"- Moroso: {situacion.get('moroso', 'No disponible')}\n"
                resultado += f"- Omiso: {situacion.get('omiso', 'No disponible')}\n"
                resultado += f"- Administración: {situacion.get('administracionTributaria', 'No disponible')}\n"
            
            self.result_text.setPlainText(resultado)
            
        except Exception as e:
            self.mostrar_error(f"Error al procesar datos: {str(e)}")
        
        finally:
            self.finalizar_consulta()
    
    def mostrar_error(self, error_msg):
        """Mostrar mensaje de error"""
        self.result_text.setPlainText(f"ERROR: {error_msg}")
        QMessageBox.critical(self, "Error", error_msg)
        self.finalizar_consulta()
    
    def finalizar_consulta(self):
        """Restaurar estado de la interfaz después de la consulta"""
        self.consulta_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        if self.worker:
            self.worker.quit()
            self.worker.wait()
    
    def limpiar(self):
        """Limpiar los campos de entrada y resultado"""
        self.id_input.clear()
        self.result_text.clear()
        self.id_input.setFocus()


def main():
    app = QApplication(sys.argv)
    
    # Configurar aplicación
    app.setApplicationName("Consulta Hacienda CR")
    app.setApplicationVersion("1.0")
    
    # Crear y mostrar ventana principal
    window = ConsultaHaciendaApp()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()