import numpy
from classes.graph.graph import *
from algorithms.bfs import *
from algorithms.dijkstra import *
import operator
import itertools
import heapq

def h(vertex: Vertex, end_vertex: Vertex):
    return sqrt((vertex.x() - end_vertex.x())**2 + (vertex.y() - end_vertex.y())**2) / 120


def best_first_search(graph: Graph, begin_vertex: Vertex, end_vertex: Vertex):
    if (begin_vertex == end_vertex):
        return {}
    q = []
    # heapq.heapify(q)
    heapq.heappush(q, (0, begin_vertex))
    came_from = {}
    visited_edges = {}
    came_from[begin_vertex] = None

    while q.__len__() > 0:
        current = heapq.heappop(q)[1]
        if current == end_vertex:
            break

        reachable_edges = [i for i in current.getAdjacentEdgeList()
                           if (i.getStartVertex() == current or not i.isDirected())]

        for edge in reachable_edges:
            next = get_end_node(current, edge)
            if edge in visited_edges or next == current:
                continue
            visited_edges[edge] = True
            priority = h(next, end_vertex)
            heapq.heappush(q, (priority, next))
            came_from[next] = (current, edge)
        print(q)

    len = 0
    path = []
    i = end_vertex
    while came_from[i] is not None:
        print('{}->{}'.format(i.getName(), came_from[i][0].getName()))
        tmp = came_from[i]
        len += tmp[1].getWeight()
        path.append(tmp[1])
        i = tmp[0]
    print("path = ", [i.getName() for i in path])
    print("len of path = ", len)
    return path

def setVisualForBestFirst(path):
    for i in path:
        i.setColor(QtCore.Qt.green)

