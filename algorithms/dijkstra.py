from classes.graph.graph import *
from queue import Queue


def get_end_node(begin: Vertex, edge: Edge):
    tmp_end_node = edge.getEndVertex()
    if tmp_end_node == begin:
        tmp_end_node = edge.getStartVertex()
    return tmp_end_node


def dijkstra_algo(graph: Graph, vertex: Vertex):
    checked_nodes = {}
    ranges_to_nodes = {}
    for i in graph.getVertexList():
        checked_nodes[i] = False
        ranges_to_nodes[i] = None
    ranges_to_nodes[vertex]: int = 0
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
            print(type(i))
            print(type(x))
            print(x)
            if not tmp_end_node:
                continue
            if ranges_to_nodes[tmp_end_node] is None:
                ranges_to_nodes[tmp_end_node] = tmp_range_from_node + i.getWeight()
            elif ranges_to_nodes[tmp_end_node] > tmp_range_from_node + i.getWeight():
                ranges_to_nodes[tmp_end_node] = tmp_range_from_node + i.getWeight()
            if not checked_nodes[tmp_end_node]:
                nodes_to_visit.put(tmp_end_node)
        checked_nodes[checking_node] = True
    names = [i.getName() for i in ranges_to_nodes.keys()]
    ranges = [i for i in ranges_to_nodes.values()]
    print(names)
    print(ranges)

    return (ranges_to_nodes)

def setVisualForDijkstra(ranges_to_nodes):
    for i in ranges_to_nodes.keys():
        if ranges_to_nodes[i] is not None and ranges_to_nodes[i] != 0:
            i.setServiceValue("r=" + str(ranges_to_nodes[i]))
