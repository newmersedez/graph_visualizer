from algorithms.bfs import bfs
from algorithms.connected import *
from classes.graph.graph import *
from queue import Queue


def search_min_cycle(graph: Graph):
    cycles = []
    for vertex in graph.getVertexList():
        visited_nodes = set()
        is_cycled = False
        nodes_to_visit = Queue()
        nodes_to_visit.put(vertex)
        ways = [[vertex]]
        way_edges = []
        visited_nodes.add(vertex)
        while nodes_to_visit.qsize() > 0 and not is_cycled:
            new_vertex: Vertex = nodes_to_visit.get()
            adjacent_vertex_list = new_vertex.getAdjacentVertexList()
            current_way = []
            for way in ways:
                if way.count(vertex):
                    current_way = way
                    ways.remove(current_way)
                    break

            for adjacent_vertex in adjacent_vertex_list:
                if adjacent_vertex in current_way:
                    continue
                way = current_way.copy()
                way.append(adjacent_vertex)
                if adjacent_vertex in visited_nodes:
                    is_cycled = True
                    for way_iter in ways:
                        if way_iter.count(adjacent_vertex):
                            prev_vertex = way_iter[0]
                            for curr_vertex in way_iter[1:]:
                                way_edges.append(Edge(prev_vertex, curr_vertex))
                                prev_vertex = curr_vertex
                            break
                    prev_vertex = way[0]
                    for curr_vertex in way[1:]:
                        way_edges.append(Edge(prev_vertex, curr_vertex))
                        prev_vertex = curr_vertex
                    break
                else:
                    ways.append(way)
                visited_nodes.add(adjacent_vertex)
                nodes_to_visit.put(adjacent_vertex)
        if is_cycled:
            cycles.append(way_edges)
    cycles.sort(key=lambda x: len(x))

    if is_cycled:
        for edge in graph._edgeList:
            for edge_copy in cycles[0]:
                if edge.getStartVertex() == edge_copy.getStartVertex() and edge.getEndVertex() == edge_copy.getEndVertex() or edge.getStartVertex() == edge_copy.getEndVertex() and edge.getEndVertex() == edge_copy.getStartVertex():
                    edge.setColor(QtCore.Qt.green)
    else:
        centre_search(graph)


def centre_search(graph: Graph):
    vertexes = graph.getVertexList()
    list = []
    for vertex in vertexes:
        depths = bfs(graph, vertex)
        list.append((vertex, max(depths.values())))

    list.sort(key=lambda x: x[1])
    if len(list):
        min_depth = list[0][1]
        for pair in list:
            if pair[1] != min_depth:
                break
            pair[0].setColor(QtCore.Qt.green)
            pair[0].setServiceValue("d = " + str(min_depth))

def is_search_min_cycle_applicable(graph: Graph):
    return not graph.isDirected() and isConnected(graph)