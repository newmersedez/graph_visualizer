from classes.graph.graph import *
from queue import Queue


def bfs(graph: Graph, vertex: Vertex):
    visited_nodes = [False] * len(graph.getVertexList())
    shortest_ways = {}
    depth = {}
    bfs_steps = []

    for i in graph.getVertexList():
        shortest_ways[i] = None
        depth[i] = None
    shortest_ways[vertex] = 0
    depth[vertex] = 0

    nodes_to_visit = Queue()
    nodes_to_visit.put(vertex)
    while nodes_to_visit.qsize() > 0:
        new_vertex: Vertex = nodes_to_visit.get()
        adj_list = new_vertex.getAdjacentVertexList()
        tmp = []
        for i in adj_list:
            range_vertex = new_vertex.rangeToAdjNode(i)
            if range_vertex is not None and shortest_ways[i] is None and new_vertex.isReachable(i):
                shortest_ways[i] = shortest_ways[new_vertex] + range_vertex
                depth[i] = depth[new_vertex] + 1
                tmp.append(i)
                nodes_to_visit.put(i)
        if len(tmp) > 0:
            bfs_steps.append(tmp)

    for i in shortest_ways.keys():
        if (depth[i] != 0):
            i.setColor("red")
            i.setServiceValue("n=" + str(depth[i]))

    return shortest_ways