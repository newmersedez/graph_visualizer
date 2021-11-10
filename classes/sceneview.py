from PyQt5 import QtCore, QtGui, QtWidgets
from utils.defines import *


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

    def _addVertex(self, event, x: int, y: int):
        pass

    def _deleteVertex(self):
        pass

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            pos_x, pos_y = event.pos().x(), event.pos().y()
            item = self._scene.itemAt(pos_x, pos_y, QtGui.QTransform())
            if item is None:
                print('add new vertex')
                self._addVertex(event, pos_x, pos_y)

        elif event.button() == QtCore.Qt.RightButton:
            item = self._scene.itemAt(event.pos().x(), event.pos().y(), QtGui.QTransform())
            if item is not None:
                print('delete vertex')
                self._scene.removeItem(item)
