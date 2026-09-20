from flask import Flask, render_template, redirect, url_for, request
from conexion.conexion import obtener_conexion
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_muy_segura'

@app.route('/')
def index():
    return render_template('index.html', usuario="Manuel")

@app.route('/productos', methods=['GET', 'POST'])
def productos():
    form = ProductoForm()
    
    # 1. GUARDAR EN MYSQL AL ENVIAR FORMULARIO (POST)
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

    # 2. CONSULTAR PRODUCTOS
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
                
    return render_template('formulario_producto.html', form=form, productos=lista_productos, usuario="Manuel")

@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    form = ClienteForm()
    return render_template('formulario_cliente.html', form=form, usuario="Manuel")

@app.route('/proveedores', methods=['GET', 'POST'])
def proveedores():
    form = ProveedorForm()
    return render_template('formulario_proveedor.html', form=form, usuario="Manuel")

@app.route('/facturacion', methods=['GET', 'POST'])
def facturacion():
    form = FacturacionForm()
    return render_template('formulario_facturacion.html', form=form, usuario="Manuel")

if __name__ == '__main__':
    app.run(debug=True)