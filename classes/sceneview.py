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
        self.setStyleSheet('background-color: #151515;')
        self.setMouseTracking(True)

    def changeViewColor(self):
        if self._backgroundColor == FIELD_DARK_COLOR:
            self._backgroundColor = FIELD_BRIGHT_COLOR
            self.setStyleSheet('background-color: gray;')

        elif self._backgroundColor == FIELD_BRIGHT_COLOR:
            self._backgroundColor = FIELD_DARK_COLOR
            self.setStyleSheet('background-color: #151515;')

    def _addVertex(self, x: int, y: int):
        print('add new item')
        vertex = Vertex(x, y, '1', VERTEX_COLOR)
        self._scene.addItem(vertex)
        self._vertexList.append(vertex)

    def _deleteVertex(self, item):
        print('delete vertex')
        self._vertexList.remove(item)
        self._scene.removeItem(item)

    def mousePressEvent(self, event):
        pos_x, pos_y = event.pos().x(), event.pos().y()
        if event.button() == QtCore.Qt.LeftButton:
            item = self._scene.itemAt(pos_x, pos_y, QtGui.QTransform())

            if item is None:
                self._addVertex(pos_x, pos_y)

        elif event.button() == QtCore.Qt.RightButton:
            item = self._scene.itemAt(pos_x, pos_y, QtGui.QTransform())

            if item is not None:
                self._deleteVertex(item)
