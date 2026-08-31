from flask import Flask, render_template, redirect, url_for
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_muy_segura'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/productos', methods=['GET', 'POST'])
def productos():
    form = ProductoForm()
    if form.validate_on_submit():
        # Aquí puedes procesar los datos válidos en el futuro
        pass
    return render_template('formulario_producto.html', form=form)

@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    form = ClienteForm()
    if form.validate_on_submit():
        pass
    return render_template('formulario_cliente.html', form=form)

@app.route('/proveedores', methods=['GET', 'POST'])
def proveedores():
    form = ProveedorForm()
    if form.validate_on_submit():
        pass
    return render_template('formulario_proveedor.html', form=form)

@app.route('/facturacion', methods=['GET', 'POST'])
def facturacion():
    form = FacturacionForm()
    if form.validate_on_submit():
        pass
    return render_template('formulario_facturacion.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)