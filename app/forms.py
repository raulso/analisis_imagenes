from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, PasswordField,TextAreaField,SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from models import *



class SignupForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(max=64)])
    edad = StringField('Edad', validators=[DataRequired(), Length(max=2)])
    password = PasswordField('Password', validators=[DataRequired()])
    #email = StringField('Email', validators=[DataRequired(), Email()])
    descripcion = StringField('Descripcion', validators=[DataRequired(), Length(max=200)])
    submit = SubmitField('Registrar')


class FormImg(FlaskForm):
    files = FileField( validators=[FileAllowed(['jpg'], 'Solo formato JPG'),FileRequired('Campo imagen requerido!')])
    submit = SubmitField('Cargar')

class FormRegistro(FlaskForm):
    niveles = catalogos.listNivel()
    elementos = catalogos.listElem()
    username = StringField('Nombre de usuario', validators =[DataRequired('Campo requerido')])
    password1 = PasswordField('Password', validators = [DataRequired('Campo requerido')])
    password2 = PasswordField('Confirmar Password', validators = [DataRequired('Campo requerido'),EqualTo('password1', message='Contraseñas deben ser iguales')])
    idelemento = SelectField('Elemento',choices=elementos, validators =[DataRequired('Campo requerido')])
    idnivel = SelectField('Nivel',choices=niveles, validators =[DataRequired('Campo requerido')])
    submit = SubmitField('Enviar')

class FormRegistroEle(FlaskForm):
    grados = catalogos.listGrados()
    expediente = StringField('Expediente', validators =[DataRequired('Campo requerido')])
    nombre = StringField('Nombre', validators =[DataRequired('Campo requerido')])
    appaterno = StringField('Apellido paterno', validators =[DataRequired('Campo requerido')])
    apmaterno = StringField('Apellido Materno', validators =[DataRequired('Campo requerido')])
    idgrado = SelectField('Grado',choices=grados, validators =[DataRequired('Campo requerido')])
    correo = StringField('Correo electronico', validators =[DataRequired('Campo requerido'),Email(message='Correo invalido')])
    telefono = StringField('Telefono', validators =[DataRequired('Campo requerido')])
    submit = SubmitField('Registrar')



class FormLogin(FlaskForm):
    username = StringField('Usuario', validators =[DataRequired('Campo requerido')])
    password = PasswordField('Contraseña', validators = [DataRequired('Campo requerido')])
    submit = SubmitField('Entrar')


