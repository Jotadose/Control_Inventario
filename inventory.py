class Producto:
    def __init__(self, id, nombre, cantidad, precio):
        self.id = id
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

class GestorInventario:
    def __init__(self):
        self.inventario = []

    def agregar_producto(self, producto):
        self.inventario.append(producto)

    def actualizar_stock(self, id, nueva_cantidad):
        for producto in self.inventario:
            if producto.id == id:
                producto.cantidad = nueva_cantidad
                break

    def mostrar_inventario(self):
        return [{'id': p.id, 'nombre': p.nombre, 'cantidad': p.cantidad, 'precio': p.precio} for p in self.inventario]
