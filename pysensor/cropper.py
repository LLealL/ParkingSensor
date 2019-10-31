import cv2
import threading
import numpy as np
import Queue
from threading import Thread
from croprecognizer import CropRecognizer
from multiprocessing.pool import ThreadPool

def createRecognizerThread(myCrop,myId):
    cropRec = CropRecognizer(crop=myCrop, cropId =myId)
    result = cropRec.describe()
    return result

class Cropper():

    def __init__(self,frame,cameraId):
        Thread.__init__(self)
        self.frame=frame
        self.cameraId= cameraId

    def start(self):
        ratio = 300.0/self.frame.shape[1]
        dim = (300,int(self.frame.shape[0] *ratio))
        resized = cv2.resize(self.frame,dim,interpolation= cv2.INTER_AREA)

        rets = np.load("Camera"+str(self.cameraId)+"Coords.npy")
        pool = ThreadPool(processes= len(rets))

        que = Queue.Queue()
        results=[]
        i=0
        for r in rets:
            i=i+1
            imCrop = resized[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
            thread = Thread(target= lambda q, arg1: q.put(createRecognizerThread(arg1)),args=(que,imCrop,i))
            thread.start()
            thread.join()
            result = que.get()
            results.append(result)
            
            print(result)

        return results
        
        
        
