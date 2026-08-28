from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre del Proyecto / Producto', validators=[DataRequired(), Length(min=3, max=100)])
    descripcion = TextAreaField('Descripción', validators=[DataRequired(), Length(min=5, max=250)])
    precio = FloatField('Precio', validators=[DataRequired(), NumberRange(min=0.01)])
    stock = IntegerField('Stock', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Guardar Proyecto')