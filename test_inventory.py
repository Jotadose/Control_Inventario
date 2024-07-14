import unittest
from inventory import Producto, GestorInventario

class TestGestorInventario(unittest.TestCase):
    def setUp(self):
        self.gestor = GestorInventario()
        self.producto1 = Producto(1, "Producto1", 10, 100.0)
        self.producto2 = Producto(2, "Producto2", 20, 200.0)

    def test_agregar_producto(self):
        # Test para verificar que se puede agregar un producto correctamente
        resultado = self.gestor.agregar_producto(self.producto1)
        self.assertTrue(resultado)
        self.assertEqual(len(self.gestor.inventario), 1)

        # Test para verificar que no se pueden agregar productos duplicados
        resultado = self.gestor.agregar_producto(self.producto1)
        self.assertFalse(resultado)
        self.assertEqual(len(self.gestor.inventario), 1)

    def test_actualizar_stock(self):
        # Agregar un producto y luego actualizar su stock
        self.gestor.agregar_producto(self.producto1)
        resultado = self.gestor.actualizar_stock(1, 15)
        self.assertTrue(resultado)
        self.assertEqual(self.gestor.inventario[0].cantidad, 15)

        # Intentar actualizar un producto que no existe
        resultado = self.gestor.actualizar_stock(3, 30)
        self.assertFalse(resultado)

    def test_mostrar_inventario(self):
        # Verificar que mostrar_inventario devuelve la lista correcta
        self.gestor.agregar_producto(self.producto1)
        self.gestor.agregar_producto(self.producto2)
        inventario = self.gestor.mostrar_inventario()
        self.assertEqual(len(inventario), 2)
        self.assertEqual(inventario[0]['id'], 1)
        self.assertEqual(inventario[1]['id'], 2)

    def test_eliminar_producto(self):
        # Agregar productos y luego intentar eliminar uno
        self.gestor.agregar_producto(self.producto1)
        self.gestor.agregar_producto(self.producto2)
        resultado = self.gestor.eliminar_producto(1)
        self.assertTrue(resultado)
        self.assertEqual(len(self.gestor.inventario), 1)

        # Intentar eliminar un producto que no existe
        resultado = self.gestor.eliminar_producto(3)
        self.assertFalse(resultado)

if __name__ == '__main__':
    unittest.main()
