from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre del Producto', validators=[DataRequired(message="El nombre es obligatorio.")])
    descripcion = TextAreaField('Descripción')
    precio = FloatField('Precio ($)', validators=[DataRequired(message="Ingrese un precio válido."), NumberRange(min=0.01)])
    stock = IntegerField('Stock', validators=[DataRequired(message="Ingrese la cantidad de stock."), NumberRange(min=0)])
    submit = SubmitField('Guardar Producto')