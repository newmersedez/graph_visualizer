from classes.graph.graph import *

def kruskal(graph: Graph):
    connected_vertex_sets = []
    spanning_tree_edges = set()

    def function(edge: Edge):
        return int(edge.getWeight())

    sorted_edge_list = sorted(graph.getEdgeList(), key=function)
    for edge in sorted_edge_list:
        is_cycled = False
        is_added = False
        for vertex_set in connected_vertex_sets:
            if edge.getStartVertex() in vertex_set and edge.getEndVertex() in vertex_set:
                is_cycled = True
                break
            elif edge.getStartVertex() in vertex_set or edge.getEndVertex() in vertex_set:
                vertex_set.add(edge.getStartVertex())
                vertex_set.add(edge.getEndVertex())
                spanning_tree_edges.add(edge)
                is_added = True
                break

        if is_cycled:
            continue

        elif not is_added:
            vertex_set = set()
            vertex_set.add(edge.getStartVertex())
            vertex_set.add(edge.getEndVertex())
            spanning_tree_edges.add(edge)
            connected_vertex_sets.append(vertex_set)

    for edge in graph._edgeList:
        if edge in spanning_tree_edges:
            edge.setColor(QtCore.Qt.green)
