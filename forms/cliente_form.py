from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class ClienteForm(FlaskForm):
    empresa = StringField('Nombre de la Empresa / Cliente', validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField('Correo Electrónico', validators=[DataRequired(), Email()])
    ciudad = StringField('Ciudad', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Guardar Cliente')