from PyQt5 import QtWidgets, QtGui, QtCore
from utils.defines import *
from classes.vertex import *
from classes.verge import *


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

        print('after add vertex: ')
        for i in self._vertexList:
            print(i.getName())
        print('\n')

    def removeVertex(self, vertex):
        for vert in self._vertexList:
            vert.removeAdjacentVertex(vertex)

        for verge in self._vergeList[:]:
            if (verge.getStartVertex() == vertex) or (verge.getEndVertex() == vertex):
                self._vergeList.remove(verge)
                self._scene.removeItem(verge)

        self._vertexList.remove(vertex)
        self._scene.removeItem(vertex)

        # print('after remove vertex: ')
        # for i in self._vertexList:
        #     print(i.getName())
        # for i in self._vergeList:
        #     print(i.getStartVertex().getName(), ' -> ', i.getEndVertex().getName())
        # print('\n')
        print("asdbewfaewfrasdfasdfasdf")

    def findVertexByName(self, name):
        for vertex in self._vertexList:
            if vertex.getName() == name:
                return vertex

    # Verge methods
    # SEG FAULT HERE
    def addVerge(self, startVertex, endVertex, weight=1, direction=False):
        # Count bezier factor
        if startVertex.getName() > endVertex.getName():
            factorStart = startVertex
            factorEnd = endVertex
        else:
            factorStart = endVertex
            factorEnd = startVertex

        endAdjVertexList = factorEnd.getAdjacentVertexList().copy()
        startAdjVertexList = factorStart.getAdjacentVertexList().copy()

        factor = 0
        for vertex in endAdjVertexList:
            if vertex == factorStart:
                factor += 1
                for i in range(startAdjVertexList.count(factorEnd)):
                    startAdjVertexList.remove(factorEnd)
        for vertex in startAdjVertexList:
            if vertex == factorEnd:
                factor += 1
        if factor > 0 and factor % 2 == 0:
            factor /= -2
        elif factor > 0 and factor % 2 != 0:
            factor = (factor + 1) / 2
        if startVertex.getName() > endVertex.getName():
            factor = -factor

        # Create default name
        if len(self._vergeList) == 0:
            name = '1'
        else:
            name = str(len(self._vergeList) + 1)

        verge = Verge(startVertex, endVertex, name, weight=weight, direction=direction, factor=factor)

        if startVertex == endVertex:
            startVertex.setLoop(value=True)

        self._vergeList.append(verge)
        self._scene.addItem(verge)
        startVertex.addAdjacentVertex(endVertex)
        endVertex.addAdjacentVertex(startVertex)
        self._start = None
        self._end = None

        print('after add verge: ')
        for i in self._vergeList:
            print(i.getStartVertex().getName(), ' -> ', i.getEndVertex().getName())
        print('\n')

    def _findVergeByName(self, name):
        for verge in self._vergeList:
            if verge.getName() == name:
                return verge

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

                if startVertex == endVertex:
                    startVertex.setLoop(value=False)

                startVertex.removeAdjacentVertex(endVertex)
                endVertex.removeAdjacentVertex(startVertex)
                self._vergeList.remove(verge)
                self._scene.removeItem(verge)

        print('after remove verge: ')
        for i in self._vergeList:
            print(i.getStartVertex().getName(), ' -> ', i.getEndVertex().getName())
        print('\n')

    # Utils
    def clearScene(self):
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

    def getScene(self):
        return self._scene

    def getVertexList(self):
        return self._vertexList

    def getVergeList(self):
        return self._vergeList


    # Events
    def contextMenuEvent(self, event):
        pos = event.pos()
        mnu = QtWidgets.QMenu()

        mnu.addSection('Вершина:')
        mnu.addAction('Добавить вершину').setObjectName('add vertex')
        mnu.addAction('Создать петлю').setObjectName('make loop')
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
                    print('event = ', event.pos().x(), event.pos().y(), 'item = ', item.pos().x(), item.pos().y())
                    self.removeVertex(item)

        elif obj == 'make loop':
            pos_x, pos_y = event.pos().x(), event.pos().y()
            item = self._scene.itemAt(pos_x, pos_y, QtGui.QTransform())
            if item is not None:
                if isinstance(item, Vertex):
                    if not item.isLoopExist():
                        item.setLoop(value=True)
                        self.addVerge(item, item)

        elif obj == 'toggle direction':
            self.toggleVergeDirection()

        elif obj == 'set weight':
            self.setVergeWeight()

        elif obj == 'delete verge':
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
                    if self._start != self._end:
                        self.addVerge(self._start, self._end)

        super(View, self).mouseReleaseEvent(event)
