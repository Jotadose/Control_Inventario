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
        """Agrega un nuevo producto al inventario si no existe ya."""
        if any(p.id == producto.id for p in self.inventario):
            return False
        self.inventario.append(producto)
        return True

    def actualizar_producto(self, id, nuevo_nombre, nueva_cantidad, nuevo_precio):
        """Actualiza la información de un producto existente."""
        for producto in self.inventario:
            if producto.id == id:
                producto.nombre = nuevo_nombre
                producto.cantidad = nueva_cantidad
                producto.precio = nuevo_precio
                return True
        return False

    def mostrar_inventario(self):
        """Devuelve una lista con la información de todos los productos en el inventario."""
        return [{'id': p.id, 'nombre': p.nombre, 'cantidad': p.cantidad, 'precio': p.precio} for p in self.inventario]

    def eliminar_producto(self, id):
        """Elimina un producto del inventario según su ID."""
        print(f"Intentando eliminar ID: {id}")
        original_length = len(self.inventario)
        self.inventario = [producto for producto in self.inventario if producto.id != id]
        if len(self.inventario) < original_length:
            print("Producto eliminado")
            return True
        else:
            print("Producto no encontrado")
            return False
