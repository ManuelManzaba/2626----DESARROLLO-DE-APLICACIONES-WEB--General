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
app.config['SECRET_KEY'] = 'tu_clave_secreta_muy_segura'

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, inicia sesión para acceder a esta página.'
login_manager.login_message_category = 'warning'

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
                return Usuario(id=row[0], usuario=row[1], password=row[2])
        except Exception as e:
            print(f"Error al cargar usuario: {e}")
            if conexion:
                conexion.close()
    return None

# --- RUTAS DE INICIO Y AUTENTICACIÓN ---

@app.route('/')
def index():
    # Si ya inició sesión, va al dashboard; si no, lo redirige directo al login
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
                # Verificar si ya existe el nombre de usuario
                cursor.execute("SELECT id FROM usuarios WHERE usuario = %s", (usuario_input,))
                if cursor.fetchone():
                    flash("El nombre de usuario ya está registrado.", "danger")
                    cursor.close()
                    conexion.close()
                    return render_template('registro.html', form=form)

                # Insertar nuevo usuario con contraseña protegida por hash
                cursor.execute("INSERT INTO usuarios (usuario, password) VALUES (%s, %s)", (usuario_input, password_hash))
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

                if user_data and check_password_hash(user_data[2], password_input):
                    user_obj = Usuario(id=user_data[0], usuario=user_data[1], password=user_data[2])
                    login_user(user_obj)
                    flash("Inicio de sesión exitoso.", "success")
                    next_page = request.args.get('next')
                    return redirect(next_page or url_for('dashboard'))
                else:
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

# --- RUTAS PROTEGIDAS DEL SISTEMA ---

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/productos', methods=['GET', 'POST'])
@login_required
def productos():
    form = ProductoForm()
    
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        precio_raw = request.form.get('precio', '0')
        stock_raw = request.form.get('stock', '0')
        
        try:
            precio = float(precio_raw) if precio_raw else 0.0
        except ValueError:
            precio = 0.0
            
        try:
            stock = int(stock_raw) if stock_raw else 0
        except ValueError:
            stock = 0
            
        if nombre:
            conexion = obtener_conexion()
            if conexion:
                try:
                    cursor = conexion.cursor()
                    try:
                        query = "INSERT INTO productos (nombre, descripcion, precio, stock) VALUES (%s, %s, %s, %s)"
                        cursor.execute(query, (nombre, descripcion, precio, stock))
                    except Exception:
                        query = "INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s)"
                        cursor.execute(query, (nombre, precio, stock))
                        
                    conexion.commit()
                    cursor.close()
                    conexion.close()
                except Exception as e:
                    print(f"Error al insertar en MySQL: {e}")
                    if conexion:
                        conexion.close()
                        
        return redirect(url_for('productos'))

    lista_productos = []
    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            try:
                cursor.execute('SELECT id_producto, nombre, descripcion, precio, stock FROM productos')
                filas = cursor.fetchall()
                for fila in filas:
                    lista_productos.append((
                        int(fila[0]),
                        str(fila[1]),
                        str(fila[2]) if fila[2] else "",
                        str(fila[3]),
                        int(fila[4])
                    ))
            except Exception:
                cursor.execute('SELECT id_producto, nombre, precio, stock FROM productos')
                filas = cursor.fetchall()
                for fila in filas:
                    lista_productos.append((
                        int(fila[0]),
                        str(fila[1]),
                        "",
                        str(fila[2]),
                        int(fila[3])
                    ))
            cursor.close()
            conexion.close()
        except Exception as e:
            print(f"Error al consultar en MySQL: {e}")
            if conexion:
                conexion.close()
                
    return render_template('formulario_producto.html', form=form, productos=lista_productos)

@app.route('/clientes', methods=['GET', 'POST'])
@login_required
def clientes():
    form = ClienteForm()
    return render_template('formulario_cliente.html', form=form)

@app.route('/proveedores', methods=['GET', 'POST'])
@login_required
def proveedores():
    form = ProveedorForm()
    return render_template('formulario_proveedor.html', form=form)

@app.route('/facturacion', methods=['GET', 'POST'])
@login_required
def facturacion():
    form = FacturacionForm()
    return render_template('formulario_facturacion.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)