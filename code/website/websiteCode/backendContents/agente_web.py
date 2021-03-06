import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from entorno_malware import Red

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
        self.inicio = red.inicial
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

        for e in range(episodios):
            # reiniciamos las variables del episodio
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

        #normalizamos la tabla Q
        self.Q = self.Q/np.max(self.Q)
        
        return self.Q


    # Método que, una vez entrenado el modelo, encuentra la ruta más corta hasta la meta desde 
    # el nodo definido como inicial en el entorno.
    # 
    # Return:
    #  - ruta: lista con los nodos por los que pasa
    #  - puntuacion: recompensa total del camino
    def busca_ruta(self, render=False):

        # inicializamos el vector en el que se guardará la ruta, la puntuación, y 
        # los estados intermedios que usaremos al buscar el camino
        ruta = [self.inicio]
        estado_actual = self.red.reset()
        accion = self.NNODOS
        puntuacion = 0
        terminado = False
        # hasta llegar a la meta
        while(not terminado):
            # buscamos la acción con mayor calidad
            accion = np.argmax(self.Q[estado_actual,])
            # realizamos la acción
            estado_actual, recompensa, terminado = self.red.step(accion)
            if render:
                self.red.render()
            # actualizamos la puntuación y la ruta
            puntuacion += recompensa
            ruta.append(accion)

        return ruta, puntuacion
        


'''# --- Uso del algoritmo: ---

# guardamos el número de nodos
NNODOS = 30

# declaramos los nodos de inicio y fin
meta = 15
inicio = 17

# creamos la red de ordenadores
red = Red(NNODOS, inicio, meta, seed=123456)
#red = Red(predefinido=4)
G = red.grafo
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G,pos)
nx.draw_networkx_edges(G,pos)
nx.draw_networkx_labels(G,pos)
plt.show()

# creamos el agente
agente = AgenteMalware(red)


# definimos el factor de descuento y la tasa de aprendizaje respectivamente
gamma = 0.7
alpha = 0.9

# entrenamos el agente con 5 episodios
print("Tabla de calidades (normalizada): ")
print(agente.entrena_agente(alpha, gamma, 50))

# obtenemos la ruta óptima
ruta, puntuacion = agente.busca_ruta(render=False)

print("Ruta:")
print(ruta)
print("Puntuación:")
print(puntuacion)'''
