import sqlite3

class GestionDevoluciones:
    def __init__(self, db_name="devoluciones.db"):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS devoluciones 
                            (producto_id INTEGER, cantidad INTEGER)''')
        self.conn.commit()

    def procesar_devolucion(self, producto_id, cantidad):
        self.cur.execute("INSERT INTO devoluciones (producto_id, cantidad) VALUES (?, ?)", (producto_id, cantidad))
        self.conn.commit()
        print(f"Devolución procesada para Producto ID: {producto_id}, Cantidad: {cantidad}")
