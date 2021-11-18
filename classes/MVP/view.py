# Presenter

from classes.MVP.graph import *


class View(QtWidgets.QGraphicsView):
    def __init__(self, window):
        super().__init__()

        # Graph variables
        self._mainWindow = window
        self._graph = Graph()
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

    def addGraph(self, graph: Graph):
        self.removeGraph()
        self._graph = graph
        
        vertexList = self._graph.getVertexList()
        vergeList = self._graph.getVergeList()
        
        for item in vertexList:
            self._scene.addItem(item)
            item.setPos(self.mapToScene(x, y))
        
        for item in vergeList:
            self._scene.addItem(item)

    def removeGraph(self):
        self._graph.clear()
        self._redrawScene()

    def _redrawScene(self):
        vertexList = self._graph.getVertexList()
        vergeList = self._graph.getVergeList()

        for item in self._scene.items():
            if not (item in vertexList) and not (item in vergeList):
                self._scene.removeItem(item)

    # Vertex methods
    def _createVertexName(self):
        vertexList = self._graph.getVertexList()

        if len(vertexList) == 0:
            name = '1'
        else:
            name = str(int(vertexList[-1].getName()) + 1)
        return name

    def _contextMenuAddVertex(self, x, y):
        name = self._createVertexName()
        vertex = Vertex(0, 0, name=name, color=VERTEX_COLOR)
        # vertex.setPos(self.mapToScene(x, y))

        self._graph.addVertex(vertex)
        self._scene.addItem(vertex)

    def _contextMenuRemoveVertex(self, vertex):
        self._graph.removeVertex(vertex)
        self._redrawScene()

    # Verge methods
    @staticmethod
    def _countVergeFactor(startVertex, endVertex):
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
        return factor

    def _createVergeName(self):
        vergeList = self._graph.getVergeList()

        if len(vergeList) == 0:
            name = '1'
        else:
            name = str(len(vergeList) + 1)
        return name

    def _contextMenuAddVerge(self, startVertex, endVertex):
        # Count bezier factor
        factor = self._countVergeFactor(startVertex, endVertex)

        # Create default name
        name = self._createVergeName()

        # Create verge
        verge = Verge(startVertex, endVertex, name, weight=1, direction=False, factor=factor)

        if startVertex == endVertex:
            startVertex.setLoop(value=True)

        self._graph.addVerge(verge)
        self._scene.addItem(verge)

    def _contextMenuToggleDirection(self):
        inputDialog = QtWidgets.QInputDialog(self)
        inputDialog.setInputMode(QtWidgets.QInputDialog.TextInput)
        inputDialog.setWindowTitle('Вкл/Выкл направление ребра')
        inputDialog.setStyleSheet('background-color: #303030; color: white;')
        inputDialog.setFont(QtGui.QFont('Arial', 15))
        inputDialog.setLabelText('Название ребра:')
        ok = inputDialog.exec_()
        name = inputDialog.textValue()

        if ok:
            verge = self._graph.findVergeByName(name)
            self._graph.toggleVergeDirection(verge)

    def _contextMenuSetWeight(self):
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
            verge = self._graph.findVergeByName(name)
            self._graph.setVergeWeight(verge, weight)

    def _contextMenuRemoveVerge(self):
        inputDialog = QtWidgets.QInputDialog(self)
        inputDialog.setInputMode(QtWidgets.QInputDialog.TextInput)
        inputDialog.setWindowTitle('Удаление ребра')
        inputDialog.setStyleSheet('background-color: #303030; color: white;')
        inputDialog.setFont(QtGui.QFont('Arial', 15))
        inputDialog.setLabelText('Название ребра:')
        ok = inputDialog.exec_()
        name = inputDialog.textValue()

        if ok:
            verge = self._graph.findVergeByName(name)
            self._graph.removeVerge(verge)
            self._redrawScene()

    # Utils
    def _contextMenuClearScene(self):
        self._graph.clear()
        self._redrawScene()

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
            self._contextMenuAddVertex(pos_x, pos_y)

        elif obj == 'delete vertex':
            pos_x, pos_y = event.pos().x(), event.pos().y()
            item = self._scene.itemAt(pos_x, pos_y, QtGui.QTransform())
            if item is not None:
                if isinstance(item, Vertex):
                    self._contextMenuRemoveVertex(item)

        elif obj == 'make loop':
            pos_x, pos_y = event.pos().x(), event.pos().y()
            item = self._scene.itemAt(pos_x, pos_y, QtGui.QTransform())
            if item is not None:
                if isinstance(item, Vertex):
                    if not item.isLoopExist():
                        item.setLoop(value=True)
                        self._contextMenuAddVerge(item, item)

        elif obj == 'toggle direction':
            self._contextMenuToggleDirection()

        elif obj == 'set weight':
            self._contextMenuSetWeight()

        elif obj == 'delete verge':
            self._contextMenuRemoveVerge()

        elif obj == 'clear all':
            self._contextMenuClearScene()

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
                        self._contextMenuAddVerge(self._start, self._end)
                        self._start = None
                        self._end = None

        super(View, self).mouseReleaseEvent(event)
