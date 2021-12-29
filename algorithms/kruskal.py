from classes.graph.graph import *

def kruskal(graph: Graph):
    connected_vertex_sets = []
    spanning_tree_edges = set()

    sorted_edge_list = sorted(graph.getEdgeList(), key=lambda x: int(x.getWeight()))
    for edge in sorted_edge_list:
        is_added = False
        first_vertex_set = set()
        second_vertex_set = set()
        is_first_set_found = False
        is_second_set_found = False
        for vertex_set in connected_vertex_sets:
            if edge.getStartVertex() in vertex_set:
                first_vertex_set = vertex_set
                is_first_set_found = True
            if edge.getEndVertex() in vertex_set:
                second_vertex_set = vertex_set
                is_second_set_found = True

        if is_first_set_found and is_second_set_found:
            if first_vertex_set != second_vertex_set:
                join_set = first_vertex_set
                for elem in second_vertex_set:
                    join_set.add(elem)
                connected_vertex_sets.remove(second_vertex_set)
                connected_vertex_sets.remove(first_vertex_set)
                connected_vertex_sets.append(join_set)
                spanning_tree_edges.add(edge)
            is_added = True
        elif is_first_set_found:
            first_vertex_set.add(edge.getStartVertex())
            first_vertex_set.add(edge.getEndVertex())
            spanning_tree_edges.add(edge)
            is_added = True
        elif is_second_set_found:
            second_vertex_set.add(edge.getStartVertex())
            second_vertex_set.add(edge.getEndVertex())
            spanning_tree_edges.add(edge)
            is_added = True

        if not is_added:
            vertex_set = set()
            vertex_set.add(edge.getStartVertex())
            vertex_set.add(edge.getEndVertex())
            spanning_tree_edges.add(edge)
            connected_vertex_sets.append(vertex_set)

    for edge in graph._edgeList:
        if edge in spanning_tree_edges:
            edge.setColor(QtCore.Qt.green)
