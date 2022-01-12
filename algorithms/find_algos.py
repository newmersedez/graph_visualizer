from algorithms.astar import *
from algorithms.best_first import *
from utils.colorpalletes import *
import random
import numpy as np
from algorithms.connected import *
from time import time

def getRange(i, j):
    return int(np.sqrt((i.x() - j.x())**2 + (i.y() - j.y())**2))

def getPOfConnect(range: int, scale: int):
    return 0.01 * (0.5 ** (range/scale))

def get_end_node(begin: Vertex, edge: Edge):
    tmp_end_node = edge.getEndVertex()
    if tmp_end_node == begin:
        tmp_end_node = edge.getStartVertex()
    return tmp_end_node

def getPathFromPrevNodeAndEdge(prev_node_and_edge, node_to: Vertex):
    path = []
    begin_node_and_edge = prev_node_and_edge[node_to]
    while begin_node_and_edge is not None:
        previous_node = begin_node_and_edge[0]
        edge_from_previous_to_current = begin_node_and_edge[1]
        path.append(edge_from_previous_to_current)
        begin_node_and_edge = prev_node_and_edge[previous_node]
    path.reverse()
    return path

def dijkstra_with_path(graph: Graph, vertex: Vertex):
    visited = {}
    prev_node_and_edge = {}
    ranges_to_nodes = {}
    for i in graph.getVertexList():
        visited[i] = False
        ranges_to_nodes[i] = None
    ranges_to_nodes[vertex] = 0
    prev_node_and_edge[vertex] = None
    for n in range(len(graph.getVertexList())):
        curr = None
        for i in ranges_to_nodes.keys():
            if not visited[i] and (ranges_to_nodes[i] is not None and (curr is None or\
                                                                       ranges_to_nodes[i] < ranges_to_nodes[curr])):
                curr = i
        if curr is vertex and visited[curr]:
            print("but why??...")
            break
        visited[curr] = True
        print("curr_name = ", curr.getName())
        for i in curr.getAdjacentEdgeList():
            end_node = get_end_node(curr, i)
            if ranges_to_nodes[end_node] is None:
                ranges_to_nodes[end_node] = i.getWeight() + ranges_to_nodes[curr]
                prev_node_and_edge[end_node] = (curr, i)
            elif ranges_to_nodes[end_node] > i.getWeight() + ranges_to_nodes[curr]:
                ranges_to_nodes[end_node] = i.getWeight() + ranges_to_nodes[curr]
                prev_node_and_edge[end_node] = (curr, i)
    return ranges_to_nodes, prev_node_and_edge

def bfs_with_path(graph: Graph, vertex: Vertex):
    shortest_ways = {vertex: 0}
    depth = {vertex: 0}
    prev_node_and_edge = {vertex: None}

    nodes_to_visit = Queue()
    nodes_to_visit.put(vertex)
    while nodes_to_visit.qsize() > 0:
        current_node: Vertex = nodes_to_visit.get()
        reachable_edges = [i for i in current_node.getAdjacentEdgeList()
                if (i.getStartVertex() == current_node or not i.isDirected())]
        for i in reachable_edges:
            end_node = get_end_node(current_node, i)
            if end_node not in depth:
                prev_node_and_edge[end_node] = (current_node, i)
                shortest_ways[end_node] = shortest_ways[current_node] + i.getWeight()
                depth[end_node] = depth[current_node] + 1
                nodes_to_visit.put(end_node)
    return shortest_ways, prev_node_and_edge

def generate_graph():
    nodes_number = 500

    xmax = 1000
    ymax = 1000
    # set_coords = set()
    graph = Graph()

    for i in range(nodes_number):
        x = int(random.uniform(0, 1) * xmax)
        y = int(random.uniform(0, 1) * ymax)
        # if (x, y) in set_coords:
        #     continue
        # set_coords.add((x, y))
        # vertex =
        graph.addVertex(Vertex(x, y, str(i), VERTEX_COLOR))

    name = 1
    for i in graph.getVertexList():
        for j in graph.getVertexList():
            if i == j:
                continue
            random_number = random.uniform(0, 1)
            if random_number < getPOfConnect(getRange(i, j), xmax * np.sqrt(2)):
                # edge =
                name += 1
                graph.addEdge(Edge(startVertex=i, endVertex=j, name=str(name), weight=getRange(i, j)))
    return graph

def generate_pairs(graph: Graph):
    pairs = {"4_6": None, "5_2": None, "1_9": None, "any": (graph.getVertexList()[1], graph.getVertexList()[-1])}
    for i in graph.getVertexList():
        for j in graph.getVertexList():
            if None not in pairs.values():
                break
            if i != j:
                if pairs["1_9"] is None and i.x() < 200 and i.y() < 200 and j.x() > 800 and j.y() > 800:
                    pairs["1_9"] = (i, j)
                if pairs["4_6"] is None and \
                        666 > i.x() > 333 and \
                        333 > i.y() > 0 and \
                        666 > j.x() > 333 and \
                        1000 > j.y() > 666:
                    pairs["4_6"] = (i, j)
                if pairs["5_2"] is None and \
                        666 > i.x() > 333 and \
                        666 > i.y() > 333 and \
                        1000 > j.x() > 666 and \
                        666 > j.y() > 333:
                    pairs["5_2"] = (i, j)
    return pairs


def testAStar(graph, pair):
    start_time = time()
    path = astar(graph, pair[0], pair[1])
    print("astar done!")
    len_of_path = sum([i.getWeight() for i in path])
    end_time = time()

    return (path, len_of_path, end_time - start_time)

def testDijkstra(graph, pair):
    start_time = time()
    _, prev_node_and_edge = dijkstra_with_path(graph, pair[0])
    print("dijkstra done")
    path = getPathFromPrevNodeAndEdge(prev_node_and_edge, pair[1])
    len_of_path = sum([i.getWeight() for i in path])
    end_time = time()

    return (path, len_of_path, end_time - start_time)

def testBestFirst(graph, pair):
    start_time = time()
    path = best_first_search(graph, pair[0], pair[1])
    print("best first done")
    len_of_path = sum([i.getWeight() for i in path])
    end_time = time()

    return (path, len_of_path, end_time - start_time)


def testBFS(graph, pair):
    start_time = time()
    tmp, prev_node_and_edge = bfs_with_path(graph, pair[0])
    path = getPathFromPrevNodeAndEdge(prev_node_and_edge, pair[1])
    print("bfs done!")
    len_of_path = sum([i.getWeight() for i in path])
    end_time = time()

    return (path, len_of_path, end_time - start_time)


def testAlgos(graph, pairs, filename):
    f = open(filename, 'w')
    names = ["bfs", "dijksta", "best first", "A*"]
    for key in pairs.keys():
        print("at key ", key)
        f.write("TEST FOR SITUATION " + key + "\n")
        nodes_pair = pairs[key]
        result_lst = [testBFS(graph, nodes_pair),
                      testDijkstra(graph, nodes_pair),
                      testBestFirst(graph, nodes_pair),
                      testAStar(graph, nodes_pair)]
        for i in range(len(names)):
            f.write(f"{names[i]}:\n time = {result_lst[i][2]}\n" + \
                    f"path = {[k.getName() for k in result_lst[i][0]]}\n" + \
                    f"len of this path = {result_lst[i][1]}\n\n")
            # f.write(f"path = {}, ")
        f.write("\n____________________\n\n")
    f.close()


def find_algos_test():
    graph = generate_graph()
    test = isConnected(graph)
    print("try generate graph")
    lst = []
    number = 1
    print(max(test.values()))
    while number != max(test.values()):
        for i in test.keys():
            if test[i] == number:
                lst.append(i)
                number += 1
    for i in range(len(lst) - 1):
        graph.addEdge(Edge(lst[i], lst[i + 1], name=str(len(graph.getEdgeList()) + 1),
                            weight=getRange(lst[i], lst[i+1])))
    if max(isConnected(graph).values()) != 1:
        print("я хуй знает что произошло")



    print(graph.getAdjacentMatrix())
    pairs = generate_pairs(graph)
    print("graph and pairs generated")
    testAlgos(graph, pairs, "test.txt")




