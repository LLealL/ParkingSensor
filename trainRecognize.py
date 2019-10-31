from pysensor.localbinarypatterns import LocalBinaryPatterns
from sklearn.svm import LinearSVC
from imutils import paths
import argparse
import cv2
import os
import pickle

#construcao dos argumentos e parse de argumentos
ap = argparse.ArgumentParser()
ap.add_argument("-t","--training", required=True,
                help="Path para Imagens de Treinamento")
ap.add_argument("-e","--testing",required=True,
                help="Path para Imagens de Teste")
args=vars(ap.parse_args())

#Inicializa o descritor do LBP junto com as listas de dados e labels
desc = LocalBinaryPatterns(24,4)
data=[]
labels=[]

#loop nas imagens de treinamento
for imagePath in paths.list_images(args["training"]):
    #carrega a imagem e converte para escala de cinza e descreve ela
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    hist = desc.describe(gray)

    #extrai a label da imagem e atualiza as listas
    labels.append(imagePath.split(os.path.sep)[-2])
    data.append(hist)

#treina o Linear SVM nos dados
model= LinearSVC(C=100.0, random_state=42)

model.fit(data,labels)

#loop nas imagens de treinamento
for imagePath in paths.list_images(args["testing"]):
    #carrega a imagem e converte para escala de cinza, descreve e classifica
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    hist = desc.describe(gray)
    prediction = model.predict(hist.reshape(1, -1))

    #Mostra a imagem e a predição
    cv2.putText(image,prediction[0],(10,30),cv2.FONT_HERSHEY_SIMPLEX,1.0,(0,0,255),2)
    cv2.imshow("Image",image)
    cv2.waitKey(0)
    cv2.destroyWindow("Image")
    

pkl_filename= 'pickle_model.pkl'
with open(pkl_filename,'wb') as file:
    pickle.dump(model,file)
