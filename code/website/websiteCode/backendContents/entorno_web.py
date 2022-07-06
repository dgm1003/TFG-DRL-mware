import random

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


class Red():

    def __init__(self, NNODOS=30, inicial=17, meta=15, seed=None, ratio_riesgo=0.25, predefinido=0):

        # guardamos el número de nodos 
        self.NNODOS = NNODOS

        # definimos la lista de acciones (puramente informativo de momento, no se utiliza)
        self.acciones = list(range(0, self.NNODOS+1))

        if predefinido > 0 and predefinido < 5:
            self.genera_predefinido(predefinido, ratio_riesgo)
        else:
            # generamos el grafo
            self.grafo = nx.random_internet_as_graph(self.NNODOS, seed)

            # seleccionamos al azar un porcentaje de los nodos como nodos de alto riesgo
            dict_riesgos = {}
            for i in range(self.NNODOS):
                if random.random() < ratio_riesgo:
                    dict_riesgos[i] = {"riesgo" : 10}
                else:
                    dict_riesgos[i] = {"riesgo" : 1}

            #definimos el estado inicial (lo guardamos aparte también para poder resetear el entorno) y la meta
            self.inicial = inicial
            self.estado = inicial
            self.meta = meta

            # guardamos los riesgos de los nodos
            nx.set_node_attributes(self.grafo, dict_riesgos)
        
        # guardamos si están infectados o no los nodos (empiezan todos sin infectar), y
        # el color y grosor de los nodos y conexiones en el renderizado. 
        nx.set_node_attributes(self.grafo, False, "infectado")
        nx.set_node_attributes(self.grafo, 'cyan', 'color')
        nx.set_edge_attributes(self.grafo, 'black', 'color')
        nx.set_edge_attributes(self.grafo, 1, 'grosor')
        
        # se seleccionan colores diferentes para los nodos de inicio y fin
        self.grafo.nodes[self.meta]['color'] = 'yellow'
        self.grafo.nodes[self.inicial]['color'] = 'blue'

        # definimos un tiempo límite para llegar al objetivo
        self.tiempo_limite = 1000
    
    
    def genera_predefinido(self, predefinido, ratio_riesgo):
        self.grafo = nx.Graph()

        if predefinido == 1:
            self.NNODOS = 9
            self.meta=5
            self.inicial=7
            self.estado=7
            conexiones = [(0,1), (1,2), (1,3), (2,4), (2,5), (3,6), (3,7), (3,8)]
            self.grafo.add_edges_from(conexiones)
            lista_riesgo = [6]
            # Reiniciamos los riesgos de los nodos
            for i in range(self.NNODOS):
                self.grafo.nodes[i]["riesgo"] = 1

            # Asignamos los nuevos riesgos
            for i in lista_riesgo:
                self.grafo.nodes[i]["riesgo"] = 10
        
        elif predefinido == 2:
            self.NNODOS=30
            self.meta=15
            self.inicial=17
            self.estado=17
            self.grafo = nx.random_internet_as_graph(self.NNODOS, seed=123456)
            lista_riesgo = [1,4,5,7,8]
            # Reiniciamos los riesgos de los nodos
            for i in range(self.NNODOS):
                self.grafo.nodes[i]["riesgo"] = 1

            # Asignamos los nuevos riesgos
            for i in lista_riesgo:
                self.grafo.nodes[i]["riesgo"] = 10
            
        elif predefinido == 3:
            self.NNODOS=30
            self.meta=15
            self.inicial=17
            self.estado=17
            self.grafo = nx.random_internet_as_graph(self.NNODOS, seed=123456)
            lista_riesgo = [0,1,4,5,8]
            # Reiniciamos los riesgos de los nodos
            for i in range(self.NNODOS):
                self.grafo.nodes[i]["riesgo"] = 1

            # Asignamos los nuevos riesgos
            for i in lista_riesgo:
                self.grafo.nodes[i]["riesgo"] = 10
            
        elif predefinido == 4:
            self.NNODOS=100
            self.meta=65
            self.inicial=66
            self.estado=66
            self.grafo = nx.random_internet_as_graph(self.NNODOS, seed=12345678)
            # seleccionamos al azar un porcentaje de los nodos como nodos de alto riesgo
            dict_riesgos = {}
            random.seed(12345678)
            for i in range(self.NNODOS):
                if random.random() < ratio_riesgo:
                    dict_riesgos[i] = {"riesgo" : 10}
                else:
                    dict_riesgos[i] = {"riesgo" : 1}

            nx.set_node_attributes(self.grafo, dict_riesgos)
        
    #método que se ejecuta cada vez que se aplica una acción
    def step(self, accion):

        # Pasa 1 segundo en el reloj
        self.tiempo_limite -= 1 
        
        # Calculamos la recompensa
        recompensa = self.obtener_recompensa(self.estado, accion)
        
        # si la acción es infectar (la definimos como NNODOS, es decir, un número que no corresponde 
        # a un nodo), infectamos. También actualizamos el color del nodo para que lo refleje
        if accion == self.NNODOS:
            self.grafo.nodes[self.estado]['infectado'] = True
            self.grafo.nodes[self.estado]['color'] = 'red'
        # si no, omprobamos que existe la conexión y cambiamos el estado
        # además de los colores de la conexión por la que ha viajado y el nodo que ha visitado
        elif self.grafo.has_edge(self.estado, accion):
            self.grafo.edges[self.estado, accion]['color'] = 'red'
            self.grafo.edges[self.estado, accion]['grosor'] = 3
            self.estado = accion
            self.grafo.nodes[self.estado]['color'] = 'green'
        
        # Comprobamos que no se haya llegado al final del episodio
        if ( self.tiempo_limite <= 0 or
            (self.estado == self.meta and self.grafo.nodes[self.estado]['infectado'] == True) ): 
            finalizado = True
        else:
            finalizado = False
        
        # Devolvemos los datos
        return self.estado, recompensa, finalizado,
    
    
    #método que se ejecuta para probar la aplicación de una acción sobre un estado
    def step_prueba(self, estado, accion):

        # Calculamos la recompensa
        recompensa = self.obtener_recompensa(estado, accion)

        # actualizamos el estado en el que se quedaría el agente al realizar la acción
        if accion != self.NNODOS and self.grafo.has_edge(estado, accion):
            estado = accion
        
        # Devolvemos los datos
        return estado, recompensa

    
    # Método que obtiene la recompensa de una acción
    # 
    # Parámetros:
    #  - actual: estado actual
    #  - siguiente: acción a realizar (número de nodo a moverse o NNODOS para infectar)
    # Return: la recompensa de dicha acción partiendo de dicho estado
    def obtener_recompensa(self, actual, siguiente):

        # si se está infectando al nodo actual
        if(siguiente == self.NNODOS):
            # si el nodo actual es el objetivo, devuelve la máxima recompensa
            if(actual == self.meta):
                return 999
            # en caso contrario, penaliza la acción
            return -5

        # si se mantiene en el estado actual
        if(actual == siguiente):
            # si está en el estado objetivo, devuelve la máxima recompensa
            if(actual == self.meta and self.grafo.nodes[actual]['infectado'] == True):
                return 999
            # en caso contrario, penalización de -1 al haber pasado el tiempo
            return -1
        
        # si se mueve por una conexión válida
        if( self.grafo.has_edge(actual, siguiente) ):
            # si el destino aporta poca información, se penaliza ligeramente
            if(self.grafo.degree(siguiente)==1):
                return -3
            # en caso contrario, devolvemos el riesgo del nodo (el riesgo mínimo 
            # será 1, equivalente a la penalización por tiempo)
            return - self.grafo.nodes[siguiente]["riesgo"]

        # si no es ninguno de los casos anteriores, penalización máxima al ser un movimiento imposible.
        return -111
    
    # Método que obtiene los estados a los que se puede llegar desde el estado actual
    # 
    # Parámetros:
    #  - actual: el estado actual
    # Return:
    #  - acciones: las acciones posibles desde ese estado
    def get_posibles_acciones(self, actual):

        # incluimos los nodos a los que puede llegar desde el actual
        acciones = [a for a in self.grafo[actual]]
        # si es un estado no infectado, añadimos la acción de infectarlo
        if self.grafo.nodes[actual]['infectado'] == False: acciones.append(self.NNODOS)

        return acciones

    def get_infectado(self, estado):
        return self.grafo.nodes[estado]['infectado']

    # Método que muestra una representación del entorno
    #
    # Leyenda:
    #   Conexiones:
    #    - negro: no recorrida
    #    - verde: recorrida
    #   Nodos:
    #    - azul claro: no visitado
    #    - azul oscuro: nodo de inicio
    #    - amarillo: nodo objetivo
    #    - verde: nodo visitado
    #    - rojo: nodo infectado
    def render(self):

        # obtenemos los colores y grosores de los nodos y conexiones
        mapa_colores_nodos = nx.get_node_attributes(self.grafo,'color').values()
        mapa_colores_caminos = nx.get_edge_attributes(self.grafo,'color').values()
        mapa_grosores_caminos = list(nx.get_edge_attributes(self.grafo,'grosor').values())

        # seleccionamos una layout para la impresión
        pos = nx.spring_layout(self.grafo)
        # dibujamos los nodos y conexiones
        nx.draw_networkx_nodes(self.grafo,pos, node_color=mapa_colores_nodos)
        nx.draw_networkx_edges(self.grafo,pos, edge_color=mapa_colores_caminos, width=mapa_grosores_caminos)
        nx.draw_networkx_labels(self.grafo,pos)
        plt.savefig("./static/images/network.png")
    
    
    def reset(self):
        # Reiniciamos las variables a sus valores iniciales
        self.estado = self.inicial
        
        # reiniciamos los atributos de los nodos y conexiones
        nx.set_node_attributes(self.grafo, False, "infectado")
        nx.set_node_attributes(self.grafo, 'cyan', 'color')
        nx.set_edge_attributes(self.grafo, 'black', 'color')
        nx.set_edge_attributes(self.grafo, 'grosor', 1)
        self.grafo.nodes[self.meta]['color'] = 'yellow'
        self.grafo.nodes[self.inicial]['color'] = 'blue'

        self.tiempo_limite = 1000
        return self.estado
