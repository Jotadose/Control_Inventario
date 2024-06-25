from sklearn.linear_model import LinearRegression
import numpy as np

class PrediccionDemanda:
    def __init__(self):
        self.model = LinearRegression()
        self.is_trained = False

    def entrenar(self, datos_x, datos_y):
        X = np.array(datos_x).reshape(-1, 1)
        y = np.array(datos_y)
        self.model.fit(X, y)
        self.is_trained = True

    def predecir(self, datos):
        if not self.is_trained:
            raise Exception("El modelo no ha sido entrenado. Por favor, llame al método 'entrenar' primero.")
        X = np.array(datos).reshape(-1, 1)
        return self.model.predict(X)[0]
