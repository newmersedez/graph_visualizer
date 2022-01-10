from algorithms.dijkstra import *
import random

def dijkstra_algo_for_tsp(graph: Graph, vertex: Vertex):
    checked_nodes = {}
    prev_node_and_edge = {}
    ranges_to_nodes = {}
    for i in graph.getVertexList():
        checked_nodes[i] = False
        ranges_to_nodes[i] = None
    ranges_to_nodes[vertex]: int = 0
    prev_node_and_edge[vertex] = None
    nodes_to_visit = Queue()
    nodes_to_visit.put(vertex)
    while nodes_to_visit.qsize() > 0:
        checking_node: Vertex = nodes_to_visit.get()
        reachable_edges = [i for i in checking_node.getAdjacentEdgeList()
                           if (i.getStartVertex() == checking_node or not i.isDirected())]

        reachable_edges = sorted(reachable_edges, key=(lambda x: int(x.getWeight())))
        for i in reachable_edges:
            tmp_range_from_node = ranges_to_nodes[checking_node]  # inf == None
            tmp_end_node = get_end_node(checking_node, i)
            x = i.getWeight()
            if not tmp_end_node:
                continue
            if ranges_to_nodes[tmp_end_node] is None:
                ranges_to_nodes[tmp_end_node] = tmp_range_from_node + i.getWeight()
                prev_node_and_edge[tmp_end_node] = (checking_node, i)
            elif ranges_to_nodes[tmp_end_node] > tmp_range_from_node + i.getWeight():
                ranges_to_nodes[tmp_end_node] = tmp_range_from_node + i.getWeight()
                prev_node_and_edge[tmp_end_node] = (checking_node, i)
            if not checked_nodes[tmp_end_node]:
                nodes_to_visit.put(tmp_end_node)
        checked_nodes[checking_node] = True
    names = [i.getName() for i in ranges_to_nodes.keys()]
    ranges = [i for i in ranges_to_nodes.values()]
    # print(names)
    # print(ranges)
    #
    # print([i.getName() for i in prev_node_and_edge.keys()])
    # print_list = [(
    #     i[0].getName(),
    #     i[1][0].getName() if i[1] is not None else None,
    #     i[1][1].getName()  if i[1] is not None else None)
    #         for i in [(j, prev_node_and_edge[j]) for j in prev_node_and_edge.keys()]]
    # print([f"node: {i[0]}, prev_node: {i[1]}, edge_number: {i[2]}" for i in print_list])
    return ranges_to_nodes, prev_node_and_edge


# возвращает словарь, тип ключа - кортеж из двух вершин, обозначающих виртуальное ребро, а значение - вес виртуального ребра
# ranges_to_all_nodes - словарь, вершина -> словарь расстояний от заданной вершины до всех остальных

def createDijkstraForAllNodes(graph: Graph):
    all_prev_node_and_edge = {}
    ranges_to_all_nodes = {}
    for i in graph.getVertexList():
        tmp1, tmp2 = dijkstra_algo_for_tsp(graph, i)
        all_prev_node_and_edge[i] = tmp2
        ranges_to_all_nodes[i] = tmp1
    return ranges_to_all_nodes, all_prev_node_and_edge

def getAllVirtualPath(graph: Graph, all_prev_node_and_edge):
    all_path = {}
    for i in graph.getVertexList():
        prev_node_and_edge = all_prev_node_and_edge[i]
        all_path[i] = {}
        for j in graph.getVertexList():
            if i == j:
                all_path[i][j] = None
                continue
            tmp_list = []
            begin_node_and_edge = prev_node_and_edge[j]
            while begin_node_and_edge is not None:
                previous_node = begin_node_and_edge[0]
                edge_from_previous_to_current = begin_node_and_edge[1]
                tmp_list.append(edge_from_previous_to_current)
                begin_node_and_edge = prev_node_and_edge[previous_node]
            all_path[i][j] = tmp_list
    return all_path


def getNodesInVirtualPath(all_path):
    nodes_in_path = {}
    for i in all_path.keys():
        nodes_in_path[i] = {}
        for j in all_path[i].keys():
            tmp_nodes = set()
            for k in all_path[i][j]:
                tmp_nodes.add(k.getStartVertex())
                tmp_nodes.add(k.getEndVertex())
            nodes_in_path[i][j] = tmp_nodes
    return nodes_in_path




# ВЕРОЯТНОСТЬ ПОПАСТЬ В ВЕРШИНУ
# P(i, j) = tau(i, j)^alpha * mu(i, j)^beta / sum(tau(i, k)^alpha * mu(i, k)^beta для всех допустимых k)

#   tau - количество феромона на ребре, mu - вес ребра, (i, j) - ребро, k - муравей,
#   alpha beta - const, больше альфа - больше влияние феромонов, больше бета - больше влияние веса вершин

# ИЗМЕНЕНИЕ ФЕРОМОНА НА РЕБРЕ МУРАВЬЕМ k НА ИТЕРАЦИИ t
# d( tau(i, j, k, t)) = Q / L(k, t), если (i, j) in Path(k, t)

# (i, j) - ребро, k - муравей, t - номер итерации,
# Path(k, t) - множество ребер, по которым прошелся k-ый муравей на итерации T, L(k, t)
# L(k, t) - общая длина Path(k, t)
# Q - const, влияет на то, насколько много феромонов появляется, ставить в зависимости от весов вершин

# ОБЩЕЕ КОЛИЧЕСТВО ФЕРОМОНОВ НА РЕБРЕ ПОСЛЕ ПРОХОЖДЕНИЯ ИТЕРАЦИИ t
# tau(i, j, t + 1) = tau(i, j, t) * p + sum(d( tau(i, j, k, t) для всех допустимых k)
# p - const, коэффициент испарения, чем он меньше - тем быстрее испаряется весь предыдущий феромон


# t - максимальное количество итераций



class   antsAlgo:
    def __init__(self, graph: Graph, begin_vertex: Vertex):

        # получение данных о графе и его виртуальном дополнении
        self.rangeMatrix, tmp_all_path = createDijkstraForAllNodes(graph)
        self.allPath = getAllVirtualPath(tmp_all_path)
        self.nodesInPath = getNodesInVirtualPath(self.allPath)
        self.begin_vertex = begin_vertex
        self.graph = graph
        self.vertex_number = len(self.graph.getVertexList())

        # константы
        self.alpha = 1.0 # степень важности феромона
        self.beta = 4.0 # cтепень важности веса ребра
        self.Q = 4.0 # коэффициент количества феромонов на путь
        self.P = 0.7 # Скорость испарения феромона
        self.T_MAX = 1000 # максимальное количество итераций
        self.begin_pheromones = 0.5 # начальное количество феромонов на ребрах
        self.antsCount = 50 # количество муравьев


        # иные необходимые для работы алгоритма вещи
        self.pheromones = {}
        for i in graph.getVertexList():
            self.pheromones[i] = {}
            for j in graph.getVertexList():
                self.pheromones[i][j] = self.begin_pheromones


        # результат алгоритма
        self.bestPath = None
        self.bestLen = None

    def getAllPForPath(self, vertex_from, visited_nodes):
        all_prob = {}
        sum_probs = 0.0
        for curr in self.graph.getVertexList():
            if curr == vertex_from or curr in visited_nodes:
                all_prob[curr] = None
                continue
            all_prob[curr] = self.pheromones[vertex_from][curr] ** self.alpha * \
                             self.rangeMatrix[vertex_from][curr] ** self.beta
            sum_probs += all_prob[curr]
        for curr in all_prob.keys():
            if all_prob[curr] is not None:
                all_prob[curr] /= sum_probs
        return all_prob

    def get_random_node_from_current(self, current, visited_nodes):
        all_random = self.getAllPForPath(self, current, visited_nodes)
        rand_number = random.uniform(0, 1)
        tmp_sum_of_probs = 0
        key_number = 0
        node = all_random.keys()[0]
        while rand_number > tmp_sum_of_probs and key_number < len(all_random.keys()):
            node = all_random.keys()[key_number]
            tmp_sum_of_probs += all_random[node]
        return node

    def algoIter(self, t):
        antsPaths = {} # ant_number -> (path, len_of_path), path is list of vertex
        for i in range(self.antsCount):
            curr_node = self.begin_vertex
            path = [self.begin_vertex]
            len = 0
            visited_nodes = set()
            while len(visited_nodes) != self.vertex_number:
                rand_node = self.get_random_node_from_current(curr_node, visited_nodes)
                path.append(rand_node)
                visited_nodes.update(self.nodesInPath[curr_node][rand_node])













