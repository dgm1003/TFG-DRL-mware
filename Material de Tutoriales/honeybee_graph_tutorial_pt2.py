import numpy as np
import pylab as plt
import networkx as nx
from honeybee_graph_functions import *

# creamos conexiones entre nodos, teniendo 8 nodos representados por los números del 0 al 7
points_list = [(0,1), (1,5), (5,6), (5,4), (1,2), (2,3), (2,7)]
# indicamos que la meta (colmena) es el nodo 7
goal = 7

#indicamos casillas con abejas (están cerca de la colmena)
bees = [2]
#indicamos casillas con humo
smoke = [4,5,6]

def plot_node_graph():
    G=nx.Graph()
    G.add_edges_from(points_list)
    mapping={0:'Start', 1:'1', 2:'2 - Bees', 3:'3',
        4:'4 - Smoke', 5:'5 - Smoke', 6:'6 - Smoke', 7:'7 - Beehive'}
    H=nx.relabel_nodes(G,mapping)
    pos = nx.spring_layout(H)
    nx.draw_networkx_nodes(H,pos,
        node_size=[200,200,200,200,200,200,200,200])
    nx.draw_networkx_edges(H,pos)
    nx.draw_networkx_labels(H,pos)
    plt.show()

plot_node_graph()

# número de nodos
MATRIX_SIZE = 8

# creamos una matriz 8x8 con recompensa -1 para todos los caminos de un nodo a otro
R = np.matrix(np.ones(shape=(MATRIX_SIZE, MATRIX_SIZE)))
R *= -1

R = initialize_R(R, points_list, goal)

print(R)

# re-initialize the matrices for new run
Q = np.matrix(np.zeros([MATRIX_SIZE,MATRIX_SIZE]))

enviro_bees = np.matrix(np.zeros([MATRIX_SIZE,MATRIX_SIZE]))
enviro_smoke = np.matrix(np.zeros([MATRIX_SIZE,MATRIX_SIZE]))

gamma = 0.8

initial_state = 1

#entrenamos el algoritmo igual que en la parte 1
scores = []
for i in range(700):
    current_state = np.random.randint(0, int(Q.shape[0]))
    available_act = available_actions(R, current_state)
    action = sample_next_action(available_act)
    score = update_env(R, Q, current_state,action,gamma, bees, smoke, enviro_bees, enviro_smoke)

# imprimimos las nuevas matrices
print('Bees Found')
print(enviro_bees)
print('Smoke Found')
print(enviro_smoke)


# ahora, despues de estudiar la red, descubrimos que las abejas 
# indican que la meta está mas cerca, y el humo indica lo contrario, 
# así que le damos una recompensa positiva a las abejas y una negativa al humo
enviro_matrix = enviro_bees - enviro_smoke

# Entrenamos el modelo con las variables de entorno
scores = []
for i in range(700):
    current_state = np.random.randint(0, int(Q.shape[0]))
    available_act = available_actions_with_enviro_help(R, current_state, enviro_matrix)
    action = sample_next_action(available_act)
    score = update_env2(R, Q, current_state,action,gamma, bees, smoke, enviro_matrix)
    scores.append(score)
    print ('Score:', str(score))

plt.plot(scores)
plt.show()

# podemos ver como el entrenamiento converge mucho más rápido (100-200 updates)
# que en la parte 1 que no usaba más datos del entorno

