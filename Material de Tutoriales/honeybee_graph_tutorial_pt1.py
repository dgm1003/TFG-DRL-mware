import numpy as np
import pylab as plt
from honeybee_graph_functions import *

# creamos conexiones entre nodos, teniendo 8 nodos representados por los números del 0 al 7
points_list = [(0,1), (1,5), (5,6), (5,4), (1,2), (2,3), (2,7)]
# indicamos que la meta es el nodo 7, el cual consideramos una colmena de 
# abejas con miel (en este ejemplo el agente es un oso)
goal = 7

# representamos el grafo usando networkx
import networkx as nx
G=nx.Graph()
G.add_edges_from(points_list)
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G,pos)
nx.draw_networkx_edges(G,pos)
nx.draw_networkx_labels(G,pos)
plt.show()

# número de nodos
MATRIX_SIZE = 8

# creamos una matriz 8x8 con recompensa -1 para todos los caminos de un nodo a otro
R = np.matrix(np.ones(shape=(MATRIX_SIZE, MATRIX_SIZE)))
R *= -1

R = initialize_R(R, points_list, goal)

print("Matriz de recompensas:")
print(R)


#construimos la tabla Q, igual que en el archivo de Numpy_basic
Q = np.matrix(np.zeros([MATRIX_SIZE,MATRIX_SIZE]))

gamma = 0.8

initial_state = 1


available_act = available_actions(R, initial_state)
print(available_act)

action = sample_next_action(available_act)
print(action)

update_no_env(R, Q, initial_state, action, gamma)

# Entrenamos el modelo, también igual que en Numpy_basic, pero guardando las puntuaciones totales de cada ejecución
scores = []
for i in range(700):
    current_state = np.random.randint(0, int(Q.shape[0]))
    available_act = available_actions(R, current_state)
    action = sample_next_action(available_act)
    score, Q = update_no_env(R, Q, current_state,action,gamma)
    scores.append(score)
    print ('Score:', str(score))

print("Trained Q matrix:")
print(Q/np.max(Q)*100)

# Probamos el algoritmo, igual que en Numpy_basic.py
current_state = 0
steps = [current_state]

while current_state != 7:

    next_step_index = np.where(Q[current_state,]
        == np.max(Q[current_state,]))[1]

    if next_step_index.shape[0] > 1:
        next_step_index = int(np.random.choice(next_step_index, size = 1))
    else:
        next_step_index = int(next_step_index)

    steps.append(next_step_index)
    current_state = next_step_index

print("Most efficient path:")
print(steps)

# creamos una gráfica de como ha ido aumentando la puntuación a medida que progresaba el entrenamiento
plt.plot(scores)
plt.show()

# vemos como converge alrededor de los 300 updates