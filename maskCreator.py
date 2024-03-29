import cv2
import numpy as np
import argparse


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--id", required=True, help= "Camera Id")
ap.add_argument("-f", "--frame", required=True, help="Arquivo do frame de camera")

args=vars(ap.parse_args())


image = cv2.imread(args["frame"])
image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

coordsFile= "Camera"+str(args["id"]) + "Coords"

print(np.load(coordsFile+ ".npy"))

ratio = 600.0/ image.shape[1]
dim = (600, int(image.shape[0] *ratio))

resized = cv2.resize(image,dim,interpolation= cv2.INTER_AREA)

rets=[]

while(True):

    k=cv2.waitKey(0)

    if k==27:
        cv2.destroyAllWindows()
        break
    r = cv2.selectROI(resized)
    if r[1]==0 | r[2]==0 | r[3]==0 | r[0]==0:
        continue    
    rets.append(r)

    print(r)

print(rets)
np.save(coordsFile,rets)
