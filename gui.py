import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from inventory import GestorInventario
from inventory import Producto, GestorInventario


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Inventarios")
        self.gestor = GestorInventario()

        layout = QVBoxLayout()

        self.id_label = QLabel("ID del Producto")
        layout.addWidget(self.id_label)
        self.id_entry = QLineEdit()
        layout.addWidget(self.id_entry)

        self.nombre_label = QLabel("Nombre del Producto")
        layout.addWidget(self.nombre_label)
        self.nombre_entry = QLineEdit()
        layout.addWidget(self.nombre_entry)

        self.cantidad_label = QLabel("Cantidad del Producto")
        layout.addWidget(self.cantidad_label)
        self.cantidad_entry = QLineEdit()
        layout.addWidget(self.cantidad_entry)

        self.precio_label = QLabel("Precio del Producto")
        layout.addWidget(self.precio_label)
        self.precio_entry = QLineEdit()
        layout.addWidget(self.precio_entry)

        self.add_button = QPushButton("Agregar Producto")
        self.add_button.clicked.connect(self.agregar_producto)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def agregar_producto(self):
        id = int(self.id_entry.text())
        nombre = self.nombre_entry.text()
        cantidad = int(self.cantidad_entry.text())
        precio = float(self.precio_entry.text())
        producto = Producto(id, nombre, cantidad, precio)
        self.gestor.agregar_producto(producto)
        self.mostrar_mensaje("Producto agregado con éxito.")

    def mostrar_mensaje(self, mensaje):
        QMessageBox.information(self, "Información", mensaje)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
