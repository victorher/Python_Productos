from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, Length, NumberRange

class LoginForm(FlaskForm):
    usuario = StringField('Usuario', validators=[DataRequired()])
    clave = PasswordField('Clave', validators=[DataRequired()])
    submit = SubmitField('Ingresar')

class RegistroForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    correo = StringField('Correo', validators=[DataRequired(), Email()])
    usuario = StringField('Usuario', validators=[DataRequired()])
    clave = PasswordField('Clave', validators=[DataRequired(), Length(min=4)])
    submit = SubmitField('Registrar')

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    cantidad = IntegerField('Cantidad', validators=[DataRequired(), NumberRange(min=1)])
    medida = SelectField('Medida', choices=[
        ('litros', 'Litros'),
        ('kilos', 'Kilos'),
        ('libras', 'Libras'),
        ('onzas', 'Onzas'),
        ('unidades', 'Unidades')
    ], validators=[DataRequired()])
    comprado = BooleanField('Comprado')
    submit = SubmitField('Guardar')