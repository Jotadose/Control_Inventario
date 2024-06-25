import sqlite3
import requests

class IntegracionProveedores:
    def __init__(self, db_name="proveedores.db"):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS proveedores 
                            (id INTEGER PRIMARY KEY, nombre TEXT, api_url TEXT)''')
        self.conn.commit()

    def registrar_proveedor(self, id_proveedor, nombre, api_url):
        self.cur.execute("INSERT INTO proveedores (id, nombre, api_url) VALUES (?, ?, ?)",
                        (id_proveedor, nombre, api_url))
        self.conn.commit()
        print(f"Proveedor {nombre} registrado con éxito.")

    def solicitar_reabastecimiento(self, id_proveedor, producto_id, cantidad):
        self.cur.execute("SELECT api_url FROM proveedores WHERE id = ?", (id_proveedor,))
        result = self.cur.fetchone()
        if result:
            api_url = result[0]
            response = requests.post(api_url, json={"producto_id": producto_id, "cantidad": cantidad})
            if response.status_code == 200:
                print("Reabastecimiento solicitado con éxito.")
            else:
                print("Error en la solicitud de reabastecimiento.")
        else:
            print("Proveedor no encontrado.")
