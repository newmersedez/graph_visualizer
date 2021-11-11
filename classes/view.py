from PyQt5 import QtWidgets, QtGui, QtCore
from utils.defines import *
from classes.vertex import *
from classes.verge import *


class View(QtWidgets.QGraphicsView):
    def __init__(self):
        super().__init__()
        self._vertexList = list()
        self._vergeList = list()
        self.scene = QtWidgets.QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, FIELD_WIDTH, FIELD_HEIGHT)
        self.setStyleSheet('background-color: #202020;')
        self.setScene(self.scene)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setViewportUpdateMode(QtWidgets.QGraphicsView.FullViewportUpdate)
        self.setFixedSize(FIELD_WIDTH, FIELD_HEIGHT)

        self._start = None
        self._end = None

    def contextMenuEvent(self, e):
        pos = e.pos()
        mnu = QtWidgets.QMenu()
        mnu.addAction('Add vertex').setObjectName('add vertex')
        mnu.addAction('Delete vertex').setObjectName('delete vertex')
        mnu.addAction('Clear all').setObjectName('clear all')
        ret = mnu.exec_(self.mapToGlobal(pos))
        if not ret:
            return
        obj = ret.objectName()
        if obj == 'add vertex':
            if len(self._vertexList) == 0:
                name = 1
            else:
                name = str(int(self._vertexList[-1].getName()) + 1)
            item = Vertex(0, 0, name, VERTEX_COLOR)
            self._vertexList.append(item)
            self.scene.addItem(item)
            item.setPos(self.mapToScene(pos))

        elif obj == 'delete vertex':
            pos_x, pos_y = e.pos().x(), e.pos().y()
            item = self.scene.itemAt(pos_x, pos_y, QtGui.QTransform())
            if item is not None:
                self._vertexList.remove(item)
                self.scene.removeItem(item)

        elif obj == 'clear all':
            for item in self.scene.items():
                self.scene.removeItem(item)

    def resizeEvent(self, e):
        width, height = self.viewport().width(), self.viewport().height()
        self.setSceneRect(0, 0, width, height)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MiddleButton:
            pos_x, pos_y = event.pos().x(), event.pos().y()
            item = self.scene.itemAt(pos_x, pos_y, QtGui.QTransform())

            if item is not None:
                self._start = item
        super(View, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.MiddleButton:
            pos_x, pos_y = event.pos().x(), event.pos().y()
            item = self.scene.itemAt(pos_x, pos_y, QtGui.QTransform())

            if item is not None:
                self._end = item
                if self._start.type() == 4 and self._end.type() == 4:
                    verge = Verge(self._start, self._end)
                    self.scene.addItem(verge)
                    self._start = None
                    self._end = None
        super(View, self).mouseReleaseEvent(event)