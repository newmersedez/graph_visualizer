from PyQt5 import QtWidgets, QtGui, QtCore
from utils.defines import *


class Vertex:
    def __init__(self, x: int, y: int, name: str, color: str):
        self.x = x
        self.y = y
        self.name = name
        self.color = color
        self.radius = VERTEX_RADIUS
        self.adjacentVertexList = list()
