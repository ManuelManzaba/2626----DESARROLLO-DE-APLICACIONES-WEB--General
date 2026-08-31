import os
import sqlite3
from flask import Flask, render_template, redirect, url_for, request
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_muy_segura'

# Ruta de la base de datos SQLite
DB_PATH = os.path.join('data', 'ferreteria.db')

def init_db():
    """Crea la base de datos y la tabla de productos si no existen"""
    os.makedirs('data', exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Inicializar la base de datos al arrancar la app
init_db()

@app.route('/')
def index():
    return render_template('index.html', usuario="Manuel")

@app.route('/productos', methods=['GET', 'POST'])
def productos():
    form = ProductoForm()
    
    if form.validate_on_submit():
        # Capturar datos del formulario validado
        nombre = form.nombre.data
        descripcion = form.descripcion.data
        precio = form.precio.data
        stock = form.stock.data
        
        # Guardar en SQLite usando consultas parametrizadas
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO productos (nombre, descripcion, precio, stock)
            VALUES (?, ?, ?, ?)
        ''', (nombre, descripcion, precio, stock))
        conn.commit()
        conn.close()
        
        return redirect(url_for('productos'))
    
    # Consultar productos almacenados para mostrarlos en la tabla
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, nombre, descripcion, precio, stock FROM productos')
    lista_productos = cursor.fetchall()
    conn.close()
    
    return render_template('formulario_producto.html', form=form, productos=lista_productos, usuario="Manuel")

@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    form = ClienteForm()
    if form.validate_on_submit():
        pass
    return render_template('formulario_cliente.html', form=form, usuario="Manuel")

@app.route('/proveedores', methods=['GET', 'POST'])
def proveedores():
    form = ProveedorForm()
    if form.validate_on_submit():
        pass
    return render_template('formulario_proveedor.html', form=form, usuario="Manuel")

@app.route('/facturacion', methods=['GET', 'POST'])
def facturacion():
    form = FacturacionForm()
    if form.validate_on_submit():
        pass
    return render_template('formulario_facturacion.html', form=form, usuario="Manuel")

if __name__ == '__main__':
    app.run(debug=True)