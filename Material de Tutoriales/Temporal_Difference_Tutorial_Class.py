import numpy as np

# mismo código que antes, pero redefinido en una clase con varias funciones. Algo mejorado en 
# comparación al tutorial, eliminando variables innecesarias y usando las propias de la clase.
class QAgent():
    
    def __init__(self, alpha, gamma, location_to_state, state_to_location, actions, rewards, Q):
            
        self.gamma = gamma  
        self.alpha = alpha 

        self.location_to_state = location_to_state
        self.actions = actions
        self.rewards = rewards
        self.state_to_location = state_to_location

        self.Q = Q
        self.end_location = None

    # Función que entrena la tabla Q dado un objetivo
    def training(self, end_location, iterations):
        # definimos el estado objetivo
        self.end_location = end_location
        ending_state = self.location_to_state[end_location]

        # Creamos una copia de la tabla de recompensas
        rewards_copy = np.copy(self.rewards)

        # Actualizamos la tabla de recompensas con la recompensa del objetivo
        rewards_copy[ending_state,ending_state] = 999

        # --- ENTRENAMIENTO ---

        # Realizamos un número elevado de iteraciones para entrenar el agente
        for i in range(iterations):
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
            TD = rewards_copy[current_state,next_state] + self.gamma * self.Q[next_state, np.argmax(self.Q[next_state,])] - self.Q[current_state,next_state]
            self.Q[current_state,next_state] += self.alpha * TD

        # Ya estaría entrenado el algoritmo

    # Función que obtiene el camino óptimo de un punto al destino
    def get_optimal_route(self, start_location):

        # Se empieza la ruta en el estado inicial definido, y se inicializa la variable de "siguiente estado"
        route = [start_location]
        next_location = start_location
        # Se busca hasta llegar al final
        while(next_location != self.end_location):
            # se obtiene el estado inicial
            starting_state = self.location_to_state[start_location]
            # se busca el siguiente estado con mayor calidad
            next_state = np.argmax(self.Q[starting_state,])
            # se obtiene su nombre y añade a la ruta. 
            next_location = self.state_to_location[next_state]
            route.append(next_location)
            # se pasa a estar en el siguiente estado, y se repite el bucle.
            start_location = next_location
        # se devuelve la ruta de todos los estados por los que ha pasado.
        return route

# Definimos variables
alpha = 0.9
gamma = 0.75
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
state_to_location = dict((state,location) for location,state in location_to_state.items())
actions = [0,1,2,3,4,5,6,7,8]
rewards = np.array([[0,1,0,0,0,0,0,0,0],
                    [1,0,1,0,1,0,0,0,0],
                    [0,1,0,0,0,1,0,0,0],
                    [0,0,0,0,0,0,1,0,0],
                    [0,1,0,0,0,0,0,1,0],
                    [0,0,1,0,0,0,0,0,0],
                    [0,0,0,1,0,0,0,1,0],
                    [0,0,0,0,1,0,1,0,1],
                    [0,0,0,0,0,0,0,1,0]])
Q = np.array(np.zeros([9,9]))

# creamos un agente y lo ejecutamos, nos dará el mismo resultado que el otro archivo
qagent = QAgent(alpha, gamma, location_to_state, state_to_location, actions, rewards,  Q)
qagent.training('L4', 1000)
print(qagent.get_optimal_route('L1'))
