import sys
import json
import requests
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QMessageBox,
    QProgressBar,
)
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
            url = (
                f"https://api.hacienda.go.cr/fe/ae?identificacion={self.identificacion}"
            )

            # Headers adicionales para evitar bloqueos de antivirus
            headers = {
                "User-Agent": "ConsultaHacienda/1.0 (https://github.com/eriosgamer/ConsultaHacienda)",
                "Accept": "application/json",
                "Content-Type": "application/json",
            }

            response = requests.get(url, timeout=15, headers=headers)

            if response.status_code == 200:
                data = response.json()
                self.finished.emit(data)
            elif response.status_code == 404:
                self.error.emit(
                    "La identificación consultada no existe en la base de datos de Hacienda."
                )
            else:
                self.error.emit(f"Error HTTP {response.status_code}: {response.text}")

        except requests.exceptions.Timeout:
            self.error.emit(
                "Timeout: La consulta tardó demasiado. Verifica tu conexión a internet."
            )
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
            QMessageBox.warning(
                self, "Advertencia", "Por favor ingrese un número de identificación."
            )
            return

        if not identificacion.isdigit():
            QMessageBox.warning(
                self, "Advertencia", "La identificación debe contener solo números."
            )
            return

        # Validar longitud típica de cédula costarricense (9, 10, 11 o 12 dígitos)
        if len(identificacion) not in (9, 10, 11, 12):
            QMessageBox.warning(
                self,
                "Advertencia",
                "La identificación debe tener Entre 9 y 12 dígitos.",
            )
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
        estado_map = {"A": "Activo", "I": "Inactivo"}
        tipo_map = {"P": "Primaria", "S": "Secundaria"}
        try:
            nombre = data.get("nombre", "No disponible")
            situacion = data.get("situacion", {})
            estado = situacion.get("estado", "No disponible")
            actividades = data.get("actividades", [])

            # Detectar tema oscuro/claro
            palette = QApplication.instance().palette()
            from PySide6.QtGui import QPalette
            bg = palette.color(QPalette.ColorRole.Window)
            bg_color = bg.red() + bg.green() + bg.blue()
            is_dark = bg_color < 384  # 128*3

            if is_dark:
                # Colores claros para fondo oscuro
                style = """<style>
.titulo { font-size: 18px; font-weight: bold; color: #fff; }
.dato { font-size: 15px; font-weight: bold; color: #e0e0e0; }
.valor { font-size: 15px; color: #7fffd4; }
.seccion { margin-top: 18px; font-size: 14px; font-weight: bold; color: #00bfff; }
.actividad { background: #222; border-radius: 6px; padding: 8px; margin-bottom: 8px; color: #e0e0e0; }
.label { font-weight: bold; color: #b0b0b0; }
.extra { color: #ffb6c1; font-size: 13px; }
</style>"""
            else:
                # Colores oscuros para fondo claro
                style = """<style>
.titulo { font-size: 18px; font-weight: bold; color: #2c3e50; }
.dato { font-size: 15px; font-weight: bold; color: #34495e; }
.valor { font-size: 15px; color: #16a085; }
.seccion { margin-top: 18px; font-size: 14px; font-weight: bold; color: #2980b9; }
.actividad { background: #f4f8fb; border-radius: 6px; padding: 8px; margin-bottom: 8px; }
.label { font-weight: bold; color: #7f8c8d; }
.extra { color: #8e44ad; font-size: 13px; }
</style>"""

            html = style
            html += f'<div class="titulo">Información General</div>'
            html += (
                f'<div class="dato">Nombre: <span class="valor">{nombre}</span></div>'
            )
            html += (
                f'<div class="dato">Estado: <span class="valor">{estado}</span></div>'
            )

            # Actividades
            html += '<div class="seccion">Actividades</div>'
            if actividades:
                for i, actividad in enumerate(actividades, 1):
                    codigo = actividad.get("codigo", "Sin código")
                    descripcion = actividad.get("descripcion", "Sin descripción")
                    estado_act = actividad.get("estado", "N/A")
                    tipo = actividad.get("tipo", "N/A")
                    estado_legible = estado_map.get(estado_act, estado_act)
                    tipo_legible = tipo_map.get(tipo, tipo)
                    html += f"""<div class="actividad">
<span class="label">{i}. Código:</span> {codigo}<br>
<span class="label">Descripción:</span> {descripcion}<br>
<span class="label">Estado:</span> <span class="valor">{estado_legible}</span> | <span class="label">Tipo:</span> <span class="valor">{tipo_legible}</span>
</div>"""
            else:
                html += '<div class="actividad">Sin actividad registrada</div>'

            # Régimen
            if "regimen" in data:
                regimen = data["regimen"]
                html += f'<div class="seccion">Régimen</div>'
                html += f'<div class="extra">{regimen.get('descripcion', 'No disponible')}</div>'

            # Situación tributaria
            if situacion:
                html += f'<div class="seccion">Situación Tributaria</div>'
                html += f'<div class="extra">Moroso: {situacion.get('moroso', 'No disponible')}<br>'
                html += f"Omiso: {situacion.get('omiso', 'No disponible')}<br>"
                html += f"Administración: {situacion.get('administracionTributaria', 'No disponible')}</div>"

            self.result_text.setHtml(html)

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
