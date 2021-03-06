import numpy as np


# Versión del algoritmo utilizando tablas de calidad. 
# Con estructura de clases y usando una clase de entorno.
# 
# NUEVO: entrena mediante estructura de episodios.
#
# Author: Diego García Muñoz

class AgenteMalware():

    # constructor, se le pasarán la red de ordenadores
    # 
    # Parámetros:
    #  - red: red de ordenadores del tipo de objeto GrafoRed
    def __init__(self, red):
        np.set_printoptions(suppress=True)
        self.red = red
        self.NNODOS = self.red.NNODOS
        self.Q = np.matrix(np.zeros([self.NNODOS,self.NNODOS+1]))
    

    # Método que entrena al agente rellenando la tabla de calidades
    # 
    # Parámetros:
    #  - alpha: tasa de aprendizaje
    #  - gamma: factor de descuento
    #  - episodios: número de episodios del entrenamiento
    # Return:
    #  - Q: tabla de calidades
    def entrena_agente(self, alpha, gamma, episodios):
        
        log = {"episodio": [], "puntuacion": []}

        for e in range(episodios):
            # reiniciamos las variables del episodio
            log["episodio"].append(e)
            actual = self.red.reset()
            accion = self.NNODOS
            terminado = False
            # hasta llegar a la meta
            while(not terminado):
                # de las acciones posibles, seleccionamos una al azar
                accion = np.random.choice(self.red.get_posibles_acciones(actual))
                # realizamos la acción
                estado, recompensa, terminado = self.red.step(accion)
                # actualizamos el valor de la celda correspondiente con la función de diferencia temporal
                self.Q[actual,accion] += alpha * recompensa +  gamma * \
                                            self.Q[estado, np.argmax(self.Q[estado,])] - self.Q[actual,accion]
                # actualizamos el estado actual
                actual = estado
            
            ruta, puntuacion = self.busca_ruta()
            log["puntuacion"].append(puntuacion)

        #normalizamos la tabla Q
        self.Q = self.Q/np.max([np.max(self.Q), 0.0001])
        
        return self.Q, log

    # Método que, una vez entrenado el modelo, encuentra la ruta más corta hasta la meta desde 
    # el nodo definido como inicial en el entorno.
    # 
    # Return:
    #  - ruta: lista con los nodos por los que pasa
    #  - puntuacion: recompensa total del camino
    def busca_ruta(self, render=False):

        # inicializamos el vector en el que se guardará la ruta, la puntuación, y 
        # los estados intermedios que usaremos al buscar el camino
        ruta = [self.red.inicial]
        estado_actual = self.red.reset()
        accion = self.NNODOS
        max_iter = self.NNODOS/2
        iteracion = 0
        puntuacion = 0
        terminado = False
        # hasta llegar a la meta
        while(not terminado and iteracion < max_iter):
            # buscamos la acción con mayor calidad
            accion = np.argmax(self.Q[estado_actual,])
            # realizamos la acción
            estado_actual, recompensa, terminado = self.red.step(accion)
            if render:
                self.red.render()
            # actualizamos la puntuación y la ruta
            puntuacion += recompensa
            ruta.append(accion)
            iteracion += 1 

        return ruta, puntuacion
        
