"""
Libs rso
"""
import os
import shutil
import imutils 
import datetime 
import cv2
from peddec.pedestrian_detection_ssdlite import api
from matplotlib import pyplot as plt




class reconocimiento():
   


    def boundingHuman(dirOri,dirPrs):

        ejemplo_dir = 'peddec/test_img/'
        nombre = ""
        count = 0
        with os.scandir(dirOri) as ficheros:
            for fichero in ficheros:
                nombre = dirOri + "/" +fichero.name 
                img = cv2.imread(nombre)
                bbox_list = api.get_person_bbox(img, thr=0.6)

                if len(bbox_list) > 0: 
                        hum_exist = True
                        print("Personas true") 
                else:
                        hum_exist = False
                
                print("Numero de Perrsonas encontradas:", len(bbox_list))

                for i in bbox_list:
                    cv2.rectangle(img, i[0], i[1], (125, 255, 51), thickness=2)

                #proceso de guardado en carpeta 
                if hum_exist: 
                        print("Personas detectada") 
                        count += 1
                        #nombre_nuevo = 'peddec/personas/persona_' + str(count) + ".jpg"
                        nombre_nuevo = dirPrs+'/persona_' + str(count) + ".jpg"
                        #print(count)
                        #os.rename(nombre, nombre_nuevo)
                        #newFileName=shutil.copy(frame, nombre_nuevo)
                        cv2.imwrite(nombre_nuevo,img)

                else: 
                        print("No detectada") 

                cv2.imshow("Test", img)
                cv2.waitKey(1000)