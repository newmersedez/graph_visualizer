from classes.graph.graph import *
from queue import Queue


def get_end_node(begin: Vertex, edge: Edge):
    tmp_end_node = edge.getEndVertex()
    if tmp_end_node == begin:
        tmp_end_node = edge.getStartVertex()
    return tmp_end_node


def dijkstra_algo(graph: Graph, vertex: Vertex):
    print("\n\n\n\n\n\n\n\n")
    checked_nodes = {}
    ranges_to_nodes = {}
    for i in graph.getVertexList():
        checked_nodes[i] = False
        ranges_to_nodes[i] = None
    ranges_to_nodes[vertex] = 0
    nodes_to_visit = Queue()
    nodes_to_visit.put(vertex)
    while nodes_to_visit.qsize() > 0:
        checking_node: Vertex = nodes_to_visit.get()

        print("node = {}".format(checking_node.getName()))

        reachable_edges = [i for i in checking_node.getAdjacentEdgeList()
                           if (i.getStartVertex() == checking_node or not i.isDirected())]
        reachable_edges = sorted(reachable_edges, key=(lambda x: x.getWeight()))
        print("reachable (sorted by edge weight) nodes - ",
              [get_end_node(checking_node, i).getName() for i in reachable_edges])
        for i in reachable_edges:
            print("here1")
            tmp_range_from_node = ranges_to_nodes[checking_node]  # inf == None
            tmp_end_node = get_end_node(checking_node, i)
            if not tmp_end_node:
                continue
            print("here2")
            print("i.getW = ", i.getWeight())
            print("tmp range is ", tmp_range_from_node)
            if ranges_to_nodes[tmp_end_node] is None:
                ranges_to_nodes[tmp_end_node] = i.getWeight()
            print("here 2.2")
            if ranges_to_nodes[tmp_end_node] > (tmp_range_from_node + i.getWeight()):
                ranges_to_nodes[tmp_end_node] = tmp_range_from_node + i.getWeight()
            print("here 2.3")
            if not checked_nodes[tmp_end_node]:
                nodes_to_visit.put(tmp_end_node)
            print("maybe here3???")
        checked_nodes[checking_node] = True
        print("end checking node")
    names = [i.getName() for i in ranges_to_nodes.keys()]
    ranges = [i for i in ranges_to_nodes.values()]
    print(names)
    print(ranges)
