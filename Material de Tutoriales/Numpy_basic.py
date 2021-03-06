import numpy as np

# matriz de recompensas
# esta matriz indicará la recompensa de ir de un estado a otro.

# Podemos decir que  hay 6 estados, numerados del 0 al 5, de modo que cada
# fila represente el estado de inicio y cada columna el estado de destino.
# Así, por ejemplo, la tercera columna de la primera fila consistirá en 
# la recompensa de pasar del "estado 0" al "estado 2" 
R = np.matrix([ 
        	[-1,-1,-1,-1, 0, -1],
		[-1,-1,-1, 0,-1,100],
		[-1,-1,-1, 0,-1, -1],
		[-1, 0, 0,-1, 0, -1],
		[-1, 0, 0,-1,-1,100],
		[-1, 0,-1,-1, 0,100] ])

# Tabla Q, con la calidad de cada una de las acciones en cada uno de los estados
# En este ejemplo consideramos 6 acciones por cada estado, y cada acción nos moverá
# a su estado correspondiente (acción 4 llevará al estado 4)
Q = np.matrix(np.zeros([6,6]))

# Tasa de aprendizaje
gamma = 0.8

# Estado inicial (normalmente se elegiría aleatoriamente)
initial_state = 1

# Esta función nos devolverá todas las acciones con recompensa positiva, dado un estado
def available_actions(state):
    current_state_row = R[state,]
    av_act = np.where(current_state_row >= 0)[1]
    return av_act

# Probamos el método
available_act = available_actions(initial_state) 
print("Acciones disponibles desde el estado {}: {}".format(initial_state,available_act))


# función que selecciona una acción al azar de aquellas que no resultarán en recompensa negativa
def sample_next_action(available_actions_range):
    next_action = int(np.random.choice(available_act,1))
    return next_action

# Ejemplo de uso:
action = sample_next_action(available_act)
print("Acción seleccionada: {}".format(action))


# Función que actualiza la tabla Q dado un estado y una acción
def update(current_state, action, gamma):
    
    # obtiene la acción con calidad máxima del estado 
    # al que se llegaría con la acción seleccionada
    max_index = np.where(Q[action,] == np.max(Q[action,]))[1]

    #si hay varias con calidad máxima, selecciona una al azar
    if max_index.shape[0] > 1:
        max_index = int(np.random.choice(max_index, size = 1))
    else:
        max_index = int(max_index)
    # obtiene el valor de calidad máximo dado esa acción 
    max_value = Q[action, max_index]
    
    # actualiza la tabla Q, usando la fórmula Q
    Q[current_state, action] = R[current_state, action] + gamma * max_value

# Ejemplo de uso
print("Q antes de actualizar")
print(Q)
update(initial_state,action,gamma)
print("Q después de actualizar")
print(Q)


#-------------------------------------------------------------------------------
# ENTRENAMIENTO

# Entrenamos la tabla Q mediante 10000 iteraciones de los pasos anteriores
# (seleccionamos estado y acción aleatoria, actualizamos la tabla)
for i in range(10000):
    current_state = np.random.randint(0, int(Q.shape[0]))
    available_act = available_actions(current_state)
    action = sample_next_action(available_act)
    update(current_state,action,gamma)
    
# Normalizamos los valores para que estén entre 0 y 100
print("Tabla Q entrenada:")
print(Q/np.max(Q)*100)

#-------------------------------------------------------------------------------
# ENTRENAMIENTO

# Estado de destino = 5
# Mejor secuencia empezando en el estado 2 -> 2, 3, 1, 5

current_state = 2 # empezamos en el estado 2
steps = [current_state] # creamos una lista de pasos

while current_state != 5: # hasta que llegue al destino:

    # obtenemos la acción con calidad máxima (si hay varias se elige una al azar)
    next_step_index = np.where(Q[current_state,] == np.max(Q[current_state,]))[1]
    
    if next_step_index.shape[0] > 1:
        next_step_index = int(np.random.choice(next_step_index, size = 1))
    else:
        next_step_index = int(next_step_index)
    
    # pasamos al estado al que lleva dicha acción y lo guardamos en la lista de pasos
    steps.append(next_step_index)
    current_state = next_step_index

# Imprimimos la secuencia de pasos
print("Camino seleccionado:")
print(steps)

#-------------------------------------------------------------------------------
#                               OUTPUT ESPERADO
#-------------------------------------------------------------------------------
#
# Tabla Q entrenada:
#[[   0.     0.     0.     0.    80.     0. ]
# [   0.     0.     0.    64.     0.   100. ]
# [   0.     0.     0.    64.     0.     0. ]
# [   0.    80.    51.2    0.    80.     0. ]
# [   0.    80.    51.2    0.     0.   100. ]
# [   0.    80.     0.     0.    80.   100. ]]
#
# Camino seleccionado:
# [2, 3, 1, 5]
# """
