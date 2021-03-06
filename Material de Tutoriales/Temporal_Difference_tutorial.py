import numpy as np

# Damos nombre a los estados de un almacén con la siguiente forma:

#  L1   L2   L3
# -----
#  L4 | L5 | L6
#          -----
#  L7   L8   L9

location_to_state = {
    'L1' : 0,
    'L2' : 1,
    'L3' : 2,
    'L4' : 3,
    'L5' : 4,
    'L6' : 5,
    'L7' : 6,
    'L8' : 7,
    'L9' : 8
}
# Y creamos una lista para obtener el nombre de un estado dado su índice.
state_to_location = dict((state,location) for location,state in location_to_state.items())

# Definimos el conjunto de acciones. En nuestro caso la acción X consistirá en moverse al estado X.
actions = [0,1,2,3,4,5,6,7,8]

# Creamos la tabla de recompensas (recompensa por realizar una acción en un estado).
# en este caso no se opta por penalizar las acciones técnicamente imposibles, sino 
# recompensar ligeramente las posibles. Por lo tanto, el robot podría atravesar paredes.
# No hay estado meta definido de momento.
rewards = np.array([[0,1,0,0,0,0,0,0,0],
                    [1,0,1,0,1,0,0,0,0],
                    [0,1,0,0,0,1,0,0,0],
                    [0,0,0,0,0,0,1,0,0],
                    [0,1,0,0,0,0,0,1,0],
                    [0,0,1,0,0,0,0,0,0],
                    [0,0,0,1,0,0,0,1,0],
                    [0,0,0,0,1,0,1,0,1],
                    [0,0,0,0,0,0,0,1,0]])


# En este caso, se va un poco más allá, permitiendo indicar los estados de inicio y final en la propia función de entrenamiento.
def get_optimal_route(start_location, end_location):

    # Creamos la tabla de calidades con todo a 0
    Q = np.array(np.zeros([9,9]))

    # Definimos los parámetros de la función de calidad
    gamma = 0.75 # Será el factor de descuento, que determina la cantidad de peso que se le da al futuro lejano.
    alpha = 0.9 # Será la tasa de aprendizaje.

    # definimos el estado objetivo
    ending_state = location_to_state[end_location]

    # Creamos una copia de la tabla de recompensas
    rewards_copy = np.copy(rewards)

    # Actualizamos la tabla de recompensas con la recompensa del objetivo
    rewards_copy[ending_state,ending_state] = 999

    # --- ENTRENAMIENTO ---

    # Realizamos un número elevado de iteraciones para entrenar el agente
    for i in range(1000):
        # obtenemos un número de estado aleatorio
        current_state = np.random.randint(0,9)

        # Obtenemos las acciones con recompensa mayor a 0 desde ese estado
        playable_actions = []
        for j in range(9):
            if rewards_copy[current_state,j] > 0:
                playable_actions.append(j)
        # Y seleccionamos una de ellas al azar
        next_state = np.random.choice(playable_actions)

        # Actualizamos la tabla Q usando las funciones de Diferencia Temporal y ecuación de Bellman
        TD = rewards_copy[current_state,next_state] + gamma * Q[next_state, np.argmax(Q[next_state,])] - Q[current_state,next_state]
        Q[current_state,next_state] += alpha * TD

       # Ya estaría entrenado el algoritmo

    # --- Explotación ---

    # Se empieza la ruta en el estado inicial definido, y se inicializa la variable de "siguiente estado"
    route = [start_location]
    next_location = start_location
    # Se busca hasta llegar al final
    while(next_location != end_location):
        # se obtiene el estado inicial
        starting_state = location_to_state[start_location]
        # se busca el siguiente estado con mayor calidad
        next_state = np.argmax(Q[starting_state,])
        # se obtiene su nombre y añade a la ruta. 
        next_location = state_to_location[next_state]
        route.append(next_location)
        # se pasa a estar en el siguiente estado, y se repite el bucle.
        start_location = next_location
    # se devuelve la ruta de todos los estados por los que ha pasado.
    return route

# probamos a ejecutar el algoritmo, y vemos como recorre el camino más corto sin atravesar paredes
print(get_optimal_route("L1","L4"))
