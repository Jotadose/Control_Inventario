from inventory import Producto, GestorInventario
from prediction import PrediccionDemanda
from returns import GestionDevoluciones
from suppliers import IntegracionProveedores
from utils import input_int

def main():
    gestor_inventario = GestorInventario()
    prediccion_demanda = PrediccionDemanda()
    gestion_devoluciones = GestionDevoluciones()
    integracion_proveedores = IntegracionProveedores()

    while True:
        print("\nSeleccione una opción:")
        print("1. Agregar Producto")
        print("2. Actualizar Stock")
        print("3. Mostrar Inventario")
        print("4. Predecir Demanda")
        print("5. Procesar Devolución")
        print("6. Registrar Proveedor")
        print("7. Solicitar Reabastecimiento")
        print("8. Salir")
        opcion = input()

        if opcion == "1":
            id = input_int("Ingrese el ID del producto: ")
            nombre = input("Ingrese el nombre del producto: ")
            cantidad = input_int("Ingrese la cantidad del producto: ")
            precio = float(input("Ingrese el precio del producto: "))
            producto = Producto(id, nombre, cantidad, precio)
            gestor_inventario.agregar_producto(producto)
        elif opcion == "2":
            id = input_int("Ingrese el ID del producto: ")
            nueva_cantidad = input_int("Ingrese la nueva cantidad: ")
            gestor_inventario.actualizar_stock(id, nueva_cantidad)
        elif opcion == "3":
            gestor_inventario.mostrar_inventario()
        elif opcion == "4":
            datos = [input_int(f"Ingrese las ventas para el día {i+1}: ") for i in range(7)]
            demanda = prediccion_demanda.predecir(datos)
            print(f"Demanda Predicha: {demanda}")
        elif opcion == "5":
            producto_id = input_int("Ingrese el ID del producto a devolver: ")
            cantidad = input_int("Ingrese la cantidad a devolver: ")
            gestion_devoluciones.procesar_devolucion(producto_id, cantidad)
        elif opcion == "6":
            id_proveedor = input_int("Ingrese el ID del proveedor: ")
            nombre = input("Ingrese el nombre del proveedor: ")
            api_url = input("Ingrese el URL de la API del proveedor: ")
            integracion_proveedores.registrar_proveedor(id_proveedor, nombre, api_url)
        elif opcion == "7":
            id_proveedor = input_int("Ingrese el ID del proveedor: ")
            producto_id = input_int("Ingrese el ID del producto: ")
            cantidad = input_int("Ingrese la cantidad a solicitar: ")
            integracion_proveedores.solicitar_reabastecimiento(id_proveedor, producto_id, cantidad)
        elif opcion == "8":
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
