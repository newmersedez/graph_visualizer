from PyQt5 import QtWidgets, QtGui, QtCore
from utils.defines import *
from classes.vertex import *
from classes.verge import *
from classes.cache import *


class View(QtWidgets.QGraphicsView):
    def __init__(self, window):
        super().__init__()

        # Graph variables
        self._vertexList = list()
        self._vergeList = list()
        self._start = None
        self._end = None
        self._mainWindow = window

        # Scene and view settings
        self._scene = QtWidgets.QGraphicsScene(self)
        self._scene.setSceneRect(0, 0, FIELD_WIDTH, FIELD_HEIGHT)
        self.setScene(self._scene)
        self.setFixedSize(FIELD_WIDTH, FIELD_HEIGHT)
        self.setStyleSheet('background-color: #202020;')
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setViewportUpdateMode(QtWidgets.QGraphicsView.FullViewportUpdate)

    # Vertex methods
    def addVertex(self, x, y):
        if len(self._vertexList) == 0:
            name = '1'
        else:
            name = str(int(self._vertexList[-1].getName()) + 1)
        vertex = Vertex(0, 0, name, VERTEX_COLOR)

        self._vertexList.append(vertex)
        self._scene.addItem(vertex)
        vertex.setPos(self.mapToScene(x, y))

        # Update table
        self._mainWindow.updateAdjacentTable()

        # Update cache
        newCacheItem = CacheItem(self._vertexList, self._vergeList)
        self._mainWindow.getCache().updateCache(newCacheItem)

        # print('after add vertex: ')
        # for i in self._vertexList:
        #     print(i.getName())
        # print('\n')

    def removeVertex(self, vertex):
        for vert in self._vertexList:
            vert.removeAdjacentVertex(vertex)

        for verge in self._vergeList[:]:
            if (verge.getStartVertex() == vertex) or (verge.getEndVertex() == vertex):
                self._vergeList.remove(verge)
                self.scene().removeItem(verge)

        self._vertexList.remove(vertex)
        self._scene.removeItem(vertex)

        # Update table
        self._mainWindow.updateAdjacentTable()

        # Update cache
        newCacheItem = CacheItem(self._vertexList, self._vergeList)
        self._mainWindow.getCache().updateCache(newCacheItem)

        # print('after remove vertex: ')
        # for i in self._vertexList:
        #     print(i.getName())
        # for i in self._vergeList:
        #     print(i.getStartVertex().getName(), ' -> ', i.getEndVertex().getName())
        # print('\n')

    def findVertexByName(self, name):
        for vertex in self._vertexList:
            if vertex.getName() == name:
                return vertex
        return None

    # Verge methods
    def addVerge(self, startVertex, endVertex):
        endAdjVertexList = endVertex.getAdjacentVertexList()
        factor = 0
        for vertex in endAdjVertexList:
            if vertex == startVertex:
                factor += 1

        if factor > 0 and factor % 2 == 0:
            factor /= -2

        elif factor > 0 and factor % 2 != 0:
            factor = (factor + 1) / 2

        print('factor = ', factor)

        if len(self._vergeList) == 0:
            name = '1'
        else:
            name = str(len(self._vergeList) + 1)

        verge = Verge(startVertex, endVertex, name, factor=factor)

        self._vergeList.append(verge)
        self._scene.addItem(verge)

        startVertex = verge.getStartVertex()
        endVertex = verge.getEndVertex()

        startVertex.addAdjacentVertex(endVertex)
        endVertex.addAdjacentVertex(startVertex)

        self._start = None
        self._end = None

        # Update table
        self._mainWindow.updateAdjacentTable()

        # Update cache
        newCacheItem = CacheItem(self._vertexList, self._vergeList)
        self._mainWindow.getCache().updateCache(newCacheItem)

        # print('after add verge: ')
        # for i in self._vergeList:
        #     print(i.getStartVertex().getName(), ' -> ', i.getEndVertex().getName())
        # print('\n')

    def _findVergeByName(self, name):
        for verge in self._vergeList:
            if verge.getName() == name:
                return verge
        return None

    def findVerge(self, startVertex, endVertex):
        for verge in self._vergeList:
            if (verge.getStartVertex() == startVertex) and (verge.getEndVertex() == endVertex):
                return verge
        return None

    def toggleVergeDirection(self):
        inputDialog = QtWidgets.QInputDialog(self)
        inputDialog.setInputMode(QtWidgets.QInputDialog.TextInput)
        inputDialog.setWindowTitle('Вкл/Выкл направление ребра')
        inputDialog.setStyleSheet('background-color: #303030; color: white;')
        inputDialog.setFont(QtGui.QFont('Arial', 15))
        inputDialog.setLabelText('Название ребра:')
        ok = inputDialog.exec_()
        name = inputDialog.textValue()

        if ok:
            verge = self._findVergeByName(name)
            if verge is not None:
                verge.toggleDirection()

        # Update table
        self._mainWindow.updateAdjacentTable()

        # Update cache
        newCacheItem = CacheItem(self._vertexList, self._vergeList)
        self._mainWindow.getCache().updateCache(newCacheItem)

    def setVergeWeight(self):
        inputDialog = QtWidgets.QDialog(self)
        inputDialog.setWindowTitle('Установить вес ребра')
        inputDialog.setStyleSheet('background-color: #303030; color: white;')
        inputDialog.setFont(QtGui.QFont('Arial', 15))
        form = QtWidgets.QFormLayout(inputDialog)

        textBox1 = QtWidgets.QLineEdit()
        form.addRow(QtWidgets.QLabel('Название ребра'))
        form.addRow(textBox1)

        textBox2 = QtWidgets.QSpinBox()
        textBox2.setMaximum(10000)
        form.addRow(QtWidgets.QLabel('Вес ребра'))
        form.addRow(textBox2)

        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        form.addRow(buttonBox)
        buttonBox.accepted.connect(inputDialog.accept)
        buttonBox.rejected.connect(inputDialog.reject)

        ok = inputDialog.exec_()

        if ok:
            name = textBox1.text()
            weight = textBox2.text()
            verge = self._findVergeByName(name)
            if verge is not None:
                verge.setWeight(weight)

        # Update cache
        newCacheItem = CacheItem(self._vertexList, self._vergeList)
        self._mainWindow.getCache().updateCache(newCacheItem)

    def removeVerge(self):
        inputDialog = QtWidgets.QInputDialog(self)
        inputDialog.setInputMode(QtWidgets.QInputDialog.TextInput)
        inputDialog.setWindowTitle('Удаление ребра')
        inputDialog.setStyleSheet('background-color: #303030; color: white;')
        inputDialog.setFont(QtGui.QFont('Arial', 15))
        inputDialog.setLabelText('Название ребра:')
        ok = inputDialog.exec_()
        name = inputDialog.textValue()

        if ok:
            verge = self._findVergeByName(name)
            if verge is not None:
                startVertex = verge.getStartVertex()
                endVertex = verge.getEndVertex()

                startVertex.removeAdjacentVertex(endVertex)
                endVertex.removeAdjacentVertex(startVertex)
                self._vergeList.remove(verge)
                self.scene().removeItem(verge)

        # Update table
        self._mainWindow.updateAdjacentTable()

        # Update cache
        newCacheItem = CacheItem(self._vertexList, self._vergeList)
        self._mainWindow.getCache().updateCache(newCacheItem)

        # print('after remove verge: ')
        # for i in self._vergeList:
        #     print(i.getStartVertex().getName(), ' -> ', i.getEndVertex().getName())
        # print('\n')

    # Utils
    def clearScene(self):
        self._vertexList.clear()
        self._vergeList.clear()
        for item in self._scene.items():
            self._scene.removeItem(item)

        # Update table
        self._mainWindow.updateAdjacentTable()

        # Update cache
        newCacheItem = CacheItem(self._vertexList, self._vergeList)
        self._mainWindow.getCache().updateCache(newCacheItem)

        # print('after clean all: ')
        # for i in self._vertexList:
        #     print(i.getName())
        # for i in self._vergeList:
        #     print(i.getStartVertex().getName(), ' -> ', i.getEndVertex().getName())
        # print('\n')

    def getScene(self):
        return self.scene()

    def getVertexList(self):
        return self._vertexList

    def getVergeList(self):
        return self._vergeList

    def setVertexList(self, vertexList):
        self._vertexList = vertexList.copy()

    def setVergeList(self, vergeList):
        self._vergeList = vergeList.copy()

    # Events
    def contextMenuEvent(self, event):
        pos = event.pos()
        mnu = QtWidgets.QMenu()

        mnu.addSection('Вершина:')
        mnu.addAction('Добавить вершину').setObjectName('add vertex')
        mnu.addAction('Удалить вершину').setObjectName('delete vertex')

        mnu.addSection('Ребро:')
        mnu.addAction('Вкл/Выкл направление ребра...').setObjectName('toggle direction')
        mnu.addAction('Установить вес ребра...').setObjectName('set weight')
        mnu.addAction('Удалить ребро...').setObjectName('delete verge')

        mnu.addSection('Дополнительно:')
        mnu.addAction('Очистить экран').setObjectName('clear all')

        ret = mnu.exec_(self.mapToGlobal(pos))
        if not ret:
            return

        obj = ret.objectName()
        if obj == 'add vertex':
            pos_x, pos_y = event.pos().x(), event.pos().y()
            self.addVertex(pos_x, pos_y)

        elif obj == 'delete vertex':
            pos_x, pos_y = event.pos().x(), event.pos().y()
            item = self._scene.itemAt(pos_x, pos_y, QtGui.QTransform())
            if item is not None:
                if isinstance(item, Vertex):
                    self.removeVertex(item)

        elif obj == 'toggle direction':
            pos_x, pos_y = event.pos().x(), event.pos().y()
            item = self._scene.itemAt(pos_x, pos_y, QtGui.QTransform())
            if item is not None:
                if isinstance(item, Vertex):
                    self.toggleVergeDirection()

        elif obj == 'set weight':
            pos_x, pos_y = event.pos().x(), event.pos().y()
            item = self._scene.itemAt(pos_x, pos_y, QtGui.QTransform())
            if item is not None:
                if isinstance(item, Vertex):
                    self.setVergeWeight()

        elif obj == 'delete verge':
            pos_x, pos_y = event.pos().x(), event.pos().y()
            item = self._scene.itemAt(pos_x, pos_y, QtGui.QTransform())
            if item is not None:
                if isinstance(item, Vertex):
                    self.removeVerge()

        elif obj == 'clear all':
            self.clearScene()

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
                    self.addVerge(self._start, self._end)

        super(View, self).mouseReleaseEvent(event)
