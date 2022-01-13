from algorithms.bfs import *
from algorithms.dijkstra import get_end_node
from algorithms.connected import isConnected

def find_cycle_from_palm_tree(palm, cycles, prev_node):
    cycle_info = cycles[0]
    end_node_of_cycle = get_end_node(cycle_info[0], cycle_info[1])
    cycle_edges = [cycle_info[1]]
    begin_node_of_cycle = cycle_info[0]
    curr = begin_node_of_cycle
    while curr != end_node_of_cycle:
        parent_node = prev_node[curr][0]
        parent_edge = prev_node[curr][1]
        cycle_edges.append(parent_edge)
        curr = parent_node
    return cycle_edges


def remove_cycle(palm: Graph, cycle: list):
    for i in cycle:
        palm.removeEdge(i)


def create_components_connectivity_list(palm):
    graphs_info = {}
    print(palm.getAdjacentMatrix())
    components = isConnected(palm)
    for i in components.keys():
        if components[i] not in graphs_info:
            graphs_info[components[i]] = ([], set([]))
        graphs_info[components[i]][0].append(i)
        len_lst = len(i.getAdjacentEdgeList())
        graphs_info[components[i]][1].update(i.getAdjacentEdgeList())
    graphs = []
    for component_number in graphs_info.keys():
        G_to_New = {}
        new_graph = Graph()
        for i in graphs_info[component_number][0]:
            new_vertex = Vertex(i.x(), i.y(), "conncpy " + i.getName(), i.getColor())
            new_graph.addVertex(new_vertex)
            G_to_New[i] = new_vertex
        for i in graphs_info[component_number][1]:
            old_begin_node = i.getStartVertex()
            old_end_node = i.getEndVertex()
            new_edge = Edge(G_to_New[old_begin_node], G_to_New[old_end_node], i.getName())
            new_graph.addEdge(new_edge)
        graphs.append(new_graph)
        print([i.getName() for i in new_graph.getVertexList()])
    return graphs


def dfs_palm_tree(graph: Graph, visited, palm: Graph, vertex: Vertex, G_to_T, cycles, prev_node):
    visited[vertex] = True

    for edge in vertex.getAdjacentEdgeList():
        i = get_end_node(vertex, edge)
        if i not in visited:
            t_edge = Edge(G_to_T[vertex], G_to_T[i], "copy " + str(len(palm.getEdgeList()) + 1))
            palm.addEdge(t_edge)
            prev_node[G_to_T[i]] = (G_to_T[vertex], t_edge)
            dfs_palm_tree(graph, visited, palm, i, G_to_T, cycles, prev_node)
        elif i in visited and G_to_T[vertex] not in G_to_T[i].getAdjacentVertexList():
            t_edge = Edge(G_to_T[vertex], G_to_T[i], "copy " + str(len(palm.getEdgeList()) + 1))
            palm.addEdge(t_edge)
            cycles.append((G_to_T[vertex], t_edge))
        else:
            continue





def isPlanarSubgraphs(graph: Graph):
    n = len(graph.getVertexList())
    m = len(graph.getVertexList())

    if n <= 4:
        print("True")
        return True
    if n > 3 and m > 3 * n - 6:
        print("False")
        return False

    palm_tree = Graph()
    begin_node = graph.getVertexList()[0]
    visited = {}
    cycles = []
    prev_node = {begin_node: None}
    G_to_T = {}
    T_to_G = {}

    for i in graph.getVertexList():
        new_vertex_for_palm = Vertex(i.x(), i.y(), "copy " + i.getName(), i.getColor())
        palm_tree.addVertex(new_vertex_for_palm)
        G_to_T[i] = new_vertex_for_palm
        T_to_G[new_vertex_for_palm] = i
    dfs_palm_tree(graph, visited, palm_tree, begin_node, G_to_T, cycles, prev_node)
    if len(cycles) == 0:
        print("True")
        return True
    print("хуета")
    true_cycle = find_cycle_from_palm_tree(palm_tree, cycles, prev_node)
    print("хуета")
    remove_cycle(palm_tree, true_cycle)
    print("хуета")
    for i in create_components_connectivity_list(palm_tree):
        print(i.getAdjacentMatrix())
        if not isPlanarSubgraphs(i):
            print("False")
            return False
    print("True")
    return True



