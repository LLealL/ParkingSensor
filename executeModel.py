import pickle
import argparse
import cv2
import os
from pysensor.localbinarypatterns import LocalBinaryPatterns
from imutils import paths

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--pickle" , required=True, help ="Pickle model treinado")
ap.add_argument("-e", "--testing", required=True, help ="Path para predict")

args=vars(ap.parse_args())

desc = LocalBinaryPatterns(24,4)

print(args["pickle"])

with open(args["pickle"], 'rb') as file:
    pickle_model = pickle.load(file)
    for imagePath in paths.list_images(args["testing"]):
        image = cv2.imread(imagePath)
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        hist = desc.describe(gray)
        prediction= pickle_model.predict(hist.reshape(1,-1))

        print(prediction[0])
        cv2.putText(image,prediction[0],(10,30),cv2.FONT_HERSHEY_SIMPLEX,1.0,(0,0,255),2)
        cv2.imshow("Image",image)
        cv2.waitKey(0)
        cv2.destroyWindow("Image")
