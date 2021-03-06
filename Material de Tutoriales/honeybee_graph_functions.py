import numpy as np
import pylab as plt
import networkx as nx

def initialize_R(R_mat, points_list, goal):
    # recorremos todos los caminos
    for point in points_list:
        print(point)
        # si el camino llega a la meta, le asignamos 100
        if point[1] == goal:
            R_mat[point] = 100
        # si no, le asignamos 0
        else:
            R_mat[point] = 0

        # si el camino sale de la meta, asignamos 100 a su inverso
        if point[0] == goal:
            R_mat[point[::-1]] = 100
        # si no, asignamos 0 a su inverso
        else:
            R_mat[point[::-1]]= 0

    # añadimos un camino de la meta a la meta con recompensa 100, para que se quede allí una vez alcanzada
    R_mat[goal,goal]= 100

    return R_mat

    
def available_actions(R, state):
    current_state_row = R[state,]
    av_act = np.where(current_state_row >= 0)[1]
    return av_act


def sample_next_action(available_actions_range):
    next_action = int(np.random.choice(available_actions_range,1))
    return next_action

def update_no_env(R, Q, current_state, action, gamma):

  max_index = np.where(Q[action,] == np.max(Q[action,]))[1]

  if max_index.shape[0] > 1:
      max_index = int(np.random.choice(max_index, size = 1))
  else:
      max_index = int(max_index)
  max_value = Q[action, max_index]

  Q[current_state, action] = R[current_state, action] + gamma * max_value
  print('max_value', R[current_state, action] + gamma * max_value)

  if (np.max(Q) > 0):
    return(np.sum(Q/np.max(Q)*100), Q)
  else:
    return (0, Q)


# función que, dado un destino, indica si tiene abejas, humo, o ambos
def collect_environmental_data(action, bees, smoke):
    found = []
    if action in bees:
        found.append('b')
    if action in smoke:
        found.append('s')
    return (found)

# función de actualización con variables de entorno
def update_env(R, Q, current_state, action, gamma, bees, smoke, enviro_bees, enviro_smoke):

    #en general es igual que el update normal
    max_index = np.where(Q[action,] == np.max(Q[action,]))[1]
    if max_index.shape[0] > 1:
        max_index = int(np.random.choice(max_index, size = 1))
    else:
        max_index = int(max_index)
    max_value = Q[action, max_index]

    Q[current_state, action] = R[current_state, action] + gamma * max_value
    print('max_value', R[current_state, action] + gamma * max_value)

    # si el destino tiene abejas o humo, actualiza sus respectivas tablas
    environment = collect_environmental_data(action, bees, smoke)
    if 'b' in environment:
        enviro_bees[current_state, action] += 1

    if 's' in environment:
        enviro_smoke[current_state, action] += 1

    if (np.max(Q) > 0):
        return(np.sum(Q/np.max(Q)*100))
    else:
        return (0)

#función de actualización con matriz conjunta de entorno
def update_env2(R, Q, current_state, action, gamma, bees, smoke, enviro_matrix):

    max_index = np.where(Q[action,] == np.max(Q[action,]))[1]

    if max_index.shape[0] > 1:
        max_index = int(np.random.choice(max_index, size = 1))
    else:
        max_index = int(max_index)
    max_value = Q[action, max_index]

    Q[current_state, action] = R[current_state, action] + gamma * max_value
    print('max_value', R[current_state, action] + gamma * max_value)

    environment = collect_environmental_data(action, bees, smoke)
    if 'b' in environment:
        enviro_matrix[current_state, action] += 1  # las abejas aumentan su valor
    if 's' in environment:
        enviro_matrix[current_state, action] -= 1  # el humo disminuye su valor

    return(np.sum(Q/np.max(Q)*100))

def available_actions_with_enviro_help(R, state, enviro_matrix):
    enviro_matrix_snap = enviro_matrix.copy()

    # obtenemos las acciones posibles
    current_state_row = R[state,]
    av_act = np.where(current_state_row >= 0)[1]

    # obtenemos la fila correspondiente de la matriz de entorno
    env_pos_row = enviro_matrix_snap[state,av_act]
    # si tiene alguna columna con valores negativos
    if (np.sum(env_pos_row < 0)):
        # seleccionamos solo aquellas acciones que no tengan recompensa negativa en la matriz de entorno
        temp_av_act = av_act[np.array(env_pos_row)[0]>=0]
        if len(temp_av_act) > 0:
            #imprimimos el cambio que ha ocurrido
            print('going from:',av_act)
            print('to:',temp_av_act)
            av_act = temp_av_act
    return av_act