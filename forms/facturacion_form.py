from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class FacturacionForm(FlaskForm):
    cliente = StringField('Cliente Facturado', validators=[DataRequired()])
    monto = FloatField('Monto Total ($)', validators=[DataRequired(), NumberRange(min=0.01)])
    submit = SubmitField('Generar Factura')