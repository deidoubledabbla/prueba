# crear_db.py
import sqlite3

conn = sqlite3.connect("kardex.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT, email TEXT, contraseña TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT, codigo TEXT, unidad TEXT, stock_actual INTEGER DEFAULT 0
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS movimientos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto_id INTEGER,
    tipo TEXT,
    cantidad INTEGER,
    fecha TEXT,
    descripcion TEXT,
    FOREIGN KEY (producto_id) REFERENCES productos(id)
)
""")

# Usuario de prueba
c.execute("INSERT INTO usuarios (nombre, email, contraseña) VALUES ('Admin', 'admin@kardex.com', '123')")

# Productos de ejemplo
c.execute("INSERT INTO productos (nombre, codigo, unidad, stock_actual) VALUES ('Lapiceros', 'LP001', 'Unidad', 100)")
c.execute("INSERT INTO productos (nombre, codigo, unidad, stock_actual) VALUES ('Cuadernos', 'CU001', 'Unidad', 200)")

conn.commit()
conn.close()
