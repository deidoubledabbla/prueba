from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'clave-secreta'

def get_db():
    conn = sqlite3.connect('kardex.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        contraseña = request.form['contraseña']
        db = get_db()
        user = db.execute("SELECT * FROM usuarios WHERE email=? AND contraseña=?", (email, contraseña)).fetchone()
        if user:
            session['user'] = user['nombre']
            return redirect('/dashboard')
        return render_template('login.html', error="Credenciales inválidas")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    db = get_db()
    productos = db.execute("SELECT * FROM productos").fetchall()
    return render_template('dashboard.html', productos=productos, user=session['user'])

@app.route('/movimientos', methods=['GET', 'POST'])
def movimientos():
    if 'user' not in session:
        return redirect('/login')
    db = get_db()
    if request.method == 'POST':
        tipo = request.form['tipo']
        producto_id = request.form['producto_id']
        cantidad = int(request.form['cantidad'])
        descripcion = request.form['descripcion']
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        db.execute("""
            INSERT INTO movimientos (producto_id, tipo, cantidad, fecha, descripcion)
            VALUES (?, ?, ?, ?, ?)
        """, (producto_id, tipo, cantidad, fecha, descripcion))

        if tipo == 'entrada':
            db.execute("UPDATE productos SET stock_actual = stock_actual + ? WHERE id = ?", (cantidad, producto_id))
        else:
            db.execute("UPDATE productos SET stock_actual = stock_actual - ? WHERE id = ?", (cantidad, producto_id))

        db.commit()
        return redirect('/dashboard')

    productos = db.execute("SELECT * FROM productos").fetchall()
    movimientos = db.execute("""
        SELECT m.*, p.nombre as producto
        FROM movimientos m JOIN productos p ON m.producto_id = p.id
        ORDER BY fecha DESC
    """).fetchall()

    return render_template('movimientos.html', productos=productos, movimientos=movimientos, user=session['user'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 8000))
    app.run(debug=False, host="0.0.0.0", port=port)
