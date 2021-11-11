from PyQt5 import QtWidgets, QtGui, QtCore
from utils.defines import *
from classes.vertex import *
from classes.verge import *


class View(QtWidgets.QGraphicsView):
    def __init__(self):
        super().__init__()

        # Graph cariables
        self._vertexList = list()
        self._vergeList = list()
        self._start = None
        self._end = None

        # Scene and view settings
        self._scene = QtWidgets.QGraphicsScene(self)
        self._scene.setSceneRect(0, 0, FIELD_WIDTH, FIELD_HEIGHT)
        self.setScene(self._scene)
        self.setFixedSize(FIELD_WIDTH, FIELD_HEIGHT)
        self.setStyleSheet('background-color: #202020;')
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setViewportUpdateMode(QtWidgets.QGraphicsView.FullViewportUpdate)

    def _addVertex(self, x, y):
        if len(self._vertexList) == 0:
            name = 1
        else:
            name = str(int(self._vertexList[-1].getName()) + 1)
        vertex = Vertex(0, 0, name, VERTEX_COLOR)

        self._vertexList.append(vertex)
        self._scene.addItem(vertex)
        vertex.setPos(self.mapToScene(x, y))

        print('after add vertex: ')
        for i in self._vertexList:
            print(i.getName())
        print('\n')

    def _removeVertex(self, vertex):
        for vert in self._vertexList:
            vert.removeAdjacentVertex(vertex)

        for verge in self._vergeList[:]:
            if (verge.getStartVertex() == vertex) or (verge.getEndVertex() == vertex):
                self._vergeList.remove(verge)
                self.scene().removeItem(verge)

        self._vertexList.remove(vertex)
        self._scene.removeItem(vertex)

        print('after remove vertex: ')
        for i in self._vertexList:
            print(i.getName())
        for i in self._vergeList:
            print(i.getStartVertex().getName(), ' -> ', i.getEndVertex().getName())
        print('\n')

    def _addVerge(self, startVertex, endVertex):
        verge = Verge(startVertex, endVertex)

        self._vergeList.append(verge)
        self._scene.addItem(verge)

        startVertex = verge.getStartVertex()
        endVertex = verge.getEndVertex()

        startVertex.addAdjacentVertex(endVertex)
        endVertex.addAdjacentVertex(startVertex)

        self._start = None
        self._end = None

        print('after add verge: ')
        for i in self._vergeList:
            print(i.getStartVertex().getName(), ' -> ', i.getEndVertex().getName())
        print('\n')

    def _removeVerge(self, item):
        startVertex = item.getStartVertex()
        endVertex = item.getEndVertex()

        startVertex.removeAdjacentVertex(endVertex)
        endVertex.removeAdjacentVertex(startVertex)
        self._vergeList.remove(item)
        self.scene().removeItem(item)

        print('after remove verge: ')
        for i in self._vergeList:
            print(i.getStartVertex().getName(), ' -> ', i.getEndVertex().getName())
        print('\n')

    def _clearScene(self):
        self._vertexList.clear()
        self._vergeList.clear()
        for item in self._scene.items():
            self._scene.removeItem(item)

        print('after clean all: ')
        for i in self._vertexList:
            print(i.getName())
        for i in self._vergeList:
            print(i.getStartVertex().getName(), ' -> ', i.getEndVertex().getName())
        print('\n')

    def contextMenuEvent(self, event):
        pos = event.pos()
        mnu = QtWidgets.QMenu()

        mnu.addAction('Add vertex').setObjectName('add vertex')
        mnu.addAction('Delete vertex').setObjectName('delete vertex')
        mnu.addAction('Delete verge').setObjectName('delete verge')
        mnu.addAction('Clear all').setObjectName('clear all')

        ret = mnu.exec_(self.mapToGlobal(pos))
        if not ret:
            return

        obj = ret.objectName()
        if obj == 'add vertex':
            pos_x, pos_y = event.pos().x(), event.pos().y()
            self._addVertex(pos_x, pos_y)

        elif obj == 'delete vertex':
            pos_x, pos_y = event.pos().x(), event.pos().y()
            item = self._scene.itemAt(pos_x, pos_y, QtGui.QTransform())
            if item is not None:
                if isinstance(item, Vertex):
                    self._removeVertex(item)

        elif obj == 'delete verge':
            pos_x, pos_y = event.pos().x(), event.pos().y()
            item = self._scene.itemAt(pos_x, pos_y, QtGui.QTransform())
            if item is not None:
                if isinstance(item, Verge):
                    self._removeVerge(item)

        elif obj == 'clear all':
            self._clearScene()

    def resizeEvent(self, event):
        width, height = self.viewport().width(), self.viewport().height()
        self.setSceneRect(0, 0, width, height)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MiddleButton:
            pos_x, pos_y = event.pos().x(), event.pos().y()
            item = self._scene.itemAt(pos_x, pos_y, QtGui.QTransform())
            if item is not None:
                self._start = item

        super(View, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.MiddleButton:
            pos_x, pos_y = event.pos().x(), event.pos().y()
            item = self._scene.itemAt(pos_x, pos_y, QtGui.QTransform())
            if item is not None:
                self._end = item
                if isinstance(self._start, Vertex) and isinstance(self._end, Vertex):
                    self._addVerge(self._start, self._end)

        super(View, self).mouseReleaseEvent(event)
