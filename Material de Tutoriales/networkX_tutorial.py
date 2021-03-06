import networkx as nx
#import pylab as plt
import matplotlib.pyplot as plt


## función para visualizar los grafos en caso de que sea necesario.
## las llamadas a esta función se dejan comentadas, para no abrir demasiados plots si se ejecutase
def imprime(g):
    pos = nx.spring_layout(g)
    nx.draw_networkx_nodes(g,pos)
    nx.draw_networkx_edges(g,pos)
    nx.draw_networkx_labels(g,pos)
    plt.show()

## PARTE 01: CREAR UN GRAFO -----------------------------------------------------------------

## los grafos se crean con el siguiente método:
G = nx.Graph()


## PARTE 02: NODOS --------------------------------------------------------------------------

## se pueden añadir nodos de uno en uno
G.add_node(0)
## o varios a la vez
G.add_nodes_from([2,3])
## también se pueden añadir como tupla (nodo, opciones)
G.add_nodes_from([
            (4, {'color':'red'}),
            (5, {"color":"green"})
])
#imprime(G)

## creamos dos copias de G para mostrar las diferencias
G2 = G.copy()
G3 = G.copy()

## creamos un grafo linear con 10 nodos
H = nx.path_graph(10)

## se pueden añadir los nodos de otro grafo
G2.add_nodes_from(H)
#imprime(G2)

## o añadir el propio grafo como nodo
G3.add_node(H)
#imprime(G3)

## esto es debido a que un nodo en networkX puede ser cualquier tipo de objeto, no solo números.


## PARTE 03: ARISTAS -----------------------------------------------------------------------
print("--- PARTE 03")

## las aristas se pueden añadir indicando dos nodos
G.add_edge(0,2)
## o pasándolos como un objeto (el * es para acceder al contenido de e)
e = (2,3)
G.add_edge(*e)

## igual que los nodos, se pueden añadir varios a la vez
G.add_edges_from([(0, 4), (0, 5)])
#imprime(G)

## e incluso añadir las aristas de otro grafo
G2.add_edges_from(H.edges)
#imprime(G2)

## si reseteamos el grafo, y añadimos nodos y aristas varias veces, veremos
## como no hay problema, y si ya están en el grafo los ignora
G.clear()
#imprime(G)
G.add_edges_from([(1, 2), (1, 3)])
#imprime(G)
G.add_node(1)
#imprime(G)
G.add_edge(1, 2)
#imprime(G)
G.add_node("spam")        # añade un nodo de contenido "spam"
#imprime(G)
G.add_nodes_from("spam")  # añade 4 nodos: 's', 'p', 'a', 'm'
#imprime(G)
G.add_edge(3, 'm')
#imprime(G)

## podemos consultar el número de nodos y aristas de esta forma
print("nº nodos: {}, nº aristas: {}".format(G.number_of_nodes(), G.number_of_edges()))


## PARTE 04: EXAMINAR ELEMENTOS DE UN GRAFO -------------------------------------------------
print("--- PARTE 04")

print("lista de nodos del grafo: {}".format(list(G.nodes)))
print("lista de aristas del grafo: {}".format(list(G.edges)))
print("lista de nodos conectados al nodo 1: {}".format(list(G.adj[1])))
print("número de aristas que salen del nodo 1: {}".format(G.degree[1]))
print("lista de aristas conectados a los nodos 2 y m: {}".format(G.edges([2, 'm'])))
print("número de aristas que salen de los nodos 2 y 3 (el formato es \"(nodo, grado)\" ): {}".format(G.degree([2, 3])))

## PARTE 05: ELIMINAR ELEMENTOS DE UN GRAFO -------------------------------------------------
print("--- PARTE 05")

## ya hemos visto el método clear(), pero se pueden eliminar nodos y aristas concretos
## de uno en uno
G.remove_node(2)
G.remove_edge(1, 3)
## o varios a la vez
G.remove_nodes_from("spam")

## no habrá ninguna arista pues al eliminar un nodo se eliminan 
## también todas las aristas que conectan con él
print("Nodos y aristas después de borrar 2, s, p, a, m, y el arista 1-3 :")
print(list(G.nodes))
print(list(G.edges))

G.add_edge(1, 2)

## PARTE 06: CONSTRUCTORES DE GRAFOS --------------------------------------------------------
print("--- PARTE 06")

## creamos un grafo direccional con los nodos y aristas de G
H = nx.DiGraph(G)
#imprime(H)

## Se pueden crear grafos directamente mediante listas de aristas
edgelist = [(0, 1), (1, 2), (2, 3)]
H = nx.Graph(edgelist)
print("lista de aristas del grafo H (debería ser [(0, 1), (1, 2), (2, 3)] ): {}".format(list(H.edges)))
#imprime(H)

## También se pueden crear dando los nodos adyacentes a cada nodo
adjacency_dict = {0: (1, 2), 1: (0, 2), 2: (0, 1)}
H = nx.Graph(adjacency_dict)
#imprime(H)
print("lista de aristas del grafo H (debería ser [(0, 1), (0, 2), (1, 2)] ): {}".format(list(H.edges)))

## PARTE 07: ACCEDER A ARISTAS Y VECINOS ----------------------------------------------------
print("--- PARTE 07")

## podemos asignar un objeto a cada arista del siguiente modo:
G = nx.Graph([(1, 2, {"color": "yellow"})])
## y accederemos a los nodos adyacentes a un nodo, junto con la
## información de sus aristas, del siguiente modo:
print("nodos adyacentes al nodo 1: {}".format(G[1]))
print("nodos adyacentes al nodo 1: {}".format(G.adj[1]))

## podemos acceder a los datos de una arista de estas formas:
print("Información de la arista 1-2: {}".format(G[1][2]))
print("Información de la arista 1-2: {}".format(G.edges[1,2]))

## también podemos añadir o cambiar los datos de una arista existente como si fuese un diccionario:
G.add_edge(1, 3)
G[1][3]['color'] = "blue"
print("Información de la arista 1-3: {}".format(G[1][3]))
G.edges[1, 2]['color'] = "red"
print("Información de la arista 1-3: {}".format(G[1][2]))

## podemos iterar por las aristas de un grafo rápidamente con G.adj.items() o G.adjacency
FG = nx.Graph()
FG.add_weighted_edges_from([(1, 2, 0.125), (1, 3, 0.75), (2, 4, 1.2), (3, 4, 0.375)])
#imprime(FG)
## n = nodo origen,  nbrs = nodos destino e información aristas 
for n, nbrs in FG.adj.items():
    ## nbr = nodo destino,  eattr = información arista
    for nbr, eattr in nbrs.items():
        wt = eattr['weight']
        ## imprime el peso si es menor de 0.5. Como el grafo no es 
        ## dirigido, lo hará dos veces para cada arista
        if wt < 0.5: print(f"({n}, {nbr}, {wt:.3})")

print("-")
## también se puede acceder a un atributo concreto con G.edges
for (u, v, wt) in FG.edges.data('weight'):
    if wt < 0.5:
        ## esta vez no se imprimirán dos veces
        print(f"({u}, {v}, {wt:.3})")


## PARTE 08: AÑADIR ATRIBUTOS A GRAFOS, NODOS O ARISTAS -------------------------------------
print("--- PARTE 08")

## se pueden añadir atributos al crear un grafo
G = nx.Graph(day="Friday")
print(G.graph)

## o una vez creado, como si fuese un diccionario
G.graph['day'] = "Monday"
print(G.graph)

## es igual con nodos
G.add_node(1, time='5pm')
G.add_nodes_from([3], time='2pm')
print(G.nodes[1])
G.nodes[1]['room'] = 714
## pero podemos acceder a sus datos con .nodes.data
print(G.nodes.data())

## y lo mismo para aristas
G.add_edge(1, 2, weight=4.7 )
G.add_edges_from([(3, 4), (4, 5)], color='red') # se añade a ambos
G.add_edges_from([(1, 2, {'color': 'blue'}), (2, 3, {'weight': 8})])
print(G.edges.data())
G[1][2]['weight'] = 4.7
G.edges[3, 4]['weight'] = 4.2
print(G.edges.data())


## PARTE 09: GRAFOS DIRIGIDOS ---------------------------------------------------------------
print("--- PARTE 09")

## creamos grafos dirigidos como vimos antes
DG = nx.DiGraph()

## al añadir aristas, el primer nodo será el de origen
DG.add_weighted_edges_from([(1, 2, 0.5), (3, 1, 0.75)])
#imprime(DG)

## obtenemos la suma de pesos de las aristas que salen del nodo 1
print(DG.out_degree(1, weight='weight'))
## obtenemos la suma de pesos de todas las aristas conectadas al nodo 1
print(DG.degree(1, weight='weight'))
## sin embargo vemos como G.neighbors en este caso será igual a los sucesores, y no a todos los nodos
print(list(DG.predecessors(1)))
print(list(DG.successors(1)))
print(list(DG.neighbors(1)))


## PARTE 10: MULTIGRAFOS --------------------------------------------------------------------
print("--- PARTE 10")

## los multigrafos permitirán más de una conexión entre dos mismos nodos
MG = nx.MultiGraph()
MG.add_weighted_edges_from([(1, 2, 0.5), (1, 2, 0.75), (2, 3, 0.5)])
#imprime(MG)

print(dict(MG.degree(weight='weight')))

## creamos un grafo similar, pero en caso de que haya más de dos aristas
## entre dos nodos se seleccionará la de menor peso
GG = nx.Graph()
for n, nbrs in MG.adjacency():
   for nbr, edict in nbrs.items():
       minvalue = min([d['weight'] for d in edict.values()])
       GG.add_edge(n, nbr, weight = minvalue)

## esta función encuentra el camino más corto, con opción de 
## tener en cuenta los pesos, puede ser útil en el trabajo
print(nx.shortest_path(GG, 1, 3))


## PARTE 11: GENERADORES DE GRAFOS ----------------------------------------------------------
print("--- PARTE 11")

## solamente se prueban los generadores de gráficos que pueden ser útiles en el trabajo
K_5 = nx.complete_graph(5)
#imprime(K_5)
K_3_5 = nx.complete_bipartite_graph(3, 5)
#imprime(K_3_5)
barbell = nx.barbell_graph(10, 10)
#imprime(barbell)
lollipop = nx.lollipop_graph(10, 20)
#imprime(lollipop)
tree = nx.balanced_tree(2, 3)
#imprime(tree)
tree2 = nx.binomial_tree(3)
#imprime(tree2)

'''
balanced_tree(r, h[, create_using]) - Returns the perfectly balanced r-ary tree of height h.
barbell_graph(m1, m2[, create_using]) - Returns the Barbell Graph: two complete graphs connected by a path.
binomial_tree(n[, create_using]) - Returns the Binomial Tree of order n.
complete_graph(n[, create_using]) - Return the complete graph K_n with n nodes.
complete_multipartite_graph(*subset_sizes) - Returns the complete multipartite graph with the specified subset sizes.
circular_ladder_graph(n[, create_using]) - Returns the circular ladder graph CL(n) of length n.
circulant_graph(n, offsets[, create_using]) - Returns the circulant graph Ci(n) with n nodes.
cycle_graph(n[, create_using]) - Returns the cycle graph C(n) of cyclically connected nodes.
dorogovtsev_goltsev_mendes_graph(n[, ...]) - Returns the hierarchically constructed Dorogovtsev-Goltsev-Mendes graph.
empty_graph([n, create_using, default]) - Returns the empty graph with n nodes and zero edges.
full_rary_tree(r, n[, create_using]) - Creates a full r-ary tree of n nodes.
ladder_graph(n[, create_using]) - Returns the Ladder graph of length n.
lollipop_graph(m, n[, create_using]) - Returns the Lollipop Graph; K_m connected to P_n.
null_graph([create_using]) - Returns the Null graph with no nodes or edges.
path_graph(n[, create_using]) - Returns the Path graph P_n of linearly connected nodes.
star_graph(n[, create_using]) - Return the star graph
trivial_graph([create_using]) - Return the Trivial graph with one node (with label 0) and no edges.
turan_graph(n, r) - Return the Turan Graph
wheel_graph(n[, create_using]) - Return the wheel graph
'''


## PARTE 12: ANÁLISIS DE GRAFOS -------------------------------------------------------------
print("--- PARTE 12")

G = nx.Graph()
G.add_edges_from([(1, 2), (1, 3)])
G.add_node("spam")  # añade un nodo "spam"

## agrupa los nodos dependiendo de si están conectados entre sí
print(list(nx.connected_components(G)))
G.remove_edge(1,3)
print(list(nx.connected_components(G)))
G.add_edge(1,3)

## podemos ordenar los grados de los nodos
print(G.degree())
print(sorted(d for n, d in G.degree()))

## esta función indicará el número posible de triángulos que se pueden formar que pasen por el nodo
print(nx.clustering(G))
G.add_edge(2,3)
print(nx.clustering(G))
G.remove_edge(2,3)

## también, como ejemplo de otra función más compleja, podemos obtener todos los 
## caminos más cortos desde todos los nodos hasta todos los nodos
sp = dict(nx.all_pairs_shortest_path(G))
## se ha guardado en un diccionario para acceder fácilmente a los datos
print(f"Caminos más cortos con el nodo 3 como origen: {sp[3]}")


## PARTE 13: DIBUJO DE GRAFOS ---------------------------------------------------------------

G = nx.petersen_graph()
subax1 = plt.subplot(121)
## dibujamos los nodos sin especificar posición
nx.draw(G, with_labels=True, font_weight='bold')
subax2 = plt.subplot(122)
## dibujamos el grafo en estilo caparazón, con los 5 primeros nodos en un anillo y los 5 siguientes en otro
nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
plt.show()

## también podemos pasar las opciones por parámetro
options = {
    'node_color': 'black',
    'node_size': 100,
    'width': 3,
}
subax1 = plt.subplot(221)
nx.draw_random(G, **options)
subax2 = plt.subplot(222)
nx.draw_circular(G, **options)
subax3 = plt.subplot(223)
nx.draw_spectral(G, **options)
subax4 = plt.subplot(224)
nx.draw_kamada_kawai(G, **options)
plt.show()

## en el caso de draw_shells, podemos especificar qué nodos poner en cada anillo
G = nx.dodecahedral_graph()
shells = [[2, 3, 4, 5, 6], [8, 1, 0, 19, 18, 17, 16, 15, 14, 7], [9, 10, 11, 12, 13]]
nx.draw_shell(G, nlist=shells, **options)
plt.show()