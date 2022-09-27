import os
import psycopg2
from werkzeug.utils import secure_filename
from datetime import datetime
from PIL.ExifTags import TAGS


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                                database='bd_deteccionA',
                                user='postgres',
                                password='root')
    return conn



class catalogos():

    def listNivel():
        choices = list()
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT idnivel, nivel FROM sc_deteccion.cat_nivel ORDER BY idnivel ASC')
        registros = cur.fetchall()
        cur.close()

        for registro in registros:
            choices.append((registro[0], registro[1]))

        print(choices)

        return choices

  