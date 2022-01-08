import itertools
from algorithms.colorize import *
from algorithms.bfs import *
from classes.graph.graph import *
import random


def graphFromVector(scene, graph: Graph, vect: list):  # Rina
    summ_of_power = 0
    list_edges = []
    vec = [int(x) for x in vect]
    vec.sort(reverse=True)
    for cur in vec:
        summ_of_power += cur
    if summ_of_power % 2 != 0:
        return False
    num_of_edges = summ_of_power / 2
    num_of_vertex = len(vec)
    vertex_and_powers = {}
    for i in range(0, num_of_vertex):
        vertex_and_powers[graph.getVertexList()[i]] = vec[i]
    flag = True

    is_correct = CalcEdges(scene, graph, vertex_and_powers, list_edges, flag)
    if is_correct == False:
        list_edges.clear()
        flag = False
        for i in range(0, num_of_vertex):
            vertex_and_powers[graph.getVertexList()[i]] = vec[i]
        is_correct = CalcEdges(scene, graph, vertex_and_powers, list_edges, flag)

    # for cur_vertex in vertex_and_powers.keys():
    #     while vertex_and_powers[cur_vertex] > 0:
    #         all = list(vertex_and_powers.keys())
    #         #for i in range(len(all)-1, -1, -1):
    #         for i in range(len(all)):
    #             if all[i] != cur_vertex and vertex_and_powers[all[i]] > 0 and vertex_and_powers[cur_vertex] and flag == True:
    #                 vertex_and_powers[all[i]] -= 1
    #                 vertex_and_powers[cur_vertex] -= 1
    #                 factor = scene.countEdgeFactor(cur_vertex, all[i])
    #                 list_edges.append(
    #                     Edge(cur_vertex, all[i], color=QtCore.Qt.green, name=createNameEdge(graph, graph.getVertexList()), factor=factor))
    #                 alldone= 0
    #                 for i in vertex_and_powers.keys():
    #                     alldone += vertex_and_powers[i]
    #                 if alldone == vertex_and_powers[cur_vertex]:
    #                     list_edges.clear()
    #                     for j in range(0, num_of_vertex):
    #                         vertex_and_powers[graph.getVertexList()[i]] = vec[j]
    #                     flag = False

    return list_edges

def extra_ideal_check (graph : Graph, do_base : bool):
    is_extrim = do_base
    output = 'Ваш граф является '
    max_color = 0
    max_click = max_click_num(graph)
    coloredVertex = colorize(graph)
    for vert in coloredVertex.keys():
        if max_color < coloredVertex[vert]:
            max_color = coloredVertex[vert]
    if max_color != max_click:
        output += 'не совершенным '
    else: output += 'совершенным '
    count_edges = (1 - 1/((max_color+1)-1))*(len(graph.getVertexList())**2)/2   #5,5,5,5,5,5
    if int(count_edges) != len(graph.getEdgeList()):
        output += 'и не экстримальным'
    else:
        is_extrim = True
        output += 'и экстримальным'
    if is_extrim:
        visited = bfs(graph, graph.getVertexList()[0])
        for visit_vert in visited.keys():
            if visited[visit_vert] is None:
                output += 'Базы нет, граф несвязный'
                return output
        for i in range(max_color):
            cur_color_list = []
            cur_color_adj_vertex = []
            for vert in coloredVertex.keys():
                if coloredVertex[vert] == i+1:
                    cur_color_list.append(vert)
                    cur_color_adj_vertex += vert.getAdjacentVertexList()
            if len(set(cur_color_adj_vertex))+len(cur_color_list) == len(graph.getVertexList()):
                for cur in cur_color_list:
                    cur.setColor(QtGui.QColor(105, 36, 126))
                    cur.setServiceValue("base")
                output += '. База выведена'
                return output

    return output


def CalcEdges(scene, graph: Graph, vertex_and_powers: dict, list_edges : list, flag : bool):
    num_of_vertex = len(vertex_and_powers.keys())
    for cur_vertex in vertex_and_powers.keys():
        while vertex_and_powers[cur_vertex] > 0:
            all = list(vertex_and_powers.keys())
            #for i in range(len(all)-1, -1, -1):
            for i in range(len(all)):
                if flag:
                        if all[i] != cur_vertex and vertex_and_powers[all[i]] > 0 and vertex_and_powers[cur_vertex]:
                            vertex_and_powers[all[i]] -= 1
                            vertex_and_powers[cur_vertex] -= 1
                            factor = scene.countEdgeFactor(cur_vertex, all[i])
                            list_edges.append(
                                Edge(cur_vertex, all[i], color=QtCore.Qt.green, name=createNameEdge(graph, list_edges), factor=factor))
                else:
                    if i % 2 == 0:
                        if all[i] != cur_vertex and vertex_and_powers[all[i]] > 0 and vertex_and_powers[cur_vertex]:
                            vertex_and_powers[all[i]] -= 1
                            vertex_and_powers[cur_vertex] -= 1
                            factor = scene.countEdgeFactor(cur_vertex, all[i])
                            list_edges.append(
                                Edge(cur_vertex, all[i], color=QtCore.Qt.green, name=createNameEdge(graph, list_edges), factor=factor))
                    else:
                        if all[len(all) - i] != cur_vertex and vertex_and_powers[all[len(all) - i]] > 0 and vertex_and_powers[cur_vertex]:
                            vertex_and_powers[all[len(all) - i]] -= 1
                            vertex_and_powers[cur_vertex] -= 1
                            factor = scene.countEdgeFactor(cur_vertex, all[len(all) - i])
                            list_edges.append(
                                Edge(cur_vertex, all[len(all) - i], color=QtCore.Qt.green, name=createNameEdge(graph, list_edges), factor=factor))

            alldone= 0
            for i in vertex_and_powers.keys():
                alldone += vertex_and_powers[i]
            if alldone == vertex_and_powers[cur_vertex] and alldone > 0:
                return False
    return True

def max_click_num(graph: Graph):

    def MatrixMade(n):
        matrix = []
        for i in range(n):
            matrix.append([])
            for j in range(n):
                if (i == j):
                    matrix[i] += [(0)];
                else:
                    matrix[i] += [(-999999999)]
        return matrix

    def new_set(old_set, v, m):
        new_set1 = set()
        for i in old_set:
            if m[i - 1][v - 1] > -1:  new_set1.add(i)
        return new_set1

    def prov(not1, candidates1, m1):
        for i in not1:
            k = 1
            for j in candidates1:
                if (m1[i - 1][j - 1] < 0):
                    k = 0
                    break
            if k == 1:
                return (False)
        return (True)

    compsub = set()
    klik = [()]
    max_k = [0]
    on = [0]

    def extended(candidates3, not3, m1, compsub, klik, max_k, on):
        # global compsub, klik, max_k, on
        print(list(not3), " ", on[0], " ", list(candidates3))
        while (not (len(candidates3) == 0) and (prov(not3, candidates3, m1))):
            v = list(candidates3)[0]
            print(list(not3), " ", on[0], " ", list(candidates3))
            candidates3.pop()
            compsub.add(v)
            new_candidates = new_set(candidates3, v, m1)
            new_not = new_set(not3, v, m1)
            on[0] = on[0] + 1
            if (len(new_candidates) == 0) and (len(new_not) == 0):
                if len(compsub) > 1:
                    #       print ("Размер ",len(compsub)," Вершины: ",compsub)
                    klik += [(list(compsub))]
                    if len(compsub) > max_k[0]: max_k[0] = len(compsub)
            else:
                extended(new_candidates, new_not, m1, compsub, klik, max_k, on)
            not3.add(v)
            compsub.discard(v)
            candidates3.discard(v)

    n = len(graph.getVertexList())
    M = graph.getAdjacentMatrix()
    k = len(graph.getEdgeList())
    # print("Введите ", k, " строк вида x y(где x,y вершины ребер графа): ")
    # for i in range(k):
    #     o, s = map(int, input('').split())
    #     if not (o == s):
    #         M[o - 1][s - 1] = 1;
    #         M[s - 1][o - 1] = 1;
    candidates = set(i for i in range(1, n + 1))
    not0 = set()
    extended(candidates, not0, M, compsub, klik, max_k, on)
    # print (klik[1:])

    for j in range(2, max_k[0] + 1):
        print("Клики размером ", j, ": ")
        for i in klik[1:]:
            if len(i) > j - 1:
                print(list(itertools.combinations(i, j)))
    return on[0]



def setVisualForVector(graph: Graph, completed_nodes):
    if completed_nodes == False: return False
    for i in completed_nodes:
        graph.addEdge(i)

def createNameEdge(graph: Graph, completed_nodes):
    name_from_graph = 1 if len(completed_nodes) == 0 else int(completed_nodes[-1].getName()) + 1
    return (str(name_from_graph))
