# Presenter

from classes.cache.cache import *
from algorithms.bfs import *
import time

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
        self.setScene(self._scene)
        self.setStyleSheet('background-color: #202020;')
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setViewportUpdateMode(QtWidgets.QGraphicsView.FullViewportUpdate)
        self.setMouseTracking(True)

    def viewBFS(self):
        inputDialog = QtWidgets.QInputDialog(self)
        inputDialog.setInputMode(QtWidgets.QInputDialog.TextInput)
        inputDialog.setWindowTitle('BFS')
        inputDialog.setStyleSheet('background-color: #303030; color: white;')
        inputDialog.setFont(QtGui.QFont('Arial', 15))
        inputDialog.setLabelText('Выберите начальную вершину обхода:')
        ok = inputDialog.exec_()
        name = inputDialog.textValue()

        if ok:
            vertex = self._graph.findVertexByName(name)
            if vertex is not None:
                bfs(self._graph, vertex)

    def addGraph(self, graph: Graph):
        for item in self._scene.items():
            self._scene.removeItem(item)

        self._graph = graph
        self._redrawScene()
        
        vertexList = self._graph.getVertexList()
        edgeList = self._graph.getEdgeList()

        for item in vertexList:
            self._scene.addItem(item)
        
        for item in edgeList:
            self._scene.addItem(item)

        # Update adjacent table widget
        self._mainWindow.updateAdjacentTable()

    def getGraph(self):
        return self._graph

    def _redrawScene(self):
        vertexList = self._graph.getVertexList()
        edgeList = self._graph.getEdgeList()

        for item in self._scene.items():
            if not (item in vertexList) and not (item in edgeList):
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
        vertex.setPos(self.mapToScene(x, y))

        self._graph.addVertex(vertex)
        self._scene.addItem(vertex)

        # Update adjacent table widget
        self._mainWindow.updateAdjacentTable()

        # Update cache
        cacheItem = CacheItem(self._graph)
        self._mainWindow.getCache().updateCache(cacheItem)

    def _contextMenuRemoveVertex(self, vertex):
        self._graph.removeVertex(vertex)
        self._redrawScene()

        # Update adjacent table widget
        self._mainWindow.updateAdjacentTable()

        # Update cache
        cacheItem = CacheItem(self._graph)
        self._mainWindow.getCache().updateCache(cacheItem)

    # Edge methods
    @staticmethod
    def countEdgeFactor(startVertex, endVertex):
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

    def _createEdgeName(self):
        edgeList = self._graph.getEdgeList()

        if len(edgeList) == 0:
            name = '1'
        else:
            name = str(len(edgeList) + 1)
        return name

    def _contextMenuAddEdge(self, startVertex, endVertex):
        # Count bezier factor
        factor = self.countEdgeFactor(startVertex, endVertex)

        # Create default name
        name = self._createEdgeName()

        # Create edge
        edge = Edge(startVertex, endVertex, name, weight=1, direction=False, factor=factor)

        if startVertex == endVertex:
            startVertex.setLoop(value=True)

        self._graph.addEdge(edge)
        self._scene.addItem(edge)

        # Update adjacent table widget
        self._mainWindow.updateAdjacentTable()

        # Update cache
        cacheItem = CacheItem(self._graph)
        self._mainWindow.getCache().updateCache(cacheItem)

    def _contextMenuToggleDirection(self):
        inputDialog = QtWidgets.QInputDialog(self)
        inputDialog.setInputMode(QtWidgets.QInputDialog.TextInput)
        inputDialog.setWindowTitle('Вкл/Выкл направление ребра')

        if self._mainWindow.getTheme():
            inputDialog.setStyleSheet('background-color: #303030; color: white;')
        else:
            inputDialog.setStyleSheet('background-color: white; color: black;')

        inputDialog.setFont(QtGui.QFont('Arial', 15))
        inputDialog.setLabelText('Название ребра:')
        ok = inputDialog.exec_()
        name = inputDialog.textValue()

        if ok:
            edge = self._graph.findEdgeByName(name)
            self._graph.toggleEdgeDirection(edge)

            # Update adjacent table widget
            self._mainWindow.updateAdjacentTable()

            # Update cache
            cacheItem = CacheItem(self._graph)
            self._mainWindow.getCache().updateCache(cacheItem)

    def _contextMenuSetWeight(self):
        inputDialog = QtWidgets.QDialog(self)
        inputDialog.setWindowTitle('Установить вес ребра')
        inputDialog.setFont(QtGui.QFont('Arial', 15))

        if self._mainWindow.getTheme():
            inputDialog.setStyleSheet('background-color: #303030; color: white;')
        else:
            inputDialog.setStyleSheet('background-color: white; color: black;')

        form = QtWidgets.QFormLayout(inputDialog)

        textBox1 = QtWidgets.QLineEdit()
        form.addRow(QtWidgets.QLabel('Название ребра'))
        form.addRow(textBox1)

        textBox2 = QtWidgets.QSpinBox()
        textBox2.setMinimum(1)
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
            edge = self._graph.findEdgeByName(name)
            self._graph.setEdgeWeight(edge, weight)

            # Update adjacent table widget
            self._mainWindow.updateAdjacentTable()

            # Update cache
            cacheItem = CacheItem(self._graph)
            self._mainWindow.getCache().updateCache(cacheItem)

    def _contextMenuRemoveEdge(self):
        inputDialog = QtWidgets.QInputDialog(self)
        inputDialog.setInputMode(QtWidgets.QInputDialog.TextInput)
        inputDialog.setWindowTitle('Удаление ребра')
        inputDialog.setFont(QtGui.QFont('Arial', 15))
        inputDialog.setLabelText('Название ребра:')

        if self._mainWindow.getTheme():
            inputDialog.setStyleSheet('background-color: #303030; color: white;')
        else:
            inputDialog.setStyleSheet('background-color: white; color: black;')

        ok = inputDialog.exec_()
        name = inputDialog.textValue()

        if ok:
            edge = self._graph.findEdgeByName(name)
            self._graph.removeEdge(edge)
            self._redrawScene()

            # Update adjacent table widget
            self._mainWindow.updateAdjacentTable()

            # Update cache
            cacheItem = CacheItem(self._graph)
            self._mainWindow.getCache().updateCache(cacheItem)

    # Utils
    def _contextMenuClearScene(self):
        self._graph.clear()
        self._scene.clear()

        # Update adjacent table widget
        self._mainWindow.updateAdjacentTable()

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
        mnu.addAction('Удалить ребро...').setObjectName('delete edge')

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
                        self._contextMenuAddEdge(item, item)

        elif obj == 'toggle direction':
            self._contextMenuToggleDirection()

        elif obj == 'set weight':
            self._contextMenuSetWeight()

        elif obj == 'delete edge':
            self._contextMenuRemoveEdge()

        elif obj == 'clear all':
            self._contextMenuClearScene()

    def resizeEvent(self, event):
        width, height = self.viewport().width(), self.viewport().height()
        self.setSceneRect(0, 0, width, height)

        for item in self._scene.items():
            if isinstance(item, Vertex):
                x, y = item.getPos()
                x = max(min(x, self.width() - VERTEX_SIZE), 0)
                y = max(min(y, self.height() - VERTEX_SIZE), 0)
                item.setPos(self.mapToScene(x, y))

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
                        self._contextMenuAddEdge(self._start, self._end)
                        self._start = None
                        self._end = None

        super(View, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            cordX, cordY = event.pos().x(), event.pos().y()
            item = self._scene.itemAt(cordX, cordY, QtGui.QTransform())
            if item is not None:
                if isinstance(item, Vertex):
                    x, y = item.getPos()
                    x = max(min(x, self.width() - VERTEX_SIZE), 0)
                    y = max(min(y, self.height() - VERTEX_SIZE), 0)
                    item.setPos(self.mapToScene(x, y))
                    print(x, y)
                    # if (x < 0 or x > self.width() - VERTEX_SIZE) or (y < 0 or y > self.height() - VERTEX_SIZE):
                    #     print('OUT')
        super(View, self).mouseMoveEvent(event)
