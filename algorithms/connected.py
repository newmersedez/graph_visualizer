from classes.graph.graph import *
from algorithms.bfs import *
from queue import Queue


def get_end_node(begin: Vertex, edge: Edge):
    tmp_end_node = edge.getEndVertex()
    if tmp_end_node == begin:
        tmp_end_node = edge.getStartVertex()
    return tmp_end_node

# для неориентированного
def isConnected(graph: Graph):
    a = graph.getVertexList().copy()
    components = {}
    component_number = 1
    while len(a) > 0:
        i = a[0]
        tmp_bfs = bfs(graph, a[0])
        for i in tmp_bfs.keys():
            if tmp_bfs[i] is not None:
                components[i] = component_number
                a.remove(i)
        component_number += 1
    return components

def isWeaklyConnected(graph: Graph):
    directed = set()
    for i in graph.getEdgeList():
        if i.isDirected():
            directed.add(i)
            i._isDirection = False
    ans = isConnected(graph)
    for i in directed:
        i._isDirection = True
    return ans


def dfs1(v: Vertex, q, visited):
    visited[v] = True
    reachable_edges = [i for i in v.getAdjacentEdgeList()
                       if (i.getStartVertex() == v or not i.isDirected())]
    for i in reachable_edges:
        if get_end_node(v, i) not in visited:
            dfs1(get_end_node(v, i), q, visited)
    print(v.getName())
    q.append(v)


def dfs2(v: Vertex, components, component_number):
    components[v] = component_number
    reachable_edges = [i for i in v.getAdjacentEdgeList()
                       if (i.getStartVertex() == v or not i.isDirected())]
    for i in reachable_edges:
        if get_end_node(v, i) not in components:
            dfs2(get_end_node(v, i), components, component_number)


def isStronglyConnected(graph: Graph):
    q = []
    visited = {}
    for i in graph.getVertexList():
        if i not in visited:
            dfs1(i, q, visited)
    for i in graph.getEdgeList():
        tmp_node = i.getStartVertex()
        i._startVertex = i.getEndVertex()
        i._endVertex = tmp_node
    component_number = 1
    components = {}
    q.reverse()
    for i in q:
        if i not in components:
            dfs2(i, components, component_number)
            component_number += 1

    for i in graph.getEdgeList():
        tmp_node = i.getStartVertex()
        i._startVertex = i.getEndVertex()
        i._endVertex = tmp_node
    print([i.getName() for i in components.keys()])
    print(list(components.values()))
    return components

def setVisualForConnected(graph: Graph):
    ans = ""
    isDirected = False
    for i in graph.getEdgeList():
        if i.isDirected():
            isDirected = True
            break

    if isDirected:
        a = isStronglyConnected(graph)
        stronglyComponentsNumber = max(a.values())
        b = isWeaklyConnected(graph)
        weaklyComponentsNumber = max(b.values())

        for i in a.keys():
            i.setServiceValue(f"s={a[i]},w={b[i]}")
        print(f"weakly components number = {weaklyComponentsNumber},\n\
         strongly components number = {stronglyComponentsNumber}")
    else:
        a = isConnected(graph)
        for i in a.keys():
            i.setServiceValue(f"c={a[i]}")
        cutpts = checkCutpoints(graph)
        for i in cutpts.keys():
            i.setColor(QtCore.Qt.green)
        brigds = checkBridges(graph)
        for i in brigds.keys():
            i.setColor(QtCore.Qt.red)


def dfsCutpoints(v: Vertex, used, tin, fup, cutpoints, parent=None, timer=0):
    used[v] = True
    tin[v] = timer
    fup[v] = timer
    timer += 1
    children = 0
    reachable_edges = [i for i in v.getAdjacentEdgeList()
        if (i.getStartVertex() == v or not i.isDirected())]
    for i in reachable_edges:
        to = get_end_node(v, i)
        if to == parent:
            continue
        if to in used:
            fup[v] = min(fup[v], tin[to])
        else:
            dfsCutpoints(to, used, tin, fup, cutpoints, parent=v, timer=timer)
            fup[v] = min(fup[v], fup[to])
            if fup[to] >= tin[v] and parent is not None:
                cutpoints[v] = True
            children += 1
    if parent is None and children > 1:
        cutpoints[v] = True


def checkCutpoints(graph: Graph):
    cutpoints = {}
    dfsCutpoints(graph.getVertexList()[0], {}, {}, {}, cutpoints)
    return (cutpoints)

def dfsBridges(v: Vertex, used, tin, fup, bridges, parent=None, timer=0):
    used[v] = True
    tin[v] = timer
    fup[v] = timer
    timer += 1
    children = 0
    reachable_edges = [i for i in v.getAdjacentEdgeList()
        if (i.getStartVertex() == v or not i.isDirected())]
    for i in reachable_edges:
        to = get_end_node(v, i)
        if to == parent:
            continue
        if to in used:
            fup[v] = min(fup[v], tin[to])
        else:
            dfsBridges(to, used, tin, fup, bridges, parent=v, timer=timer)
            fup[v] = min(fup[v], fup[to])
            if fup[to] > tin[v]:
                bridges[i] = True

def checkBridges(graph: Graph):
    bridges = {}
    dfsBridges(graph.getVertexList()[0], {}, {}, {}, bridges)
    return bridges