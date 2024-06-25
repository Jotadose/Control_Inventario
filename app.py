from flask import Flask, request, render_template, jsonify
from inventory import Producto, GestorInventario
from prediction import PrediccionDemanda
from returns import GestionDevoluciones
from suppliers import IntegracionProveedores

app = Flask(__name__)

gestor_inventario = GestorInventario()
prediccion_demanda = PrediccionDemanda()
gestion_devoluciones = GestionDevoluciones()
integracion_proveedores = IntegracionProveedores()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    data = request.json
    producto = Producto(data['id'], data['nombre'], data['cantidad'], data['precio'])
    gestor_inventario.agregar_producto(producto)
    return jsonify({'message': 'Producto agregado'})

@app.route('/actualizar_stock', methods=['POST'])
def actualizar_stock():
    data = request.json
    gestor_inventario.actualizar_stock(data['id'], data['nueva_cantidad'])
    return jsonify({'message': 'Stock actualizado'})

@app.route('/mostrar_inventario', methods=['GET'])
def mostrar_inventario():
    inventario = gestor_inventario.mostrar_inventario()
    return jsonify({'inventario': inventario})

@app.route('/predecir_demanda', methods=['POST'])
def predecir_demanda():
    datos = request.json.get('datos')
    try:
        datos_x = list(range(1, len(datos) + 1))
        prediccion_demanda.entrenar(datos_x, datos)
        demanda = prediccion_demanda.predecir([len(datos) + 1])
        return jsonify({'demanda': demanda})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/procesar_devolucion', methods=['POST'])
def procesar_devolucion():
    data = request.json
    gestion_devoluciones.procesar_devolucion(data['producto_id'], data['cantidad'])
    return jsonify({'message': 'Devolución procesada'})

@app.route('/registrar_proveedor', methods=['POST'])
def registrar_proveedor():
    data = request.json
    integracion_proveedores.registrar_proveedor(data['id'], data['nombre'], data['api_url'])
    return jsonify({'message': 'Proveedor registrado'})

@app.route('/solicitar_reabastecimiento', methods=['POST'])
def solicitar_reabastecimiento():
    data = request.json
    integracion_proveedores.solicitar_reabastecimiento(data['id_proveedor'], data['producto_id'], data['cantidad'])
    return jsonify({'message': 'Reabastecimiento solicitado'})

if __name__ == "__main__":
    app.run(debug=True)
