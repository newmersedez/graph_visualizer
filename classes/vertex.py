from utils.defines import VERTEX_RADIUS
from PyQt5.QtWidgets import QLabel


class Vertex(QLabel):
    def __init__(self, x: int, y: int, name: str, color: str):
        super().__init__()
        self._x = x
        self._y = y
        self._name = name
        self._color = color
        self._adjacentVertexList = list()
        self._dragging = False
        self.setAcceptDrops(True)

    def getPos(self):
        return self._x, self._y

    def getName(self):
        return self._name

    def getColor(self):
        return self._color

    def getAdjacentVertexList(self):
        return self._adjacentVertexList

    def setPos(self, x: int, y: int):
        self._x = x
        self._y = y

    def setName(self, name: str):
        self._name = name

    def setColor(self, color: str):
        self._color = color

    def addAdjacentVertex(self, vertex):
        self._adjacentVertexList.append(vertex)

    def removeAdjacentVertex(self, vertex):
        if vertex in self._adjacentVertexList:
            self._adjacentVertexList.remove(vertex)

    def findAdjacentVertex(self, vertex):
        if vertex in self._adjacentVertexList:
            return True
        return False

    def draggingStatus(self):
        return self._dragging

    def draggingStart(self):
        print('dragging start')
        self._dragging = True

    def draggingStop(self):
        print('dragging end')
        self._dragging = False

    def collidePoint(self, x: int, y: int):
        dist_x = abs(self._x - x)
        dist_y = abs(self._y - y)

        if (dist_x <= VERTEX_RADIUS) and (dist_y <= VERTEX_RADIUS):
            return True
        return False

    def collide_vertex(self, vertex):
        center_x, center_y = vertex.getPos()
        dist_x = abs(self._x - center_x)
        dist_y = abs(self._y - center_y)

        if (dist_x <= 2 * VERTEX_RADIUS) and (dist_y <= 2 * VERTEX_RADIUS):
            return True
        return False
