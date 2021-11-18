from classes.graph.verge import *
from classes.graph.vertex import *
from classes.MVP.graph import *
from queue import Queue
import numpy as np


def bfs(graph: Graph, vertex: Vertex):
    visited_nodes = [False] * len(graph.getVertexList())
    shortest_ways = [None] * len(graph.getVertexList())
    nodes_to_visit = Queue()
    nodes_to_visit.put(vertex)
    while nodes_to_visit.qsize() > 0:
        new_vertex: Vertex = nodes_to_visit.get()
        adjlist = new_vertex.getAdjacentVertexList()
        

