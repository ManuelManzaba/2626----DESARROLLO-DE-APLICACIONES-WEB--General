from flask_wtf import FlaskForm
from wtforms import StringField, TelField, SubmitField
from wtforms.validators import DataRequired, Length

class ProveedorForm(FlaskForm):
    nombre = StringField('Nombre del Proveedor', validators=[DataRequired(), Length(min=2, max=100)])
    contacto = StringField('Persona de Contacto', validators=[DataRequired(), Length(min=2, max=100)])
    telefono = TelField('Teléfono', validators=[DataRequired(), Length(min=7, max=15)])
    submit = SubmitField('Guardar Proveedor')