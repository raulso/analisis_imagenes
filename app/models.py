import os
import psycopg2
from flask import request,send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime
from test import reconocimiento
from PIL import Image
from PIL.ExifTags import TAGS
from werkzeug.security import generate_password_hash, check_password_hash




ALLOWED_EXTENSIONS = {'jpg'}

def get_db_connection():
    """conn = psycopg2.connect(host='localhost',
                                database='bd_pg_flask',
                                user='postgres',
                                password='root')
    """

    conn = psycopg2.connect(host='localhost',
                                database='bd_deteccionA',
                                user='postgres',
                                password='root')
    return conn

 #cargar archivos al servidor
def allowed_file(filename):
    return '.' in filename and \
       filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



class pg_data():

    def save(form):
        name = form.name.data
        edad = form.edad.data
        password = form.password.data
        descripcion = form.descripcion.data

        estatus = True
        valor = ''
        texto = ''
        conn = get_db_connection()
        
        try:
            cur = conn.cursor()
            cur.execute('INSERT INTO sc_prueba.tbl_prueba (nombre, edad, contrasena, descripcion)'
                        'VALUES (%s, %s, %s, %s)',
                        (name, edad, password, descripcion))
            conn.commit()
            valor =  0
        except (Exception, psycopg2.Error) as error:
            print("Failed to insert record into mobile table", error)
            valor = 1
        finally:    
            cur.close()
            conn.close()
        return valor


    def list_regImg():
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT fecha_carga, hora_carga,  directorio_prc,  count(id_imagen), carpeta FROM sc_deteccion.tbl_imagen group by directorio_src,fecha_carga,hora_carga,directorio_prc, carpeta')
        registros = cur.fetchall()
        cur.close()

        return registros

    def loadImage(form,folder):
        
        print("************************"+folder+"******************")
        name = form.files.data
        now = datetime.now()
        nombreFolder =str(format(now.year))+str(format(now.month))+str(format(now.day))+str(format(now.hour))+str(format(now.minute))+str(format(now.second))
        
        fecha_carga = str(format(now.year))+'-'+str(format(now.month))+'-'+str(format(now.day))
        hora_carga = str(format(now.hour))+':'+str(format(now.minute))+':'+str(format(now.second))
   

        nombreDirSrc = folder+'/'+nombreFolder+'/source'
        nombreDirPrs = folder+'/'+nombreFolder+'/process'
        directorioOri =  creaFolder(nombreDirSrc,nombreDirPrs)
        print("-----RSO--------"+nombreDirSrc+"------RSO-------")

        if 'files' not in request.files:
            print('No file part')
            #return redirect(request.url)
        files = request.files.getlist('files')
        file_names = []
        for file in files:
            if file and allowed_file(file.filename):

                filename = secure_filename(file.filename)
                file_names.append(filename)
                file.save(os.path.join(nombreDirSrc, filename))

                lastID =  insertImgData(nombreDirSrc, nombreDirPrs, filename, nombreFolder, fecha_carga, hora_carga )
                
            #else:
            #   flash('Allowed image types are -> png, jpg, jpeg, gif')
            #   return redirect(request.url)f

        reconocimiento.boundingHuman(nombreDirSrc,nombreDirPrs)

        return nombreDirSrc



    def showImg():
        directorioOri =  'uploads'
        print("aqui***"+directorioOri+"---")
        return directorioOri

    def consultImgRuta():
        valor =''
        conn = get_db_connection()
        cur = conn.cursor()
        rows_affected = cur.execute('SELECT  directorio_prc FROM sc_deteccion.tbl_imagen where id_imagen = (select max(id_imagen) from sc_deteccion.tbl_imagen)')
        row = cur.fetchall()
        
        cur.close()
        print("tardado")

        conteo = len(row)
        print(conteo)
        #print(row[0][0])
        
        if conteo > 0 :
            valor = row[0][0]
        else :
            valor = 'static/uploads'
        return valor
            
    

class catalogos():

    def listNivel():
        choices = list()
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT idnivel, nivel FROM sc_deteccion.cat_nivel where idnivel <> 0 ORDER BY idnivel ASC')
        registros = cur.fetchall()
        cur.close()
        choices.append(('','SELECCIONE...'))
        for registro in registros:
            choices.append((registro[0], registro[1]))
        return choices

    def listElem():
        choices = list()
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT idelemento, (nombre || ' ' || appaterno || ' ' || apmaterno) as nombre FROM sc_deteccion.tbl_elemento where idelemento <> 0 ORDER BY idelemento ASC")
        registros = cur.fetchall()
        cur.close()
        choices.append(('','SELECCIONE...'))
        for registro in registros:
            choices.append((registro[0], registro[1]))
        return choices

    def listGrados():
        choices = list()
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT idgrado, nomgrado FROM sc_deteccion.cat_grado ORDER BY idgrado ASC ")
        registros = cur.fetchall()
        cur.close()
        choices.append(('','SELECCIONE...'))
        for registro in registros:
            choices.append((registro[0], registro[1]))
        return choices


class usuarios():
    def login(form):
        lista={}
        username = form.username.data
        
        conn = get_db_connection()
        cur = conn.cursor()
        consulta = "SELECT idusuario, username,  password, idnivel, estatus FROM sc_deteccion.tbl_usuario where username = %s limit 1"
        cur.execute(consulta,(username,))
      
        registros = cur.fetchall()
        print("*****************************")
        if len(registros) > 0:
            for row in registros:
                lista["idusuario"]=row[0]
                lista["username"]=row[1]
                lista["password"]=row[2]
                lista["idnivel"]=row[3]
                lista["estatus"]=row[4]
                #user = {"idusuario":row[0],"username":row[1],"password":row[2],"idnivel":row[3],"estatus":row[4]}
                print(lista)
        else:
            lista["idusuario"]="0"
            lista["username"]="0"
            lista["password"]="0"
            lista["idnivel"]="0"
            lista["estatus"]="0"
            #user = {"idusuario":row[0],"username":row[1],"password":row[2],"idnivel":row[3],"estatus":row[4]}
            print(lista) 
        
        cur.close()
        return lista


    def save(form):
        now = datetime.now()
        fecha_carga = str(format(now.year))+'-'+str(format(now.month))+'-'+str(format(now.day))
        username = form.username.data
        password1 =  generate_password_hash(form.password1.data)
        idelemento = form.idelemento.data
        idnivel = form.idnivel.data
        estatus = True
        valor = ''
        texto = ''
       

        numUser = usuarios.validaUsername(username)
        print("****Nunero de usuarios")
        print(numUser)

        if numUser == 0:
            conn = get_db_connection()
        
            try:
                cur = conn.cursor()
                cur.execute('INSERT INTO sc_deteccion.tbl_usuario(username, password, idelemento, idnivel, fechaalta)'
                            'VALUES (%s, %s, %s, %s, %s)',
                            (username, password1, idelemento, idnivel, fecha_carga))
                conn.commit()
                valor =  0
            except (Exception, psycopg2.Error) as error:
                print("Failed to insert record into mobile table", error)
                valor = 1
            finally:    
                cur.close()
                conn.close()
        else:
            valor = 1


        return valor


    def validaUsername(username):
        conn = get_db_connection()
        valor = ''
      
        try:
            cur = conn.cursor()
            consulta = "SELECT idusuario, username,  password, idnivel, estatus FROM sc_deteccion.tbl_usuario where username = %s limit 1"
            cur.execute(consulta,(username,))
            
            registros = cur.fetchall()

            if len(registros) > 0:
                valor =  len(registros)
            else:
                valor = 0
        except (Exception, psycopg2.Error) as error:
            print("Failed to insert record into mobile table", error)
            valor = 0
        finally:    
            cur.close()
            conn.close()

        return valor

    def saveEle(form):
        expediente = form.expediente.data
        nombre = form.nombre.data
        appaterno = form.appaterno.data
        apmaterno = form.apmaterno.data
        idgrado = form.idgrado.data
        activo = True
        correo = form.correo.data
        telefono= form.telefono.data
        valor = ''
        texto = ''
       

        numExp = usuarios.validaExp(expediente)
        print("****Nunero de usuarios")
        print(numExp)

        if numExp == 0:
            conn = get_db_connection()
        
            try:
                cur = conn.cursor()
                cur.execute('INSERT INTO sc_deteccion.tbl_elemento(numexpediente, nombre, appaterno, apmaterno, idgrado, elemactivo, correo, telefono )'
                            'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                            (expediente, nombre, appaterno, apmaterno, idgrado, activo, correo, telefono))
                conn.commit()
                valor =  0
            except (Exception, psycopg2.Error) as error:
                print("Failed to insert record into mobile table", error)
                valor = 1
            finally:    
                cur.close()
                conn.close()
        else:
            valor = 1


        return valor

    def validaExp(expediente):
        conn = get_db_connection()
        valor = ''
      
        try:
            cur = conn.cursor()
            consulta = "SELECT numexpediente FROM sc_deteccion.tbl_elemento where numexpediente = %s limit 1"
            cur.execute(consulta,(expediente,))
            
            registros = cur.fetchall()

            if len(registros) > 0:
                valor =  len(registros)
            else:
                valor = 0
        except (Exception, psycopg2.Error) as error:
            print("Failed to insert record into mobile table", error)
            valor = 0
        finally:    
            cur.close()
            conn.close()

        return valor  

    def list_usuarios():
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT b.numexpediente, (b.nombre || ' ' || b.appaterno || ' ' || b.apmaterno) as nombre, " +
                    "username, c.nivel, a.estatus,c.idnivel, a.idelemento " +
                    "FROM sc_deteccion.tbl_usuario a, sc_deteccion.tbl_elemento b, sc_deteccion.cat_nivel c " +
                    "where b.idelemento = a.idelemento and c.idnivel = a.idnivel and a.idelemento = b.idelemento")
        registros = cur.fetchall()
        cur.close()

        return registros  



def creaFolder(folderSrc,folderPrs):
    os.makedirs(folderSrc)
    os.makedirs(folderPrs)
    return folderSrc


def insertImgData(folderSrc,folderPrs, filename, nombreFolder, fecha_carga, hora_carga):
    name = filename
    directorioOri = folderSrc
    directorioPrs = folderPrs
    observacion = 'obs'

    estatus = True
    valor = ''
    texto = ''
    conn = get_db_connection()
        
    try:
        cur = conn.cursor()
        cur.execute('INSERT INTO sc_deteccion.tbl_imagen (nombre_imagen, fecha_carga, directorio_src, observacion, hora_carga,directorio_prc, carpeta)'
                    'VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id_imagen',
                    (name, fecha_carga, directorioOri, observacion,hora_carga,directorioPrs, nombreFolder))
        conn.commit()
        lastID = cur.fetchone()[0]

        valor =  lastID
    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into", error)
        valor = 1
    finally:    
        cur.close()
        conn.close()

    return valor    