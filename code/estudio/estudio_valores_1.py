import matplotlib.pyplot as plt

from entorno_malware_estudio import Red
from agente_Q_estudio import AgenteMalware


def configura_experimentos():
    
    #lista que tendrá los parámetros de todos los 
    #experimentos en un diccionario cada uno
    experimentos = []
    
    # valores de tasa de aprendizaje
    alpha = [0.3, 0.5, 0.7, 0.9]
    # valores de tasa de descuento
    gamma = [0.2, 0.4, 0.8, 1.0]
    # valores de número de episodios
    episodes = [5, 50, 100, 200]
    # valores de qué grafos predefinidos utilizar
    graphs = [3, 4, 5]
    
    for a in alpha:
        for g in gamma:
            for e in episodes:
                for gr in graphs:
        
                    # guardamos los valores en un diccionario
                    exp = {}
                    exp["graph"] = gr
                    exp['alpha'] = a
                    exp['gamma'] = g
                    exp['episodes'] = e

                    experimentos.append(exp)

    return experimentos


# convierte el número de grafo predefinido en su correspondiente número de nodos
def get_nnodos(i):
    if i == 3:
        return "30"
    elif i == 4:
        return "300"
    elif i == 5:
        return "3000"
    return "0"


# Recibe una lista de diccionarios con los valores de los experimentos
# Guardará la ruta óptima encontrada en cada experimento y un log con
# las puntuaciones obtenidas después de cada episodio.
def ejecuta_experimentos(experimentos):

    rutas = []
    logs = []

    #recorre cada uno de los experimentos de la lista
    for exp in experimentos:
        # crea la red
        red = Red(predefinido=exp["graph"])
        # crea el agente
        agente = AgenteMalware(red)
        # entrena el agente
        Q, log = agente.entrena_agente(exp["alpha"], exp["gamma"], exp["episodes"])
        # obtiene la ruta óptima
        ruta, puntuacion = agente.busca_ruta()
        # guarda los resultados
        rutas.append(ruta)
        logs.append(log)
    
    return logs, rutas

# Dados unos parámetros de experimentos, y sus resultados, imprime sus valores
# por pantalla y crea una gráfica con la evolución de la puntuación
def visualiza_experimentos(experimentos, logs, rutas):
    
    # para cada experimento
    for exp, log, ruta in zip(experimentos, logs, rutas):
        
        # imprime sus valores y ruta óptima
        print("Parametros del experimento: ")
        print(exp)
        print("Ruta encontrada: ")
        print(ruta)
        
        # se crea un título para la gráfica y un nombre del archivo en el que se guardará
        titulo = "Nodes: " + get_nnodos(exp["graph"]) + ", Episodes: " + str(exp["episodes"]) + ", Alpha: " + str(exp["alpha"]) + ", Gamma: " + str(exp["gamma"])
        tituloArchivo = "N-" + get_nnodos(exp["graph"]) + "__Eps-" + str(exp["episodes"]) + "__A-" + str(exp["alpha"]) + "__G-" + str(exp["gamma"])
        
        fig, ax1 = plt.subplots()
    
        # Se representa la puntuación en cada episodio
        ax1.plot(log["episodio"], log["puntuacion"], "r-", label="Puntuación")
        ax1.set_xlabel("Episodio")
        ax1.set_ylabel("Recompensa") 
        ax1.set_title(titulo)
        ax1.legend(loc='lower right', frameon=True)
        
        #se guarda la gráfica
        plt.savefig(fname="./resultados_estudio_1/"+tituloArchivo+".png", format="png")


if __name__ == "__main__":
    
    experimentos = configura_experimentos()
    logs, rutas = ejecuta_experimentos(experimentos)
    visualiza_experimentos(experimentos, logs, rutas)