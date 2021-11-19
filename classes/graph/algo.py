from classes.graph.verge import *
from classes.graph.vertex import *
from classes.MVP.graph import *
from queue import Queue
import numpy as np


def bfs(graph: Graph, vertex: Vertex):
    visited_nodes = [False] * len(graph.getVertexList())
    shortest_ways = {}
    for i in graph.getVertexList():
        shortest_ways[i] = None
    shortest_ways[vertex] = 0
    nodes_to_visit = Queue()
    nodes_to_visit.put(vertex)
    print("ranges from node ", vertex.getName())
    while nodes_to_visit.qsize() > 0:
        new_vertex: Vertex = nodes_to_visit.get()
        adj_list = new_vertex.getAdjacentVertexList()
        for i in adj_list:
            range_vertex = new_vertex.rangeToAdjNode(i)
            if range_vertex is not None and shortest_ways[i] is None:
                shortest_ways[i] = shortest_ways[new_vertex] + range_vertex
                nodes_to_visit.put(i)
    names_lst = [i.getName() for i in shortest_ways.keys()]
    range_lst = [i for i in shortest_ways.values()]

    print("asdsabef")
    print(names_lst)
    print(range_lst)



    return (shortest_ways)

