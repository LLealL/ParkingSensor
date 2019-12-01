import cv2
import threading
import numpy as np
import queue
from threading import Thread
from pysensor.croprecognizer import CropRecognizer
from multiprocessing.pool import ThreadPool

def createRecognizerThread(myCrop):
    cropRec = CropRecognizer(crop=myCrop, cropId =0)
    result = cropRec.describe()
    return result

class Cropper():

    def __init__(self,frame,cameraId):
        Thread.__init__(self)
        self.frame=frame
        self.cameraId= cameraId

    def start(self):
        ratio = 600.0/self.frame.shape[1]
        dim = (600,int(self.frame.shape[0] *ratio))
        resized = cv2.resize(self.frame,dim,interpolation= cv2.INTER_AREA)

        rets = np.load("Camera"+str(self.cameraId)+"Coords.npy")
        print(rets)
        pool = ThreadPool(processes= len(rets))

        que = queue.Queue()
        results=[]
        i=0
        for r in rets:           
            i=i+1
            imCrop = resized[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
            thread = Thread(target= lambda q, arg1: q.put(createRecognizerThread(arg1)),args=(que,imCrop))
            thread.start()
            thread.join()
            result = que.get()
            lotID= "A"+str(i)
            data = {'id': lotID , 'blocked':result}
            results.append(data)
            
            print(result)

        return results
        
        
        
