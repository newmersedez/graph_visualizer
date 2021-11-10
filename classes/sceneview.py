from PyQt5 import QtCore, QtGui, QtWidgets
from utils.defines import *
from classes.vertex import *


class SceneView(QtWidgets.QGraphicsView):
    def __init__(self):
        super(SceneView, self).__init__()

        # Graph utils
        self._vertexList = list()
        self._vergeList = list()

        # Scene and View settings
        self._backgroundColor = FIELD_DARK_COLOR
        self._scene = QtWidgets.QGraphicsScene(self)
        self._scene.setSceneRect(0, 0, FIELD_WIDTH, FIELD_HEIGHT)
        self.setScene(self._scene)
        self.setFixedSize(FIELD_WIDTH, FIELD_HEIGHT)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setViewportUpdateMode(QtWidgets.QGraphicsView.SmartViewportUpdate)
        self.setStyleSheet('background-color: #151515;')
        self.setMouseTracking(True)
        self.setAcceptDrops(True)

    # def addVertex(self, x: int, y: int):
    #     print('add new item')
    #     vertex = Vertex(x - OFFSET, y - OFFSET, '1', VERTEX_COLOR)
    #     self._scene.addItem(vertex)
    #     self._vertexList.append(vertex)

    def addVertex(self):
        print('add new item')
        vertexList = self._scene.items()
        if len(vertexList) == 0:
            name = '1'
        else:
            name = str(int(vertexList[-1].getName()) + 1)

        vertex = Vertex(20, 20, name, VERTEX_COLOR)
        self._scene.addItem(vertex)
        self._vertexList.append(vertex)

    # def deleteVertex(self, item):
    #     print('delete vertex')
    #     self._vertexList.remove(item)
    #     self._scene.removeItem(item)

    def deleteVertex(self):
        print('delete vertex')
        vertexList = self._scene.items()
        if len(vertexList) != 0:
            self._vertexList.remove(vertexList[-1])
            self._scene.removeItem(vertexList[-1])


    def changeViewColor(self):
        if self._backgroundColor == FIELD_DARK_COLOR:
            self._backgroundColor = FIELD_BRIGHT_COLOR
            self.setStyleSheet('background-color: gray;')

        elif self._backgroundColor == FIELD_BRIGHT_COLOR:
            self._backgroundColor = FIELD_DARK_COLOR
            self.setStyleSheet('background-color: #151515;')

    # def mousePressEvent(self, event):
        pos_x, pos_y = event.pos().x(), event.pos().y()
        # if event.button() == QtCore.Qt.LeftButton:
        #     item = self._scene.itemAt(pos_x, pos_y, QtGui.QTransform())
        #
        #     if item is None:
        #         self._addVertex(pos_x, pos_y)
        #     else:
        #         item.setAcceptDrops(True)
        #
        # if event.button() == QtCore.Qt.RightButton:
        #     item = self._scene.itemAt(pos_x, pos_y, QtGui.QTransform())
        #
        #     if item is not None:
        #         self._deleteVertex(item)
