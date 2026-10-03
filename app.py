import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from conexion.conexion import obtener_conexion
from models import Usuario
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm
from forms.login_form import LoginForm
from forms.usuario_form import RegistroForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'tu_clave_secreta_muy_segura')

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, inicia sesión para acceder a esta página.'
login_manager.login_message_category = 'warning'

# --- INICIALIZADOR AUTOMÁTICO DE TABLAS EN POSTGRESQL ---
def inicializar_base_de_datos():
    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id SERIAL PRIMARY KEY,
                    usuario VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL
                );

                CREATE TABLE IF NOT EXISTS proveedores (
                    id SERIAL PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    contacto VARCHAR(100),
                    telefono VARCHAR(15)
                );

                CREATE TABLE IF NOT EXISTS clientes (
                    id SERIAL PRIMARY KEY,
                    empresa VARCHAR(100) NOT NULL,
                    email VARCHAR(120) NOT NULL,
                    ciudad VARCHAR(50) NOT NULL
                );

                CREATE TABLE IF NOT EXISTS productos (
                    id SERIAL PRIMARY KEY,
                    nombre VARCHAR(150) NOT NULL,
                    descripcion TEXT,
                    precio NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
                    stock INT NOT NULL DEFAULT 0,
                    proveedor_id INT REFERENCES proveedores(id) ON DELETE SET NULL,
                    usuario_id INT REFERENCES usuarios(id) ON DELETE SET NULL
                );

                CREATE TABLE IF NOT EXISTS facturas (
                    id SERIAL PRIMARY KEY,
                    cliente VARCHAR(100) NOT NULL,
                    monto NUMERIC(10, 2) NOT NULL,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conexion.commit()
            cursor.close()
            conexion.close()
            print("Tablas verificadas/creadas exitosamente en PostgreSQL.")
        except Exception as e:
            print(f"Error al inicializar tablas en PostgreSQL: {e}")
            if conexion:
                conexion.close()

# Ejecutamos la creación de tablas al arrancar la app
with app.app_context():
    inicializar_base_de_datos()

@login_manager.user_loader
def load_user(user_id):
    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT id, usuario, password FROM usuarios WHERE id = %s", (user_id,))
            row = cursor.fetchone()
            cursor.close()
            conexion.close()
            if row:
                id_u = row['id'] if isinstance(row, dict) else row[0]
                usr = row['usuario'] if isinstance(row, dict) else row[1]
                pwd = row['password'] if isinstance(row, dict) else row[2]
                return Usuario(id=id_u, usuario=usr, password=pwd)
        except Exception as e:
            print(f"Error al cargar usuario: {e}")
            if conexion:
                conexion.close()
    return None

# --- RUTAS DE INICIO Y AUTENTICACIÓN ---

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = RegistroForm()
    if form.validate_on_submit():
        usuario_input = form.usuario.data.strip()
        password_hash = generate_password_hash(form.password.data)

        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT id FROM usuarios WHERE usuario = %s", (usuario_input,))
                if cursor.fetchone():
                    flash("El nombre de usuario ya está registrado.", "danger")
                    cursor.close()
                    conexion.close()
                    return render_template('registro.html', form=form)

                cursor.execute(
                    "INSERT INTO usuarios (usuario, password) VALUES (%s, %s)",
                    (usuario_input, password_hash)
                )
                conexion.commit()
                cursor.close()
                conexion.close()

                flash("Registro exitoso. ¡Ahora puedes iniciar sesión!", "success")
                return redirect(url_for('login'))
            except Exception as e:
                print(f"Error en el registro: {e}")
                flash("Ocurrió un error al registrar el usuario.", "danger")
                if conexion:
                    conexion.close()

    return render_template('registro.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        usuario_input = form.usuario.data.strip()
        password_input = form.password.data

        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT id, usuario, password FROM usuarios WHERE usuario = %s", (usuario_input,))
                user_data = cursor.fetchone()
                cursor.close()
                conexion.close()

                if user_data:
                    u_id = user_data['id'] if isinstance(user_data, dict) else user_data[0]
                    u_usr = user_data['usuario'] if isinstance(user_data, dict) else user_data[1]
                    u_pwd = user_data['password'] if isinstance(user_data, dict) else user_data[2]

                    if check_password_hash(u_pwd, password_input):
                        user_obj = Usuario(id=u_id, usuario=u_usr, password=u_pwd)
                        login_user(user_obj)
                        flash("Inicio de sesión exitoso.", "success")
                        next_page = request.args.get('next')
                        return redirect(next_page or url_for('dashboard'))

                flash("Usuario o contraseña incorrectos.", "danger")
            except Exception as e:
                print(f"Error al iniciar sesión: {e}")
                flash("Error al conectar con la base de datos.", "danger")
                if conexion:
                    conexion.close()

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Has cerrado sesión correctamente.", "info")
    return redirect(url_for('login'))

# --- RUTAS PROTEGIDAS DEL SISTEMA (CRUD POSTGRESQL) ---

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# 1. LEER Y CREAR PRODUCTOS (CORREGIDO PARA EVITAR ERROR 500)
@app.route('/productos', methods=['GET', 'POST'])
@login_required
def productos():
    form = ProductoForm()

    if request.method == 'POST':
        nombre = form.nombre.data.strip() if getattr(form, 'nombre', None) and form.nombre.data else request.form.get('nombre', '').strip()
        descripcion = form.descripcion.data.strip() if getattr(form, 'descripcion', None) and form.descripcion.data else request.form.get('descripcion', '').strip()
        
        try:
            precio = float(form.precio.data) if getattr(form, 'precio', None) and form.precio.data else float(request.form.get('precio', 0.0))
        except (ValueError, TypeError):
            precio = 0.0

        try:
            stock = int(form.stock.data) if getattr(form, 'stock', None) and form.stock.data else int(request.form.get('stock', 0))
        except (ValueError, TypeError):
            stock = 0

        if nombre:
            conexion = obtener_conexion()
            if conexion:
                try:
                    cursor = conexion.cursor()
                    # Inserción limpia a los campos principales
                    query = """
                        INSERT INTO productos (nombre, descripcion, precio, stock)
                        VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(query, (nombre, descripcion, precio, stock))
                    conexion.commit()
                    cursor.close()
                    conexion.close()
                    flash("Producto agregado correctamente.", "success")
                    return redirect(url_for('productos'))
                except Exception as e:
                    print(f"Error al insertar en PostgreSQL: {e}")
                    flash(f"Ocurrió un error al guardar el producto: {e}", "danger")
                    if conexion:
                        conexion.close()

    # Operación LEER (SELECT)
    lista_productos = []
    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre, descripcion, precio, stock FROM productos ORDER BY id DESC;")
            lista_productos = cursor.fetchall()
            cursor.close()
            conexion.close()
        except Exception as e:
            print(f"Error al consultar productos: {e}")
            if conexion:
                conexion.close()

    return render_template('formulario_producto.html', form=form, productos=lista_productos)

# 2. ACTUALIZAR PRODUCTO
@app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_producto(id):
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        precio = request.form.get('precio', 0.0)
        stock = request.form.get('stock', 0)

        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                query = """
                    UPDATE productos 
                    SET nombre=%s, descripcion=%s, precio=%s, stock=%s
                    WHERE id=%s
                """
                cursor.execute(query, (nombre, descripcion, precio, stock, id))
                conexion.commit()
                cursor.close()
                conexion.close()
                flash("Producto actualizado exitosamente.", "success")
                return redirect(url_for('productos'))
            except Exception as e:
                print(f"Error al actualizar producto: {e}")
                flash("Error al actualizar el registro.", "danger")
                if conexion:
                    conexion.close()

    return redirect(url_for('productos'))

# 3. ELIMINAR PRODUCTO
@app.route('/productos/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_producto(id):
    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM productos WHERE id = %s", (id,))
            conexion.commit()
            cursor.close()
            conexion.close()
            flash("Producto eliminado correctamente.", "info")
        except Exception as e:
            print(f"Error al eliminar producto: {e}")
            flash("Error al eliminar el producto.", "danger")
            if conexion:
                conexion.close()

    return redirect(url_for('productos'))

# --- MÓDULOS DE CLIENTES, PROVEEDORES Y FACTURACIÓN ---

@app.route('/clientes', methods=['GET', 'POST'])
@login_required
def clientes():
    form = ClienteForm()
    if request.method == 'POST' and form.validate_on_submit():
        empresa = form.empresa.data.strip()
        email = form.email.data.strip()
        ciudad = form.ciudad.data.strip()

        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute(
                    "INSERT INTO clientes (empresa, email, ciudad) VALUES (%s, %s, %s)",
                    (empresa, email, ciudad)
                )
                conexion.commit()
                cursor.close()
                conexion.close()
                flash("Cliente guardado exitosamente.", "success")
                return redirect(url_for('clientes'))
            except Exception as e:
                print(f"Error al guardar cliente: {e}")
                flash("Error al guardar cliente.", "danger")
                if conexion:
                    conexion.close()

    return render_template('formulario_cliente.html', form=form)

@app.route('/proveedores', methods=['GET', 'POST'])
@login_required
def proveedores():
    form = ProveedorForm()
    if request.method == 'POST' and form.validate_on_submit():
        nombre = form.nombre.data.strip()
        contacto = form.contacto.data.strip()
        telefono = form.telefono.data.strip()

        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute(
                    "INSERT INTO proveedores (nombre, contacto, telefono) VALUES (%s, %s, %s)",
                    (nombre, contacto, telefono)
                )
                conexion.commit()
                cursor.close()
                conexion.close()
                flash("Proveedor guardado exitosamente.", "success")
                return redirect(url_for('proveedores'))
            except Exception as e:
                print(f"Error al guardar proveedor: {e}")
                flash("Error al guardar proveedor.", "danger")
                if conexion:
                    conexion.close()

    return render_template('formulario_proveedor.html', form=form)

@app.route('/facturacion', methods=['GET', 'POST'])
@login_required
def facturacion():
    form = FacturacionForm()
    if request.method == 'POST' and form.validate_on_submit():
        cliente = form.cliente.data.strip()
        monto = form.monto.data

        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute(
                    "INSERT INTO facturas (cliente, monto) VALUES (%s, %s)",
                    (cliente, monto)
                )
                conexion.commit()
                cursor.close()
                conexion.close()
                flash("Factura generada exitosamente.", "success")
                return redirect(url_for('facturacion'))
            except Exception as e:
                print(f"Error al generar factura: {e}")
                flash("Error al generar factura.", "danger")
                if conexion:
                    conexion.close()

    return render_template('formulario_facturacion.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)