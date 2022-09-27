import json
from os import getcwd
import uuid
from flask import Flask, render_template, request, redirect, url_for,flash,jsonify,send_file,send_from_directory, session
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import *
from forms import SignupForm, FormImg, FormRegistro, FormLogin, FormRegistroEle
from models import *
from werkzeug.utils import secure_filename
import urllib.request
from os.path import abspath, dirname, join
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import  check_password_hash
from datetime import timedelta


app = Flask(__name__)


app.config['UPLOAD_FOLDER'] = "static/uploads"
BASE_DIR = dirname(dirname(abspath(__file__)))
# Media dir
MEDIA_DIR = join(BASE_DIR, 'uploads')
#POSTS_IMAGES_DIR = join(MEDIA_DIR, 'posts')
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
app.permanent_session_lifetime = timedelta(minutes=20)



@app.route('/')
def index():
    return redirect(url_for('login'))
    #return render_template('login.html', form=form)

##################################
#Fromulario y proceso de registro#
##################################
@app.route('/registro/', methods=["GET", "POST"])
def registro():
    form = SignupForm()
    if form.validate_on_submit():
        flash(pg_data.save(form))
        return redirect(url_for('registro'))
    return render_template('registro.html', form=form)

##################################
#Consulta y listado origen BD#####
##################################
"""

Inicia carga de imagenes

"""

@app.route('/uploaderFlk/', methods=["GET", "POST"])
def uploaderFlk():
    if not session.get("user"):
        return redirect("/login")

    else:
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        directorio = pg_data.consultImgRuta()
        listDir = os.listdir(directorio)
        print("****Modulo uploaderFlk****")
        form = FormImg()
        if form.validate_on_submit():
           pg_data.loadImage(form ,app.config['UPLOAD_FOLDER'])
           return redirect(url_for('uploaderFlk'))
           
        dir = os.path.dirname(directorio)+"/process"
    return render_template('upload_flsk.html', form=form, files=listDir,directorio=dir )


@app.route('/consul_reg', methods=["GET", "POST"])
def consul_reg():
    if not session.get("user"):
        return redirect("/login")

    else:
        datos = pg_data.list_regImg() 
        return render_template('consul_reg_img.html',  datos=datos)


@app.route('/uploader', methods=['POST'])
def uploader():
    if 'files[]' not in request.files:
        flash('No file part')
        return redirect(request.url)
    files = request.files.getlist('files[]')
    file_names = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_names.append(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #else:
        #   flash('Allowed image types are -> png, jpg, jpeg, gif')
        #   return redirect(request.url)

    return render_template('upload.html', files=file_names)

@app.route('/<directorio>/<filename>')
def display_image(directorio,filename):
    return send_from_directory(directorio, filename, as_attachment=false)



#Para envio por ajax obtener  listado de imagenes
@app.route('/lista_imagenes_pro', methods=["GET", "POST"])
def lista_imagenes_pro():
   if request.method == 'POST':
        carpeta = app.config['UPLOAD_FOLDER']
        ruta = request.form['dir'] 
        directorio = carpeta + "/" + ruta + "/process"
        listDir = os.listdir(directorio)
        print(directorio)
        return jsonify({'htmlresponse':render_template('lista_imagen.html', files=listDir,directorio=directorio, lote=ruta, titulo='Procesadas' )})

@app.route('/lista_imagenes_ori', methods=["GET", "POST"])
def lista_imagenes_ori():
   if request.method == 'POST':
        carpeta = app.config['UPLOAD_FOLDER']
        ruta = request.form['dir'] 
        directorio = carpeta + "/" + ruta + "/source"
        listDir = os.listdir(directorio)
        print(directorio)
        return jsonify({'htmlresponse':render_template('lista_imagen.html', files=listDir,directorio=directorio, lote=ruta, titulo='Imagenes fuente' )})


#registro de usuarios
@app.route('/registro_us/', methods=["GET", "POST"])
def registro_us():
    error = None
    if not session.get("user"):
        return redirect("/login")
    else:
        form = FormRegistro()
        if form.validate_on_submit():
            res =   usuarios.save(form)
            if res == 0:
               flash('Registro exitoso')
               return redirect(url_for('registro_us'))
            else: 
                error = "- Usuario ya existe, Ingrese otro -" 

        return render_template('registro_us.html', form=form, error=error)

#registro de elementos
@app.route('/registro_ele', methods=["GET", "POST"])
def registro_ele():
    error = None
    if not session.get("user"):
        return redirect("/login")
    else:
        form = FormRegistroEle()
        if form.validate_on_submit():
            res =   usuarios.saveEle(form)
            if res == 0:
               flash('Registro exitoso')
               return redirect(url_for('registro_ele'))
            else: 
                error = "- Expediente ya existe, Ingrese otro -" 

        return render_template('registro_ele.html', form=form, error=error)

##################################
#consulta de usuarios
#################################
@app.route('/consul_usuarios', methods=["GET", "POST"])
def consul_usuarios():
    if not session.get("user"):
        return redirect("/login")

    else:
        datos = usuarios.list_usuarios() 
        return render_template('consul_usuarios.html',  datos=datos)

#Para obtener por ajax obtener datos de usuario
@app.route('/frm_editUser', methods=["GET", "POST"])
def frm_editUser():
   if request.method == 'POST':
        idelem = request.form['idelem'] 
        return jsonify({'htmlresponse':render_template('frm_editUser.html', idelem=idelem, titulo='Edicion de datos del usuario' )})

#Para obtener por ajax obtener datos de usuario
@app.route('/frm_editElem', methods=["GET", "POST"])
def frm_editElem():
   if request.method == 'POST':
        idelem = request.form['idelem'] 
        print("-------------")
        print(idelem)
        return jsonify({'htmlresponse':render_template('frm_editElem.html', titulo='Edicion de datos del elemento' )})


#validacion de usuarios
 
@app.route('/login', methods = ['POST', 'GET'])
def login():
    form = FormLogin()
    msg = ''
    if form.validate_on_submit():
        if(request.method == 'POST'):
            users = usuarios.login(form)
            user = users #{"usuario": "abc", "password": "xyz"}
            username = request.form['username']
            password = request.form['password'] 

            if username == user['username'] and check_password_hash(user['password'],password):
                session.permanent = True
                session['user'] = username
                return redirect('/home')
            else:
                msg = 'Usuario o contraseña incorrecta'
                return render_template("login.html",form=form,msg=msg)
            #return "<h1>Wrong username or password</h1>"    #if the username or password does not matches 

    return render_template("login.html",form=form)


@app.route('/logout')
def logout():
    session.pop('user')         #session.pop('user') help to remove the session from the browser
    return redirect('/login')


@app.route('/home')
def home():
    if not session.get("user"):
        return redirect("/login")
    else:
        datos = pg_data.list_regImg() 
        return render_template('consul_reg_img.html',  datos=datos)
        #return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True,use_debugger=False, use_reloader=False)