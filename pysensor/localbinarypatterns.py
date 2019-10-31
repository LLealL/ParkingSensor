from skimage import feature
import numpy as np

class LocalBinaryPatterns:
    def __init__(self,numPoints,radius):
        #guardar numeros de pontos e raios
        self.numPoints=numPoints
        self.radius=radius

    def describe(self, image, eps=1e-7):
        #computa a representacao do Local Binary Pattern
        #da imagem e usa a representacao LBP para
        #construir o histograma de padroes

        lbp = feature.local_binary_pattern(image,self.numPoints,self.radius, method="uniform")
        (hist, _) = np.histogram(lbp.ravel(),bins=np.arange(0, self.numPoints + 3), range=(0, self.numPoints +2))

        #normaliza o histograma
        hist = hist.astype("float")
        hist /= (hist.sum()+eps)

        #retorna histograma do LBP
        return hist
