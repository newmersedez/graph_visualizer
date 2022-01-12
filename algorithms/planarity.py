from algorithms.bfs import *

#
# def get_end_node(begin: Vertex, edge: Edge):
#     tmp_end_node = edge.getEndVertex()
#     if tmp_end_node == begin:
#         tmp_end_node = edge.getStartVertex()
#     return tmp_end_node


def dfs_palm_tree(graph: Graph, visited, palm: Graph, vertex: Vertex, prev_nodes, rebra):
    # reachable_edges = [i for i in vertex.getAdjacentEdgeList()]
    visited[vertex] = True
    for i in vertex.getAdjacentVertexList():
        if i not in visited:
            palm.addEdge(Edge(vertex, i, str(len(palm.getEdgeList()) + 1)))
            prev_nodes[i] = vertex
            rebra[(i, vertex)] = True
            dfs_palm_tree(graph, visited, palm, vertex)
        elif prev_nodes[vertex] != i and (i, vertex) not in rebra and (vertex, i) not in rebra:
            palm.addEdge(Edge(visited, i, str(len(palm.getEdgeList()) + 1)))
            # dfs_palm_tree(graph, visited, palm, vertex)
        else:
            continue





def built_palm_tree(graph: Graph):
    palm_tree = Graph()
    begin_node = graph.getVertexList()[0]
    visited = {}
    prev_nodes = {begin_node: None}
    rebra = {}


    for i in graph.getVertexList():
        palm_tree.addVertex(i)
