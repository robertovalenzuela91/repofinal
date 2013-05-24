import cv
from PIL import Image, ImageDraw,ImageFont

def pistola(entrada):

        storage = cv.CreateMemStorage()
        cv.EqualizeHist(grayscale, grayscale)
	cascade2=cv.Load("pistoladetect.xml")
        pistola = cv.HaarDetectObjects(grayscale, cascade2, storage, 1.1, 2, 0, ( 120, 120))
	if pistola:
            # Vamos cara por cara
	    contadodepisto=0
            for i in pistola:
                # Dibujamos figuras en cara
		contadodepisto+=1
                cv.Rectangle(entrada, ( i[0][0], i[0][1]), ((i[0][0] + i[0][2]), (i[0][1] + i[0][2])), cv.RGB(0, 255, 0),10, 8, 0)
                center_point = ((i[0][0]*2 + i[0][2])/2, (i[0][1]*2 + i[0][2])/2 )
                cv.Circle(entrada, center_point, 10, cv.CV_RGB(0, 0, 255), 1)
		#imagen.ellipse((i[0]-aux, i[1]-aux, i[0]+aux, i[1]+aux), fill=(0,255,0))
		cv.PutText(entrada,("Pistola # "+str(contadodepisto)), (center_point),font, 255) #Draw the text
	return entrada

cam=cv.CaptureFromCAM(0)
while True:
 im =cv.QueryFrame(cam)
 snapshot = im
 image_size = cv.GetSize(snapshot)
 # La transformamos a escala de grises para mayor rapidez
 grayscale = cv.CreateImage((image_size),snapshot.depth,1)
 cv.CvtColor(snapshot, grayscale, cv.CV_RGB2GRAY)
 font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 0, 1) #Creates a font
 snapshot = pistola(snapshot)
 cv.ShowImage('Camara', snapshot)
        
 if cv.WaitKey(30)==27:
  break
