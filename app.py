from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'inventory.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Producto {self.nombre}>'

class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    fecha_venta = db.Column(db.Date, nullable=False)
    producto = db.relationship('Producto', backref='ventas')

class Proveedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    contacto = db.Column(db.String(200), nullable=False)

class OrdenAbastecimiento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    fecha_orden = db.Column(db.Date, nullable=False)
    producto = db.relationship('Producto', backref='ordenes_abastecimiento')

@app.before_request
def create_tables():
    """Create database tables if they don't exist."""
    if not hasattr(app, 'tables_created'):
        db.create_all()
        app.tables_created = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inicio')
def inicio():
    return render_template('index.html')

@app.route('/inventario')
def inventario():
    return render_template('inventario.html')

@app.route('/ventas')
def ventas():
    return render_template('ventas.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    """Add a new product to the inventory."""
    data = request.json
    nuevo_producto = Producto(
        id=data['id'], 
        nombre=data['nombre'], 
        cantidad=data['cantidad'], 
        precio=data['precio']
    )
    db.session.add(nuevo_producto)
    try:
        db.session.commit()
        return jsonify({'message': 'Producto agregado'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/actualizar_producto', methods=['POST'])
def actualizar_producto():
    """Update product details."""
    data = request.json
    producto = Producto.query.get(data['id'])
    if producto:
        producto.nombre = data['nuevo_nombre']
        producto.cantidad = data['nueva_cantidad']
        producto.precio = data['nuevo_precio']
        try:
            db.session.commit()
            return jsonify({'message': 'Producto actualizado'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    return jsonify({'error': 'Producto no encontrado'}), 404

@app.route('/mostrar_inventario', methods=['GET'])
def mostrar_inventario():
    """Show all products in the inventory."""
    productos = Producto.query.all()
    inventario = [{'id': p.id, 'nombre': p.nombre, 'cantidad': p.cantidad, 'precio': p.precio} for p in productos]
    return jsonify({'inventario': inventario})

@app.route('/eliminar_producto', methods=['POST'])
def eliminar_producto():
    """Delete a product from the inventory."""
    data = request.json
    producto = Producto.query.get(data['id'])
    if producto:
        db.session.delete(producto)
        try:
            db.session.commit()
            return jsonify({'message': 'Producto eliminado con éxito'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    return jsonify({'error': 'Producto no encontrado'}), 404

@app.route('/vender_producto', methods=['POST'])
def vender_producto():
    """Sell a product and update the inventory."""
    data = request.json
    id_producto = int(data['id_producto'])
    cantidad_vendida = int(data['cantidad_vendida'])
    
    producto = Producto.query.get(id_producto)
    if producto and producto.cantidad >= cantidad_vendida:
        producto.cantidad -= cantidad_vendida
        nueva_venta = Venta(producto_id=id_producto, cantidad=cantidad_vendida, fecha_venta=datetime.utcnow().date())
        db.session.add(nueva_venta)
        try:
            db.session.commit()
            return jsonify({'message': 'Venta procesada correctamente'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    elif producto and producto.cantidad < cantidad_vendida:
        return jsonify({'error': 'No hay suficiente stock para la venta'}), 400
    else:
        return jsonify({'error': 'Producto no encontrado'}), 404

@app.route('/proveedores', methods=['GET', 'POST'])
def manage_proveedores():
    if request.method == 'POST':
        data = request.json
        nuevo_proveedor = Proveedor(nombre=data['nombre'], contacto=data['contacto'])
        db.session.add(nuevo_proveedor)
        try:
            db.session.commit()
            return jsonify({'message': 'Proveedor agregado'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    proveedores = Proveedor.query.all()
    return jsonify([{'id': p.id, 'nombre': p.nombre, 'contacto': p.contacto} for p in proveedores]), 200

@app.route('/abastecimientos', methods=['GET', 'POST'])
def manage_abastecimientos():
    if request.method == 'POST':
        data = request.json
        nueva_orden = OrdenAbastecimiento(producto_id=data['producto_id'], cantidad=data['cantidad'], fecha_orden=datetime.strptime(data['fecha_orden'], '%Y-%m-%d').date())
        db.session.add(nueva_orden)
        try:
            db.session.commit()
            return jsonify({'message': 'Orden de abastecimiento agregada'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    abastecimientos = OrdenAbastecimiento.query.all()
    return jsonify([{'id': o.id, 'producto': o.producto.nombre, 'cantidad': o.cantidad, 'fecha_orden': o.fecha_orden} for o in abastecimientos]), 200

@app.route('/log_ventas', methods=['GET'])
def log_ventas():
    ventas = Venta.query.all()
    return jsonify([{'id': v.id, 'producto': v.producto.nombre, 'cantidad': v.cantidad, 'fecha_venta': v.fecha_venta} for v in ventas]), 200

if __name__ == "__main__":
    app.run(debug=True)
