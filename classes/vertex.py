from utils.defines import VERTEX_RADIUS


class Vertex:
    def __init__(self, x: int, y: int, name: str, color: str):
        self.x = x
        self.y = y
        self.name = name
        self.color = color
        self.adjacentVertexList = list()
        self.dragging = False

    def getPos(self):
        return self.x, self.y

    def getName(self):
        return self.name

    def getColor(self):
        return self.color

    def getAdjacentVertexList(self):
        return self.adjacentVertexList

    def setPos(self, x: int, y: int):
        self.x = x
        self.y = y

    def setName(self, name: str):
        self.name = name

    def setColor(self, color: str):
        self.color = color

    def addAdjacentVertex(self, vertex):
        self.adjacentVertexList.append(vertex)

    def removeAdjacentVertex(self, vertex):
        if vertex in self.adjacentVertexList:
            self.adjacentVertexList.remove(vertex)

    def findAdjacentVertex(self, vertex):
        if vertex in self.adjacentVertexList:
            return True
        return False

    def draggingStatus(self):
        return self.dragging

    def draggingStart(self):
        self.dragging = True

    def draggingStop(self):
        self.dragging = False

    def collidePoint(self, x: int, y: int):
        dist_x = abs(self.x - x)
        dist_y = abs(self.y - y)

        if (dist_x <= VERTEX_RADIUS) and (dist_y <= VERTEX_RADIUS):
            return True
        return False

    def collide_vertex(self, vertex):
        center_x, center_y = vertex.getPos()
        dist_x = abs(self.x - center_x)
        dist_y = abs(self.y - center_y)

        if (dist_x <= 2 * VERTEX_RADIUS) and (dist_y <= 2 * VERTEX_RADIUS):
            return True
        return False
