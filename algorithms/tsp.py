from algorithms.dijkstra import *
import random
from algorithms.connected import *


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
            tmp_list.reverse()
            all_path[i][j] = tmp_list
    return all_path


def getNodesInVirtualPath(all_path):
    nodes_in_path = {}
    for i in all_path.keys():
        nodes_in_path[i] = {}
        for j in all_path[i].keys():
            if i != j:
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


class antsAlgo:
    def __init__(self, graph: Graph, begin_vertex: Vertex):

        # получение данных о графе и его виртуальном дополнении
        self.rangeMatrix, tmp_all_path = createDijkstraForAllNodes(graph)
        self.allPath = getAllVirtualPath(graph, tmp_all_path)
        self.nodesInPath = getNodesInVirtualPath(self.allPath)
        self.begin_vertex = begin_vertex
        self.graph = graph
        self.vertex_number = len(self.graph.getVertexList())

        # константы
        self.alpha = 1.0  # степень важности феромона
        self.beta = 4.0  # cтепень важности веса ребра
        self.Q = 4.0  # коэффициент количества феромонов на путь
        self.P = 0.7  # Скорость испарения феромона
        self.T_MAX = 800  # максимальное количество итераций
        self.begin_pheromones = 0.5  # начальное количество феромонов на ребрах
        self.antsCount = 30  # количество муравьев

        # иные необходимые для работы алгоритма вещи
        self.pheromones = {}
        for i in graph.getVertexList():
            self.pheromones[i] = {}
            for j in graph.getVertexList():
                if i != j:
                    self.pheromones[i][j] = self.begin_pheromones

        # результат алгоритма
        self.bestPath = None
        self.bestLen = None

    def getAllPForPath(self, vertex_from, visited_nodes):
        all_prob = {}
        sum_probs = 0.0
        for curr in self.graph.getVertexList():
            if curr == vertex_from or curr in visited_nodes:
                continue
            all_prob[curr] = self.pheromones[vertex_from][curr] ** self.alpha * \
                             self.rangeMatrix[vertex_from][curr] ** self.beta
            sum_probs += all_prob[curr]
        for curr in all_prob.keys():
            if all_prob[curr] is not None:
                all_prob[curr] /= sum_probs
        return all_prob

    def get_random_node_from_current(self, current, visited_nodes):
        all_random = self.getAllPForPath(current, visited_nodes)
        rand_number = random.uniform(0, 1)
        tmp_sum_of_probs = 0
        key_number = 0
        node = list(all_random.keys())[0]
        while rand_number > tmp_sum_of_probs and key_number < len(all_random.keys()):
            node = list(all_random.keys())[key_number]
            tmp_sum_of_probs += all_random[node]
        return node

    def calcutaleNewPheromoneOnPath(self, anstPaths):
        for i in self.pheromones.keys():
            for j in self.pheromones.keys():
                if i != j:
                    self.pheromones[i][j] *= self.P

        for path_info in anstPaths.values():
            path = path_info[0]
            len_of_path = path_info[1]
            for i in range(len(path) - 1):
                begin_node = path[i]
                end_node = path[i + 1]
                self.pheromones[begin_node][end_node] += self.Q / len_of_path
                self.pheromones[end_node][begin_node] += self.Q / len_of_path

    def algoIter(self, t):
        antsPaths = {}  # ant_number -> (path, len_of_path), path is list of vertex
        for i in range(self.antsCount):
            curr_node = self.begin_vertex
            path = [self.begin_vertex]
            len_of_path = 0
            visited_nodes = {self.begin_vertex}
            while len(visited_nodes) != self.vertex_number:
                rand_node = self.get_random_node_from_current(curr_node, visited_nodes)
                path.append(rand_node)
                len_of_path += self.rangeMatrix[curr_node][rand_node]
                visited_nodes.update(self.nodesInPath[curr_node][rand_node])
                curr_node = rand_node
            path.append(self.begin_vertex)
            len_of_path += self.rangeMatrix[curr_node][self.begin_vertex]
            if self.bestLen is None or self.bestLen < len_of_path:
                self.bestPath = path
                self.bestLen = len_of_path
            antsPaths[i] = (path, len_of_path)
        self.calcutaleNewPheromoneOnPath(antsPaths)

    def pathToEdgePath(self):
        edges = []
        for i in range(len(self.bestPath) - 1):
            begin_node = self.bestPath[i]
            end_node = self.bestPath[i + 1]
            for edge in self.allPath[begin_node][end_node]:
                edges.append(edge)
        return edges

    def all_algo(self):
        for i in range(self.T_MAX):
            self.algoIter(i)
        all_path = self.pathToEdgePath()
        print([i.getName() for i in all_path])
        return all_path


def tspCheckGraph(graph: Graph, vertex: Vertex):
    for i in graph.getEdgeList():
        if i.isDirected():
            return False
    a = isConnected(graph)
    for i in a.values():
        if i > 1:
            return False
    a = {}
    for i in graph.getEdgeList():
        if i.getStartVertex() in a and a[i.getStartVertex()] == i.getEndVertex() or \
                i.getEndVertex() in a and a[i.getEndVertex()] == i.getStartVertex():
            return False
        a[i.getStartVertex()] = i.getEndVertex()
        a[i.getEndVertex()] = i.getStartVertex()

    return True


def setVisualForTSP(graph: Graph, vertex: Vertex):
    a = antsAlgo(graph, vertex)
    path = a.all_algo()
    for i in path:
        i.setColor(QtCore.Qt.green)
    return path, sum([i.getWeight() for i in path])
