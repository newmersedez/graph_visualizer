from PyQt5 import QtWidgets, QtGui, QtCore
from utils.defines import *
from classes.vertex import *

class Verge:
    def __init__(self, start_vertex: Vertex, end_vertex: Vertex):
        self.startVertex = start_vertex
        self.endVertex = end_vertex
