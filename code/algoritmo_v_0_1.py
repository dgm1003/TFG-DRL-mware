from string import punctuation
import numpy as np
import pylab as plt

# Versión inicial del algoritmo, utilizando tablas de recompensa y calidad.
#
# NUEVO: estructura de clases
#
# Author: Diego García Muñoz

class AgenteMalware():

    # constructor, se le pasarán las configuraciones sobre la red de ordenadores
    # 
    # Parámetros:
    #  - conexiones: las conexiones entre los nodos
    #  - lista_sin_valor: lista de nodos hoja que no ofrecen información
    #  - lista_alto_riesgo: lista de nodos con seguridad alta
    #  - NNODOS: número total de nodos
    def __init__(self, conexiones, lista_sin_valor, lista_alto_riesgo, NNODOS):
        self.conexiones = conexiones
        self.lista_sin_valor = lista_sin_valor
        self.lista_alto_riesgo = lista_alto_riesgo
        self.NNODOS = NNODOS
        
        self.R = np.matrix(np.ones(shape=(self.NNODOS*2, self.NNODOS*2)))
        self.Q = np.matrix(np.zeros([self.NNODOS*2,self.NNODOS*2]))
    

    # Método que inicializa la tabla de recompensas con los valores correctos
    # 
    # Parámetros:
    #  - meta: nodo objetivo
    # Return:
    #  - R: tabla de recompensas
    def inicializa_recompensas(self, meta):
        self.meta = meta

        # creamos una matriz de recompensas con el doble del número de nodos como 
        # dimensiones (cada nodo podrá estar sin infectar o infectado)
        self.R = np.matrix(np.ones(shape=(self.NNODOS*2, self.NNODOS*2)))
        self.R *= -111

        # recorremos la lista de conexiones
        for conex in self.conexiones:
            # damos recompensa -1 al camino entre 2 nodos, simulando la penalización por cada unidad de tiempo
            self.R[conex] = -1
            self.R[conex[::-1]] = -1
            # también damos esa recompensa si el nodo inicio está infectado y viaja a otro no infectado
            self.R[conex[0]+self.NNODOS,conex[1]] = -1
            self.R[conex[1]+self.NNODOS,conex[0]] = -1

        # definimos la recompensa de infectar un nodo no objetivo
        for i in range(self.NNODOS):
            self.R[i, i+self.NNODOS] = -5

        # actualizamos las recompensas de visitar nodos con poca información
        for nodo in self.lista_sin_valor:
            for i in range(self.NNODOS*2):
                if self.R[i,nodo] == -1:
                    self.R[i,nodo] = -3
                    
        # actualizamos las recompensas de visitar nodos con mucho riesgo
        for nodo in self.lista_alto_riesgo:
            for i in range(self.NNODOS):
                if self.R[i,nodo] == -1:
                    self.R[i,nodo] = -10

        # definimos la recompensa por infectar el nodo objetivo
        self.R[meta, meta+self.NNODOS] = 999

        # por último, definimos la recompensa para quedarse en un nodo cualquiera
        for i in range(self.NNODOS*2):
            self.R[i, i] = -1
        self.R[meta+self.NNODOS,meta+self.NNODOS]= 999

        return self.R


    # Método que entrena al agente rellenando la tabla de calidades
    # 
    # Parámetros:
    #  - alpha: tasa de aprendizaje
    #  - gamma: factor de descuento
    # Return:
    #  - Q: tabla de calidades
    def entrena_agente(self, alpha, gamma):
        # --- ENTRENAMIENTO ---
        for i in range(1000):
            # obtenemos un nodo al azar (esté infectado o no)
            actual = np.random.randint(0,self.NNODOS*2-1)

            # obtenemos las acciones que tiene permitido tomar (aquellas con recompensa mayor que -111)
            posibles_acciones = []
            for j in range(self.NNODOS*2):
                if self.R[actual,j] > -100:
                    posibles_acciones.append(j)
            # de las acciones posibles, seleccionamos una al azar
            siguiente = np.random.choice(posibles_acciones)

            # actualizamos el valor de la celda correspondiente con la función de diferencia temporal
            self.Q[actual,siguiente] += alpha * self.R[actual,siguiente] +  gamma * \
                                        self.Q[siguiente, np.argmax(self.Q[siguiente,])] - self.Q[actual,siguiente]

        #normalizamos la tabla Q
        self.Q = self.Q/np.max(self.Q)
        
        return self.Q


    # Método que, una vez entrenado el modelo, encuentra la ruta más corta hasta la meta desde un nodo cualquiera.
    # 
    # Parámetros:
    #  - inicio: nodo de salida
    # Return:
    #  - ruta: lista con los nodos por los que pasa
    #  - puntuacion: recompensa total del camino
    def busca_ruta(self, inicio):
        # --- BÚSQUEDA DE RUTA ---
        # declaramos la posición final de la tabla
        metaReal=self.meta+self.NNODOS

        # inicializamos el vector en el que se guardará la ruta, la puntuación, y 
        # los estados intermedios que usaremos al buscar el camino
        ruta = [inicio]
        estado_actual = inicio
        siguiente_estado = estado_actual
        puntuacion = 0
        # hasta llegar a la meta
        while(estado_actual != metaReal):
            # buscamos la acción con mayor calidad
            siguiente_estado = np.argmax(self.Q[estado_actual,])
            # actualizamos la puntuación y la ruta
            puntuacion += self.R[estado_actual,siguiente_estado]
            ruta.append(siguiente_estado)
            # realizamos dicha acción
            estado_actual = siguiente_estado

        return ruta, puntuacion
        



# definición de las conexiones entre dispositivos
# 
#       0
#       |
#       1
#       |
#   ---------
#   |       |
#   2       3
#   |       |
# -----  -------
# |   |  |  |  |
# 4   5  6  7  8
conexiones = [(0,1), (1,2), (1,3), (2,4), (2,5), (3,6), (3,7), (3,8)]

# indicamos los dispositivos que solo están conectados a un único 
# dispositivo y por lo tanto no nos aportan información
lista_sin_valor = [4,8]

# indicamos los dispositivos con alto nivel de seguridad
lista_alto_riesgo = [6]

# guardamos el número de nodos
NNODOS = 9

# creamos el agente
agente = AgenteMalware(conexiones, lista_sin_valor, lista_alto_riesgo, NNODOS)

# definimos el nodo objetivo
meta = 5

# rellenamos la tabla de recompensas
print("Tabla de recompensas")
print(agente.inicializa_recompensas(meta))

# definimos el factor de descuento y la tasa de aprendizaje respectivamente
gamma = 0.7
alpha = 0.9

# entrenamos el agente
print("Tabla de calidades (normalizada)")
print(agente.entrena_agente(alpha, gamma))

# declaramos el nodo de inicio
inicio = 7

# obtenemos la ruta óptima
ruta, puntuacion = agente.busca_ruta(inicio)

print("Ruta:")
print(ruta)
print("Puntuación:")
print(puntuacion)