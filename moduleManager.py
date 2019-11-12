import cv2
import numpy as np
import argparse
from pysensor.cropper import Cropper
from kafkaModule.myKafkaProducer import KProducer


def getCropperResults(camFrame,camId):
    print("creating cropper")
    cropper = Cropper(frame= camFrame, cameraId=camId)
    results = cropper.start()
    return results

def initProducer(server):

    if server:
        prod = KProducer(servers = server)
    else:
        prod = KProducer()
    return prod

def initCamera():
    cap = cv2.VideoCapture(0)
    return cap

def drawLots(frame):
    rets = np.load("Camera0Coords.npy")
    for r in rets:
        frame = cv2.rectangle(frame, (int(r[0]),int(r[1])) , (int(r[0])+int(r[2]),int(r[1])+int(r[3])), (255,0,0), 2)
    return frame

def jsonMaker(results):
    return results


def main():


    ap = argparse.ArgumentParser()
    ap.add_argument("-s","--server", required=False,
                    help="Server Bootstrap do kafka")
    ap.add_argument("-t","--topic", required=True,
                    help="Topico para ser usado no kafka")
    
    args = vars(ap.parse_args())
    
    
    producer=initProducer(args["server"])
    cam = initCamera()
    if producer:
        if cam:
          while(cam.isOpened()):
             # cv2.waitKey(8000)
              ret,img = cam.read()
              gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
              gray = cv2.flip(img,1)
              print("frame captured")
              ratio = 400.0/ img.shape[1]
              dim = (400, int(img.shape[0] *ratio))

              resized = cv2.resize(img,dim,interpolation= cv2.INTER_AREA)
              cv2.imshow("image",drawLots(resized))
              results = getCropperResults(gray,0)
              if results:
                  print("printing results")
                  print(results)
                #  producer.sendData(data=results, topic=args["topic"])
              print(results)
             
              if cv2.waitKey(10000) & 0xFF ==ord('q'):
                  break;
    cap.release()
    cv2.destroyAllWindows()
    

if __name__== "__main__":
    main()
