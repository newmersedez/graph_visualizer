from classes.graph.graph import *

def getColorFromColorNumber(color : int):
    t = color / (1 + 50.0)
    red = (int)(9 * (1 - t) * pow(t, 3) * 255)
    green = (int)(15 * pow((1 - t), 2) * pow(t, 2) * 255)
    blue = (int)(8.5 * pow((1 - t), 3) * t * 255)
    return QtGui.QColor(red, green, blue)

def get_end_node(begin: Vertex, edge: Edge):
    tmp_end_node = edge.getEndVertex()
    if tmp_end_node == begin:
        tmp_end_node = edge.getStartVertex()
    return tmp_end_node


# покрасить ноду vertex в цвет color, если это возможно (проверяется проверкой смежных вершин на тот же самый цвет)
def colorizeNode(color: int, colors : dict, vertex: Vertex):
    if colors[vertex] is not None:
        return
    flag = True
    for i in vertex.getAdjacentVertexList():
        if colors[i] == color:
            flag = False
            break
    if flag:
        colors[vertex] = color

def colorize(graph: Graph):
    sorted_vertex = sorted(graph.getVertexList(), key=(lambda x: len(x.getAdjacentVertexList())), reverse=True)
    color = 1
    colors_of_nodes = {}
    for i in sorted_vertex:
        colors_of_nodes[i] = None
    colors_of_nodes[sorted_vertex[0]] = color
    while True:
        flag = True
        for i in sorted_vertex:
            colorizeNode(color, colors_of_nodes, i)
        color += 1
        for i in colors_of_nodes.keys():
            if colors_of_nodes[i] is None:
                flag = False
        if flag:
            break
    print([i for i in colors_of_nodes.items()])
    print_colors_of_nodes = sorted([i for i in colors_of_nodes.items()], key=(lambda x: x[0].getName()))
    print([i[0].getName() for i in print_colors_of_nodes])
    print([i[1]for i in print_colors_of_nodes])
    print("chromatic color = ", color - 1)
    return colors_of_nodes

def setVisualForColorize(colors_of_nodes : dict):
    for i in colors_of_nodes.keys():
        i.setColor(getColorFromColorNumber(colors_of_nodes[i] * 10))
