from flask import Flask, render_template, redirect, url_for, flash
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave-secreta-proyecto-integrador-2026'

@app.route("/")
def home():
    titulo_seccion = "Panel de Control Tecnológico"
    info_usuario = {
        "nombre": "Manuel Manzaba",
        "carrera": "Tecnologías de la Información",
        "semestre": "Ciclo Activo"
    }
    return render_template("index.html", titulo=titulo_seccion, usuario=info_usuario)

@app.route("/productos", methods=['GET', 'POST'])
def productos():
    form = ProductoForm()
    lista_productos = [
        {"id": 1, "nombre": "Licenciamiento Software Web", "precio": 150.00, "stock": 10},
        {"id": 2, "nombre": "Servidor Cloud VPS", "precio": 300.00, "stock": 0},
        {"id": 3, "nombre": "Mantenimiento Preventivo IT", "precio": 80.00, "stock": 5},
        {"id": 4, "nombre": "Auditoría de Redes", "precio": 200.00, "stock": 0}
    ]
    if form.validate_on_submit():
        flash('¡Proyecto/Producto registrado correctamente!', 'success')
        return redirect(url_for('productos'))
    return render_template("productos.html", productos=lista_productos, form=form)

@app.route("/clientes", methods=['GET', 'POST'])
def clientes():
    form = ClienteForm()
    lista_clientes = [
        {"empresa": "Corporación Alfa", "ciudad": "Quito", "activo": True},
        {"empresa": "Soluciones Beta", "ciudad": "Santo Domingo", "activo": False},
        {"empresa": "Global Tech S.A.", "ciudad": "Manta", "activo": True}
    ]
    if form.validate_on_submit():
        flash('¡Cliente registrado correctamente!', 'success')
        return redirect(url_for('clientes'))
    return render_template("clientes.html", clientes=lista_clientes, form=form)

@app.route("/proveedores", methods=['GET', 'POST'])
def proveedores():
    form = ProveedorForm()
    if form.validate_on_submit():
        flash('¡Proveedor registrado correctamente!', 'success')
        return redirect(url_for('proveedores'))
    return render_template("proveedores.html", form=form)

@app.route("/facturacion", methods=['GET', 'POST'])
def facturacion():
    form = FacturacionForm()
    if form.validate_on_submit():
        flash('¡Factura generada correctamente!', 'success')
        return redirect(url_for('facturacion'))
    return render_template("facturacion.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)