from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    # Variable simple y diccionario para la página de inicio
    titulo_seccion = "Panel de Control Tecnológico"
    info_usuario = {
        "nombre": "Manuel Manzaba",
        "carrera": "Tecnologías de la Información",
        "semestre": "Ciclo Activo"
    }
    return render_template("index.html", titulo=titulo_seccion, usuario=info_usuario)


@app.route("/productos")
def productos():
    # Lista de diccionarios para cumplir con los bucles y condiciones de Jinja2
    lista_productos = [
        {"id": 1, "nombre": "Licenciamiento Software Web", "precio": 150.00, "stock": 10},
        {"id": 2, "nombre": "Servidor Cloud VPS", "precio": 300.00, "stock": 0},
        {"id": 3, "nombre": "Mantenimiento Preventivo IT", "precio": 80.00, "stock": 5},
        {"id": 4, "nombre": "Auditoría de Redes", "precio": 200.00, "stock": 0}
    ]
    return render_template("productos.html", productos=lista_productos)


@app.route("/clientes")
def clientes():
    lista_clientes = [
        {"empresa": "Corporación Alfa", "ciudad": "Quito", "activo": True},
        {"empresa": "Soluciones Beta", "ciudad": "Santo Domingo", "activo": False},
        {"empresa": "Global Tech S.A.", "ciudad": "Manta", "activo": True}
    ]
    return render_template("clientes.html", clientes=lista_clientes)


@app.route("/proveedores")
def proveedores():
    return render_template("proveedores.html")


@app.route("/facturacion")
def facturacion():
    return render_template("facturacion.html")


if __name__ == "__main__":
    app.run(debug=True)