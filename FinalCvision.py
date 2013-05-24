import cv #Libreria OpenCV
from math import *
from sys import argv #toma argumento 
import random 
import Image,ImageDraw #Libreria Image de PIL
import numpy as np 
import math #libreria para operacioio matematicas

def detect_painting(image):
    image = filtro(image)
    image,gx,gy,minimo,maximo,conv = mascara(image)
    imgnor=normalizar(image,minimo,maximo,conv)
    imbina = binarizar(image)

def pistola(entradafinal):
	scale = cv.CreateImage((image_size),snapshot.depth,1)
        storage = cv.CreateMemStorage()
        cv.EqualizeHist(scale, scale)
	cascade2=cv.Load("pistoladetect.xml")
        pistola = cv.HaarDetectObjects(scale, cascade2, storage, 1.1, 2, 0, ( 120, 120))
	if pistola:
            # Vamos cara por cara
	    contadodepisto=0
            for i in pistola:
                # Dibujamos figuras en cara
		contadodepisto+=1
                cv.Rectangle(entradafinal, ( i[0][0], i[0][1]), ((i[0][0] + i[0][2]), (i[0][1] + i[0][2])), cv.RGB(0, 255, 0),10, 8, 0)
                center_point = ((i[0][0]*2 + i[0][2])/2, (i[0][1]*2 + i[0][2])/2 )
                cv.Circle(entradafinal, center_point, 10, cv.CV_RGB(0, 0, 255), 1)
		#imagen.ellipse((i[0]-aux, i[1]-aux, i[0]+aux, i[1]+aux), fill=(0,255,0))
		cv.PutText(entradafinal,("Pistola # "+str(contadodepisto)), (center_point),font, 255) #Draw the text
	return entradafinal
  
def mascara(image): 
    sobelx = ([-1,0,1],[-2,0,2],[-1,0,1])
    sobely = ([1,2,1],[0,0,0],[-1,-2,-1])
    img,gx,gy,minimo,maximo,conv=convolucion(sobelx,sobely,image)
    return img,gx,gy,minimo,maximo,conv
    
def convolucion(h1,h2,image): #Para deteccion de bordes con convolucion
    pixels = image.load()
    ancho,alto = image.size 
    a=len(h1[0])
    conv = np.empty((ancho, alto))
    gx=np.empty((ancho, alto))
    gy=np.empty((ancho, alto))
    minimo = 255
    maximo = 0
    for x in range(ancho):
        for y in range(alto):
            sumax = 0.0
            sumay = 0.0
            for i in range(a): 
                for j in range(a): 
                    try:
                        sumax +=(pixels[x+i,y+j][0]*h1[i][j])
                        sumay +=(pixels[x+i,y+j][0]*h2[i][j])

                    except:
                        pass
            gradiente = math.sqrt(pow(sumax,2)+pow(sumay,2))
            conv[x,y]=gradiente
            gx[x,y]=sumax
            gy[x,y]=sumay
            gradiente = int(gradiente)
            pixels[x,y] = (gradiente,gradiente,gradiente)
            p = gradiente
            if p <minimo:
                minimo = p
            if  p > maximo:
                maximo = p
    image.save('convo.png')
    return image,gx,gy,minimo,maximo,conv


def normalizar(image,minimo,maximo,conv): #normalizamos 
    pixels = image.load()
    r = maximo-minimo
    prop = 255.0/r
    ancho,alto = image.size
    for i in range(ancho):
        for j in range(alto):
            p =int(floor((conv[i,j]-minimo)*prop))
            pixels[i,j]=(p,p,p);

    return image

def binarizar(image): #binarizamos la imagen 
    pixels = image.load()
    ancho,alto = image.size
    minimo = int(argv[2])
    for i in range(ancho):
        for j in range(alto):
            if pixels[i,j][1] < minimo:
                p=0
            else:
                p= 255
            pixels[i,j]=(p,p,p)
    image.save('binarizar.png')
    return img


def filtro(image):
    image,matriz = escala_grises(image)
    pixels = image.load()
    ancho, alto =image.size
    lista = [-1,0,1]
    for i in range(ancho):
        for j in range(alto):
            promedio = vecindad(i,j,lista,matriz)
            pixels[i,j] = (promedio,promedio,promedio)
    image.save('filtrado.png')
    return image

def escala_grises(image):#escala de grises 
    image = Image.open(image) 
    pixels = image.load()
    ancho,alto = image.size
    matriz = np.empty((ancho, alto))
    for i in range(ancho):
        for j in range(alto):
            (r,g,b) = image.getpixel((i,j))
            escala = (r+g+b)/3
            pixels[i,j] = (escala,escala,escala)
            matriz[i,j] = int(escala)
    df = image.save('escaladegrises.png')
    return image,matriz 

    
def vecindad(i,j,lista,matriz):#filtrado
    promedio = 0
    indice  = 0
    for x in lista:
        for y in lista:
            a = i+x
            b = j+y
            try:
                if matriz[a,b] and (x!=a and y!=b):
                    promedio += matriz[a,b] 
                    indice +=1            
            except IndexError:
                pass
            try:
                promedio=int(promedio/indice)
                return promedio
            except ZeroDivisionError:
                return 0

def main():
    cam=cv.CaptureFromCAM(0)# captura la imagen de webcam con OpenCV
    while True:
        im =cv.QueryFrame(cam)#lanza la camara
        snapshot = im
        image_size = cv.GetSize(snapshot)
        cv.SaveImage("test.png",im)
        imagen=cv.CreateImage(image_size,cv.IPL_DEPTH_8U,3)
	snapshot = pistola(snapshot)
        detect_painting("test.png")
        snapshot = pistola(snapshot)
        cv.ShowImage('Camara', snapshot)
        if cv.WaitKey(30)==27:
            break
main()
