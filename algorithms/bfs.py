from classes.graph.graph import *
from queue import Queue


def bfs(graph: Graph, vertex: Vertex):
    visited_nodes = [False] * len(graph.getVertexList())
    shortest_ways = {}
    bfs_steps = []

    for i in graph.getVertexList():
        shortest_ways[i] = None
    shortest_ways[vertex] = 0
    nodes_to_visit = Queue()
    nodes_to_visit.put(vertex)
    while nodes_to_visit.qsize() > 0:
        new_vertex: Vertex = nodes_to_visit.get()
        adj_list = new_vertex.getAdjacentVertexList()
        tmp = []
        for i in adj_list:
            range_vertex = new_vertex.rangeToAdjNode(i)
            if range_vertex is not None and shortest_ways[i] is None:
                shortest_ways[i] = shortest_ways[new_vertex] + range_vertex
                tmp.append(i)
                nodes_to_visit.put(i)
        if len(tmp) > 0:
            bfs_steps.append(tmp)

    for i in range(0, len(bfs_steps)):
        for vertex in bfs_steps[i]:
            vertex.setColor("red")
            vertex.setServiceValue("n=" + str(i + 1))

    return shortest_ways



