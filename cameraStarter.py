import numpy as np
import cv2
import math
from pysensor.croprecognizer import CropRecognizer



cap = cv2.VideoCapture(0)

frameRate = cap.get(600)

while(cap.isOpened()):
    frameId =cap.get(1)
    
    ret,frame= cap.read()

    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray = cv2.flip(gray,1)

    filename="captura.jpg"
    if(frameId % math.floor(frameRate)==0):
        cv2.imwrite(filename, frame)
     #   recognizer = CropRecognizer(crop= frame, id= frameId)
      #  print(recognizer.describe())
    

    cv2.imshow('frame',gray)
    if cv2.waitKey(2000) & 0xFF ==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

