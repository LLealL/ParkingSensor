import pickle
import cv2
from pysensor.localbinarypatterns import LocalBinaryPatterns
from threading import Thread

class CropRecognizer():
    def __init__(self,crop,cropId):
        Thread.__init__(self)
        self.crop=crop
        self.id=cropId

    def describe(self):
        pickle_filename = "pickle_model.pkl"
        desc = LocalBinaryPatterns(24,4)
        with open(pickle_filename, 'rb') as file:
            pickle_model = pickle.load(file)
            image = cv2.cvtColor(self.crop,cv2.COLOR_BGR2GRAY)
            hist = desc.describe(image)
            prediction = pickle_model.predict(hist.reshape(1,-1))

            if prediction[0]=="Livre":
                return False;
            else:
                return True;

        
        



    
