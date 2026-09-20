from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import Optional

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre del Producto')
    descripcion = TextAreaField('Descripción')
    precio = StringField('Precio')
    stock = StringField('Stock')