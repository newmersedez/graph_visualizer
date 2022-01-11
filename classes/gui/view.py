# Presenter

from classes.cache.cache import *
from algorithms.bfs import *
from algorithms.complete import *
from algorithms.kruskal import *
from algorithms.colorize import *
from algorithms.dijkstra import *
from algorithms.min_cycle import *
from algorithms.astar import *
from algorithms.best_first import *
from algorithms.isomorphism import *
from utils.colorpalletes import *
from algorithms.get_weight_vertex import *
from algorithms.connected import *
from algorithms.weddings import *
from algorithms.graph_from_vector import *
from algorithms.tsp import *

import main
import sip


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
        self.setStyleSheet(FIELD_DARK)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setViewportUpdateMode(QtWidgets.QGraphicsView.FullViewportUpdate)
        self.setMouseTracking(True)

    # ALGOS
    def viewTSP(self):
        inputDialog = QtWidgets.QInputDialog(self)
        inputDialog.setInputMode(QtWidgets.QInputDialog.TextInput)
        inputDialog.setWindowTitle('TSP')
        inputDialog.setStyleSheet(WINDOW_DARK)
        inputDialog.setFont(QtGui.QFont('Arial', 15))
        inputDialog.setLabelText('Выберите начальную вершину:')
        ok = inputDialog.exec_()
        name = inputDialog.textValue()

        if ok:
            vertex = self._graph.findVertexByName(name)
            if vertex is not None:
                self.setDefaults()
                # dijkstra_algo_for_tsp(self._graph, vertex)
                if tspCheckGraph(self._graph, vertex):
                    path, len_of_path = setVisualForTSP(self._graph, vertex)
                    messageDialod = QtWidgets.QMessageBox(self)
                    messageDialod.setWindowTitle("Коммивояжер")
                    messageDialod.setStyleSheet(WINDOW_DARK)
                    messageDialod.setText(f'длина пути - {len_of_path}, путь - {[i.getName() for i in path]}')
                    messageDialod.exec_()
                else:
                    messageDialod = QtWidgets.QMessageBox(self)
                    messageDialod.setWindowTitle("Коммивояжер")
                    messageDialod.setStyleSheet(WINDOW_DARK)
                    messageDialod.setText('Граф должен быть неориентированным и связным, к тому же мультиграфы не поддерживаются')
                    messageDialod.exec_()




    def viewBFS(self):
        inputDialog = QtWidgets.QInputDialog(self)
        inputDialog.setInputMode(QtWidgets.QInputDialog.TextInput)
        inputDialog.setWindowTitle('ЛР №2. Поиска пути в ширину')
        inputDialog.setStyleSheet(WINDOW_DARK)
        inputDialog.setFont(QtGui.QFont('Arial', 15))
        inputDialog.setLabelText('Выберите начальную вершину обхода:')
        ok = inputDialog.exec_()
        name = inputDialog.textValue()

        if ok:
            vertex = self._graph.findVertexByName(name)
            if vertex is not None:
                self.setDefaults()
                setVisualForBFS(bfs(self._graph, vertex))

    def viewComp(self):
        matrix = self._graph.getAdjacentMatrix()
        isfullgraph = 0
        old_edge_list = []
        for i in self._graph.getEdgeList():
            old_edge_list.append(i)
        for x in range(len(matrix)):
            for y in range(len(matrix[x])):
                if (matrix[x][y] >= 1 and matrix[y][x] == 0) or (matrix[y][x] >= 1 and matrix[x][y] == 0):
                    matrix[y][x] = matrix[x][y] = 1
                if matrix[x][y] >= 1:
                    isfullgraph += 1
        n = (len(matrix)*(len(matrix)-1))
        #print(matrix)
        if isfullgraph >= (len(matrix)*(len(matrix)-1)):
            messageDialod = QtWidgets.QMessageBox(self)
            messageDialod.setWindowTitle("ЛР №9. Дополнение графа")
            messageDialod.setStyleSheet(WINDOW_DARK)
            messageDialod.setText('Текущий граф является полным.       ')
            messageDialod.exec_()
        else:
            # setTextelf.setDefaults()
            # editing_graph = self.copyGraph(self._graph)
            cpy = self.copyGraph(self._graph)
            setVisualForComplete(cpy, complete(cpy))
            # for edge in old_edge_list:
            #     tmp = editing_graph.findEdgeByVertexes(edge.getStartVertex(), edge.getEndVertex())
            #     editing_graph.removeEdge(tmp)
            self.addGraph(cpy)

    def viewKruskal(self):
        self.setDefaults()
        kruskal(self._graph)

    def viewConnected(self):
        self.setDefaults()
        setVisualForConnected(self._graph)

    def viewColorize(self):
        self.setDefaults()
        setVisualForColorize(colorize(self._graph))

    def viewCycle(self):
        self.setDefaults()
        if is_search_min_cycle_applicable(self._graph):
            search_min_cycle(self._graph)
        else:
            messageDialod = QtWidgets.QMessageBox(self)
            messageDialod.setWindowTitle("Ошибка")
            messageDialod.setStyleSheet(WINDOW_DARK)
            messageDialod.setText('Граф должен быть связным и ненаправленным')
            messageDialod.exec_()

    def viewDijkstra(self):
        inputDialog = QtWidgets.QInputDialog(self)
        inputDialog.setInputMode(QtWidgets.QInputDialog.TextInput)
        inputDialog.setWindowTitle('ЛР №4. Алгоритм Дейкстры')
        inputDialog.setStyleSheet(WINDOW_DARK)
        inputDialog.setFont(QtGui.QFont('Arial', 15))
        inputDialog.setLabelText('Выберите начальную вершину:')
        ok = inputDialog.exec_()
        name = inputDialog.textValue()

        if ok:
            vertex = self._graph.findVertexByName(name)
            if vertex is not None:
                self.setDefaults()
                setVisualForDijkstra(dijkstra_algo(self._graph, vertex))

    def viewFromVector(self):  # Rina
        self.setDefaults()
        inputDialog1 = QtWidgets.QInputDialog(self)
        inputDialog1.setInputMode(QtWidgets.QInputDialog.TextInput)
        inputDialog1.setWindowTitle('ЛР №11 - Восстановление графа из вектора')
        inputDialog1.setStyleSheet(WINDOW_DARK)
        inputDialog1.setFont(QtGui.QFont('Arial', 15))
        inputDialog1.setLabelText('Задайте вектор в формате:  1,2,3')
        ok = inputDialog1.exec_()
        inp = inputDialog1.textValue()
        vect = inp.split(',')

        messageDialod = QtWidgets.QMessageBox(self)
        messageDialod.setWindowTitle("ЛР №11 - Восстановление графа из вектора")
        messageDialod.setStyleSheet(WINDOW_DARK)
        messageDialod.setText('Текущий граф будет стёрт, продолжить?       ')
        messageDialod.exec()
        if ok:
            self._scene.clear()
            self.addGraph(Graph())
            for i in range(0, len(vect)):
                cordX = random.randint(0, FIELD_WIDTH - VERTEX_SIZE)
                cordY = random.randint(0, FIELD_HEIGHT - VERTEX_SIZE)
                self._contextMenuAddVertex(cordX, cordY)
            cpy = self.copyGraph(self._graph)

            ispossible = setVisualForVector(cpy, graphFromVector(self, cpy, vect))  # 4,4,3,3,3,2,2,1

            self.addGraph(cpy)
            extra_ideal_check(self._graph, False)

            if ispossible is False:
                self._scene.clear()
                self.addGraph(Graph())
                messageDialod = QtWidgets.QMessageBox(self)
                messageDialod.setWindowTitle("ЛР №11 - Восстановление графа из вектора")
                messageDialod.setStyleSheet(WINDOW_DARK)
                messageDialod.setText('Для такого вектора графа не существует.       ')
                messageDialod.exec()

    def viewIdeal(self):  # Rina
        self.setDefaults()
        text = extra_ideal_check(self._graph, True)
        messageDialod = QtWidgets.QMessageBox(self)
        messageDialod.setWindowTitle("ЛР №11.1 - Проверка на совершенство и экстримальность")
        messageDialod.setStyleSheet(WINDOW_DARK)
        messageDialod.setText(text)
        messageDialod.exec()

    def viewAStar(self):
        inputDialog = QtWidgets.QInputDialog(self)
        inputDialog.setInputMode(QtWidgets.QInputDialog.TextInput)
        inputDialog.setWindowTitle('A*')
        inputDialog.setStyleSheet(WINDOW_DARK)
        inputDialog.setFont(QtGui.QFont('Arial', 15))
        inputDialog.setLabelText('Выберите начальную вершину:')
        ok = inputDialog.exec_()
        name = inputDialog.textValue()

        inputDialog.setLabelText('Выберите конечную вершину:')
        ok2 = inputDialog.exec_()
        name2 = inputDialog.textValue()

        if ok and ok2:
            begin_vertex = self._graph.findVertexByName(name)
            end_vertex = self._graph.findVertexByName(name2)
            if begin_vertex is not None and end_vertex is not None:
                self.setDefaults()
                setVisualForAStar(astar(self._graph, begin_vertex, end_vertex))


    def viewMarrige(self):  # Rina
        matrix = self._graph.getAdjacentMatrix()
        ismarrige = wedding(self._graph)
        if ismarrige is None:
            messageDialod = QtWidgets.QMessageBox(self)
            messageDialod.setWindowTitle("ЛР №16. Задача о свадьбах")
            messageDialod.setStyleSheet(WINDOW_DARK)
            messageDialod.setText('Граф задан не верно для данной задачи       ')
            messageDialod.exec()
        else:
            if ismarrige is True:
                messageDialodITrue = QtWidgets.QMessageBox(self)
                messageDialodITrue.setWindowTitle("ЛР №16. Задача о свадьбах")
                messageDialodITrue.setStyleSheet(WINDOW_DARK)
                messageDialodITrue.setText('Задача о свадьбах имеет решение!       ')
                messageDialodITrue.exec()
            elif ismarrige is False:
                messageDialodIFaulse = QtWidgets.QMessageBox(self)
                messageDialodIFaulse.setWindowTitle("ЛР №16. Задача о свадьбах")
                messageDialodIFaulse.setStyleSheet(WINDOW_DARK)
                messageDialodIFaulse.setText('Задача о свадьбах не имеет решения на текущем графе       ')
                messageDialodIFaulse.exec()
            else:
                setVisualForWedding(ismarrige)


    def viewBestFirst(self):
        inputDialog = QtWidgets.QInputDialog(self)
        inputDialog.setInputMode(QtWidgets.QInputDialog.TextInput)
        inputDialog.setWindowTitle('Best First')
        inputDialog.setStyleSheet(WINDOW_DARK)
        inputDialog.setFont(QtGui.QFont('Arial', 15))
        inputDialog.setLabelText('Выберите начальную вершину:')
        ok = inputDialog.exec_()
        name = inputDialog.textValue()

        inputDialog.setLabelText('Выберите конечную вершину:')
        ok2 = inputDialog.exec_()
        name2 = inputDialog.textValue()

        if ok and ok2:
            begin_vertex = self._graph.findVertexByName(name)
            end_vertex = self._graph.findVertexByName(name2)
            if begin_vertex is not None and end_vertex is not None:
                self.setDefaults()
                setVisualForBestFirst(best_first_search(self._graph, begin_vertex, end_vertex))

    def viewWeight(self):
        getWeightVertex(self._graph)
        getRadiusDiameter(self._graph)
        getVectDegree(self._graph)

    def viewIso(self):  # Rina
        matrix = self._graph.getAdjacentMatrix()
        isIsomorph = isomorph(self._graph)
        if isIsomorph is None:
            messageDialod = QtWidgets.QMessageBox(self)
            messageDialod.setWindowTitle("ЛР №7. Изоморфизм графа")
            messageDialod.setStyleSheet(WINDOW_DARK)
            messageDialod.setText('Задан один/более двух подграфов.       ')
            messageDialod.exec()
        else:
            if isIsomorph is True:
                messageDialodITrue = QtWidgets.QMessageBox(self)
                messageDialodITrue.setWindowTitle("ЛР №7. Изоморфизм графа")
                messageDialodITrue.setStyleSheet(WINDOW_DARK)
                messageDialodITrue.setText('Графы изоморфны.       ')
                messageDialodITrue.exec()
            else:
                messageDialodIFaulse = QtWidgets.QMessageBox(self)
                messageDialodIFaulse.setWindowTitle("ЛР №7. Изоморфизм графа")
                messageDialodIFaulse.setStyleSheet(WINDOW_DARK)
                messageDialodIFaulse.setText('Графы не изоморфны.       ')
                messageDialodIFaulse.exec()

    def setDefaults(self):
        for item in self._graph.getVertexList():
            item.setColor(VERTEX_COLOR)
            item.setServiceValue("")
        for item in self._graph.getEdgeList():
            item.setColor(QtCore.Qt.white)
        self._scene.update()

    def addGraph(self, graph: Graph):
        self._scene.clear()

        self._graph = graph

        vertexList = self._graph.getVertexList()
        edgeList = self._graph.getEdgeList()

        for item in vertexList:
            if not sip.isdeleted(item):
                self._scene.addItem(item)
        
        for item in edgeList:
            if not sip.isdeleted(item) and \
                    not (sip.isdeleted(item.getStartVertex())) and \
                    not (sip.isdeleted(item.getEndVertex())):
                self._scene.addItem(item)
        self._scene.update()

        # Update adjacent table widget
        self._mainWindow.updateAdjacentTable()

    def getGraph(self):
        return self._graph

    def copyGraph(self, srcGraph: Graph):
        graph = Graph(directed=srcGraph.isDirected(), weighted=srcGraph.isWeighted())

        for item in srcGraph.getVertexList():
            vertex = Vertex(0, 0, name=item.getName(), color=item.getColor())
            x, y = item.getPos()

            vertex.setPos(self.mapToScene(x, y))
            graph.addVertex(vertex)

        for item in srcGraph.getEdgeList():
            startVertex = graph.findVertexByName(item.getStartVertex().getName())
            endVertex = graph.findVertexByName(item.getEndVertex().getName())

            edge = Edge(startVertex, endVertex, name=item.getName(), weight=item.getWeight(),
                        direction=item.isDirected(), factor=item.getFactor())

            graph.addEdge(edge)
        return graph

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

        self._scene.addItem(vertex)
        self._graph.addVertex(vertex)
        self._scene.update()

        # Update adjacent table widget
        self._mainWindow.updateAdjacentTable()

        # Update cache
        self._mainWindow.getCache().updateCache(self.copyGraph(self._graph))

    def _contextMenuRemoveVertex(self, vertex):
        self._graph.removeVertex(vertex)
        redrawGraph = self.copyGraph(self._graph)
        self._scene.clear()

        self._graph = redrawGraph
        for item in self._graph.getVertexList():
            self._scene.addItem(item)
            self._scene.update()

        for item in self._graph.getEdgeList():
            self._scene.addItem(item)
            self._scene.update()

        # Update adjacent table widget
        self._mainWindow.updateAdjacentTable()

        # Update cache
        self._mainWindow.getCache().updateCache(self.copyGraph(self._graph))

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
            name = str(int(edgeList[-1].getName()) + 1)
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

        self._scene.addItem(edge)
        self._graph.addEdge(edge)
        self._scene.update()

        # Update adjacent table widget
        self._mainWindow.updateAdjacentTable()

        # Update cache
        self._mainWindow.getCache().updateCache(self.copyGraph(self._graph))

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
            self._scene.update()

            # Update adjacent table widget
            self._mainWindow.updateAdjacentTable()

            # Update cache
            self._mainWindow.getCache().updateCache(self.copyGraph(self._graph))

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
            weight = int(textBox2.text())
            edge = self._graph.findEdgeByName(name)
            self._graph.setEdgeWeight(edge, weight)
            self._scene.update()

            # Update adjacent table widget
            self._mainWindow.updateAdjacentTable()

            # Update cache
            self._mainWindow.getCache().updateCache(self.copyGraph(self._graph))

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
            if edge is not None:
                self._graph.removeEdge(edge)
                redrawGraph = self.copyGraph(self._graph)
                self._scene.clear()

                self._graph = redrawGraph
                for item in self._graph.getVertexList():
                    self._scene.addItem(item)

                for item in self._graph.getEdgeList():
                    self._scene.addItem(item)
                self._scene.update()

            # Update adjacent table widget
            self._mainWindow.updateAdjacentTable()

            # Update cache
            self._mainWindow.getCache().updateCache(self.copyGraph(self._graph))

    # Utils
    def _contextMenuClearScene(self):
        self._graph.clear()
        self._scene.clear()
        self._scene.update()

        # Update adjacent table widget
        self._mainWindow.updateAdjacentTable()

        # Update cache
        self._mainWindow.getCache().updateCache(self.copyGraph(self._graph))

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
        self._scene.update()

    def resizeEvent(self, event):
        width, height = self.viewport().width(), self.viewport().height()
        self.setSceneRect(0, 0, width, height)

        for item in self._scene.items():
            if isinstance(item, Vertex):
                x, y = item.getPos()
                x = max(min(x, self.width() - VERTEX_SIZE), 0)
                y = max(min(y, self.height() - VERTEX_SIZE), 0)
                item.setPos(self.mapToScene(x, y))
        self._scene.update()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MiddleButton:
            pos_x, pos_y = event.pos().x(), event.pos().y()
            item = self._scene.itemAt(pos_x, pos_y, QtGui.QTransform())
            if item is not None:
                self._start = item

        self._scene.update()
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

        self._scene.update()
        super(View, self).mouseReleaseEvent(event)
