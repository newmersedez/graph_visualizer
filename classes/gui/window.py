# View

from PyQt5.QtCore import pyqtSlot
from classes.cache.cache import *
from classes.gui.view import *
import numpy as np
import random
import pandas as pd
import re


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        # View settings
        self._view = View(self)
        self._cache = Cache(CACHE_SIZE)
        self._task = None

        # Window settings
        self.setFixedSize(WIN_WIDTH, WIN_HEIGHT)
        self.setWindowTitle(WIN_TITLE)
        self.setFont(QtGui.QFont('Arial', 15))
        self.setStyleSheet('background-color: #303030; color: white; QMainWindow::separator {width: 20px};')
        self.setCentralWidget(self._view)

        # Layout management
        self._mainWidget = QtWidgets.QWidget()
        self._mainLayout = QtWidgets.QHBoxLayout()

        # Main layouts
        self._sceneLayout = QtWidgets.QVBoxLayout()
        self._menuLayout = QtWidgets.QVBoxLayout()

        # Menu layout
        self._tableWidget = QtWidgets.QWidget()
        self._tableLayout = QtWidgets.QVBoxLayout()
        self._tableWidget.setLayout(self._tableLayout)
        self._tableWidget.setGeometry(0, 0, 100, 100)

        self._buttonsWidget = QtWidgets.QWidget()
        self._buttonsLayout = QtWidgets.QVBoxLayout()
        self._buttonsWidget.setLayout(self._buttonsLayout)

        # Add layouts ans widgets
        self._sceneLayout.addWidget(self._view)
        self._menuLayout.addWidget(self._tableWidget)
        self._menuLayout.addWidget(self._buttonsWidget)

        self._mainLayout.addLayout(self._sceneLayout)
        self._mainLayout.addLayout(self._menuLayout)

        self._mainWidget.setLayout(self._mainLayout)
        self.setCentralWidget(self._mainWidget)

        self._initUI()

    def _initUI(self):
        # Menu bar
        self.statusBar()
        self.menuBar = self._createMenuBar()

        # Realtime adjacency matrix
        self._adjacentTable = self._createAdjacentTable()
        self._tableLayout.addWidget(self._adjacentTable)

        # Buttons
        self._createButtons()

    # Menu bar and menu widgets
    def _createMenuBar(self):
        self.statusBar()
        # Menu initialization
        menuBar = self.menuBar()
        menuBar.setNativeMenuBar(False)
        fileMenu = menuBar.addMenu('&Файл')
        tasksMenu = menuBar.addMenu('&Задачи теории графов')
        qaMenu = menuBar.addMenu('&?')

        # Load from file
        fileOpenMenu = QtWidgets.QMenu('Загрузить граф...', self)
        fileMenu.addMenu(fileOpenMenu)

        adjMatrixLoadAction = QtWidgets.QAction('&Загрузить матрицу смежности', self)
        adjMatrixLoadAction.triggered.connect(self._loadAdjacentMatrixFromFile)
        fileOpenMenu.addAction(adjMatrixLoadAction)

        incMatrixLoadAction = QtWidgets.QAction('&Загрузить матрицу инцидентности', self)
        incMatrixLoadAction.triggered.connect(self._loadIncidenceMatrixFromFile)
        fileOpenMenu.addAction(incMatrixLoadAction)

        configLoadAction = QtWidgets.QAction('&Загрузить файл конфигурации', self)
        configLoadAction.triggered.connect(self._loadConfigurationFromFile)
        fileOpenMenu.addAction(configLoadAction)

        # Save to file
        fileSaveMenu = QtWidgets.QMenu('Сохранить граф...', self)
        fileMenu.addMenu(fileSaveMenu)

        adjMatrixSaveAction = QtWidgets.QAction('&Сохранить матрицу смежности', self)
        adjMatrixSaveAction.triggered.connect(self._saveAdjacentMatrixToFile)
        fileSaveMenu.addAction(adjMatrixSaveAction)

        incMatrixSaveAction = QtWidgets.QAction('&Сохранить матрицу инцидентности', self)
        incMatrixSaveAction.triggered.connect(self._saveIncidenceMatrixToFile)
        fileSaveMenu.addAction(incMatrixSaveAction)

        configSaveAction = QtWidgets.QAction('&Сохранить файл конфигурации', self)
        configSaveAction.triggered.connect(self._saveConfigurationToFile)
        fileSaveMenu.addAction(configSaveAction)

        imageSaveAction = QtWidgets.QAction('&Сохранить граф в виде изображения', self)
        imageSaveAction.triggered.connect(self._saveToImage)
        fileSaveMenu.addAction(imageSaveAction)

        # Exit from app
        fileExitAction = QtWidgets.QAction('&Выйти из программы', self)
        fileExitAction.triggered.connect(QtWidgets.qApp.quit)
        fileMenu.addAction(fileExitAction)

        # Tasks menu
        algo = QtWidgets.QAction('BFS', self)
        algo.triggered.connect(self._view.viewBFS)
        tasksMenu.addAction(algo)

        # QA menu
        qaProgramAction = QtWidgets.QAction('&О программе', self)
        qaProgramAction.setStatusTip('Program info')
        qaMenu.addAction(qaProgramAction)

        qaAuthorAction = QtWidgets.QAction('&Об авторе', self)
        qaAuthorAction.setStatusTip('Program author')
        qaMenu.addAction(qaAuthorAction)

        return menuBar

    # Cache methods
    def getCache(self):
        return self._cache

    # File dialog
    def _openCSVFileDialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Откройте файл с матрицей", "",
                                                            "Matrix file (*.csv)", options=options)
        return fileName

    def _saveCSVFileDialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Выберите файл для сохранения", "",
                                                            "Matrix file (*.csv);;Image file (*png)", options=options)
        return fileName

    def _messageDialog(self, message: str):
        inputDialog = QtWidgets.QDialog(self)
        inputDialog.setWindowTitle('Ошибка')
        inputDialog.setStyleSheet('background-color: #303030; color: white;')
        inputDialog.setFont(QtGui.QFont('Arial', 15))

        form = QtWidgets.QFormLayout(inputDialog)
        form.addRow(QtWidgets.QLabel(message))

        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        form.addRow(buttonBox)
        buttonBox.accepted.connect(inputDialog.accept)
        buttonBox.rejected.connect(inputDialog.reject)

        inputDialog.exec_()

    # File load/save
    @staticmethod
    def _isCorrectAdjacentMatrix(matrix):
        matrixSize = len(matrix)
        for row in matrix:
            rowSize = len(row)
            if rowSize != matrixSize:
                return False
            for i in range(0, rowSize):
                if row[i] < 0:
                    return False
        return True

    @pyqtSlot()
    def _loadAdjacentMatrixFromFile(self):
        fileName = self._openCSVFileDialog()

        if len(fileName) != 0:
            try:
                adjMatrix = np.array(pd.read_csv(fileName, header=None))
                adjMatrixSize = len(adjMatrix)
                if not self._isCorrectAdjacentMatrix(adjMatrix):
                    raise ValueError

                graph = Graph()
                for i in range(0, adjMatrixSize):
                    cordX = random.randint(0, FIELD_WIDTH - VERTEX_SIZE)
                    cordY = random.randint(0, FIELD_HEIGHT - VERTEX_SIZE)

                    vertex = Vertex(0, 0, str(len(graph.getVertexList()) + 1), VERTEX_COLOR)
                    vertex.setPos(self._view.mapToScene(cordX, cordY))
                    graph.addVertex(vertex)

                vertexList = graph.getVertexList()
                vertexListSize = len(vertexList)

                for i in range(vertexListSize):
                    for j in range(i, vertexListSize):
                        if i == j and adjMatrix[i][j] != 0:
                            edge = Edge(vertexList[i], vertexList[j],
                                        name=str(len(graph.getEdgeList()) + 1),
                                        weight=int(adjMatrix[i][j]))
                            graph.addEdge(edge)
                        else:
                            if adjMatrix[i][j] == adjMatrix[j][i] and adjMatrix[i][j] != 0:
                                edge = Edge(vertexList[i], vertexList[j],
                                            name=str(len(graph.getEdgeList()) + 1),
                                            weight=int(adjMatrix[i][j]),
                                            direction=False)
                                graph.addEdge(edge)

                for i in range(vertexListSize):
                    for j in range(vertexListSize):
                        if i != j and adjMatrix[i][j] != adjMatrix[j][i] and adjMatrix[i][j] != 0:
                            edge = Edge(vertexList[i], vertexList[j],
                                        name=str(len(graph.getEdgeList()) + 1),
                                        weight=int(adjMatrix[i][j]),
                                        direction=True)
                            graph.addEdge(edge)

                if graph.empty():
                    raise ValueError
                else:
                    self._view.addGraph(graph)

            except ValueError:
                self._messageDialog('Ошибка в матрице смежности')

    @pyqtSlot()
    def _saveAdjacentMatrixToFile(self):
        fileName = self._saveCSVFileDialog()

        if len(fileName) != 0:
            matrix = self._view.getGraph().getAdjacentMatrix()
            pd.DataFrame(matrix).to_csv(fileName, header=False, index=False)

    @staticmethod
    def _isCorrectIncidenceMatrix(matrix):
        rowsCount = len(matrix)
        colsCount = len(matrix[0])

        for row in matrix:
            rowSize = len(row)
            if rowSize != colsCount:
                return False
            for i in range(rowSize):
                if abs(row[i] > 1):
                    return False
        return True

    @pyqtSlot()
    def _loadIncidenceMatrixFromFile(self):
        fileName = self._openCSVFileDialog()

        if len(fileName) != 0:
            try:
                incMatrix = np.array(pd.read_csv(fileName, header=None))
                if not self._isCorrectIncidenceMatrix(incMatrix):
                    raise ValueError

                rows = len(incMatrix)
                cols = len(incMatrix[0])
                graph = Graph()
                for i in range(0, cols):
                    vertexPoints = []
                    for j in range(0, rows):
                        if incMatrix[j][i] != 0:
                            vertexInfo = [str(j + 1), incMatrix[j][i]]
                            vertexPoints.append(vertexInfo)

                    if len(vertexPoints) == 2:
                        if graph.findVertexByName(vertexPoints[0][0]) is None:
                            cordX = random.randint(0, FIELD_WIDTH - VERTEX_SIZE)
                            cordY = random.randint(0, FIELD_HEIGHT - VERTEX_SIZE)

                            startVertex = Vertex(0, 0, str(len(graph.getVertexList()) + 1), VERTEX_COLOR)
                            startVertex.setPos(self._view.mapToScene(cordX, cordY))
                            graph.addVertex(startVertex)
                        else:
                            startVertex = graph.findVertexByName(vertexPoints[0][0])

                        if graph.findVertexByName(vertexPoints[1][0]) is None:
                            cordX = random.randint(VERTEX_SIZE, FIELD_WIDTH - 2 * VERTEX_SIZE)
                            cordY = random.randint(VERTEX_SIZE, FIELD_HEIGHT - 2 * VERTEX_SIZE)

                            endVertex = Vertex(0, 0, str(len(graph.getVertexList()) + 1), VERTEX_COLOR)
                            endVertex.setPos(self._view.mapToScene(cordX, cordY))
                            graph.addVertex(endVertex)
                        else:
                            endVertex = graph.findVertexByName(vertexPoints[1][0])

                        factor = self._view.countEdgeFactor(startVertex, endVertex)
                        if vertexPoints[0][1] == 1 and vertexPoints[1][1] == 1:
                            edge = Edge(startVertex, endVertex,
                                        name=str(len(graph.getEdgeList()) + 1),
                                        factor=factor,
                                        direction=False)
                            graph.addEdge(edge)

                        elif vertexPoints[0][1] == 1 and vertexPoints[1][1] == -1:
                            edge = Edge(startVertex, endVertex,
                                        name=str(len(graph.getEdgeList()) + 1),
                                        factor=factor,
                                        direction=True)
                            graph.addEdge(edge)

                        elif vertexPoints[0][1] == -1 and vertexPoints[1][1] == 1:
                            edge = Edge(endVertex, startVertex,
                                        name=str(len(graph.getEdgeList()) + 1),
                                        factor=factor,
                                        direction=True)
                            graph.addEdge(edge)

                    elif len(vertexPoints) == 1:
                        if vertexPoints[0][1] == 1:
                            if graph.findVertexByName(vertexPoints[0][0]) is None:
                                cordX = random.randint(VERTEX_SIZE, FIELD_WIDTH - 2 * VERTEX_SIZE)
                                cordY = random.randint(VERTEX_SIZE, FIELD_HEIGHT - 2 * VERTEX_SIZE)

                                vertex = Vertex(0, 0, str(len(graph.getVertexList()) + 1), VERTEX_COLOR)
                                vertex.setPos(self._view.mapToScene(cordX, cordY))
                                graph.addVertex(vertex)
                            else:
                                vertex = graph.findVertexByName(vertexPoints[0][0])

                            factor = self._view.countEdgeFactor(vertex, vertex)
                            edge = Edge(vertex, vertex,
                                        name=str(len(graph.getEdgeList()) + 1),
                                        factor=factor)
                            graph.addEdge(edge)

                if graph.empty():
                    raise ValueError
                else:
                    self._view.addGraph(graph)

            except ValueError:
                self._messageDialog('Ошибка в матрице инцидентности')

    @pyqtSlot()
    def _saveIncidenceMatrixToFile(self):
        fileName = self._saveCSVFileDialog()

        if len(fileName) != 0:
            matrix = self._view.getGraph().getIncidenceMatrix()
            pd.DataFrame(matrix).to_csv(fileName, header=False, index=False)

    @pyqtSlot()
    def _loadConfigurationFromFile(self):
        fileName = self._openCSVFileDialog()

        if len(fileName) != 0:
            stream = open(fileName, 'r')
            try:
                graph = Graph()
                while True:
                    line = stream.readline()
                    if not line:
                        break

                    # Vertex
                    if line.find('Vertex') != -1:
                        vertexRegex = r'(?<=Vertex{)(\d+)\((\d+), ?(\d+)'
                        vertexList = [list(map(int, (v, k, l))) for v, k, l in re.findall(vertexRegex, line)]
                        for item in vertexList:
                            if not graph.findVertexByName(str(item[0])):
                                if 0 <= int(item[1]) <= FIELD_WIDTH - VERTEX_SIZE and \
                                        0 <= int(item[2]) <= FIELD_HEIGHT - VERTEX_SIZE:
                                    vertex = Vertex(0, 0, str(item[0]), VERTEX_COLOR)
                                    vertex.setPos(self._view.mapToScene(int(item[1]), int(item[2])))
                                    graph.addVertex(vertex)

                    # Edge
                    if line.find('Edges') != -1:
                        edgeRegex = r'(?<=Edges{).+?(?=})'
                        digs = list(map(int, re.findall(r'\d+', re.search(edgeRegex, line).group())))
                        edgeList = [digs[i:i + 4] for i in range(0, len(digs), 4)]
                        for item in edgeList:
                            if not graph.findEdgeByName(str(item[0])):
                                startEdge = graph.findVertexByName(str(item[2]))
                                endEdge = graph.findVertexByName(str(item[3]))
                                if startEdge and endEdge:
                                    edge = Edge(startEdge, endEdge, name=str(item[0]), weight=int(item[1]))
                                    graph.addEdge(edge)

                if graph.empty():
                    raise ValueError
                else:
                    self._view.addGraph(graph)

            except ValueError:
                self._messageDialog('Ошибка в файле конфигурации')

            stream.close()

    @pyqtSlot()
    def _saveConfigurationToFile(self):
        fileName = self._saveCSVFileDialog()

        if len(fileName) != 0:
            vertexList = self._view.getGraph().getVertexList()
            edgeList = self._view.getGraph().getEdgeList()

            stream = open(fileName, 'w')
            for item in vertexList:
                name = item.getName()
                cordX, cordY = item.getPos()
                result = 'Vertex' + '{' + name + '(' + str(cordX) + ',' + str(cordY) + ')' + '}'
                stream.write(result)
                if item != vertexList[-1]:
                    stream.write('\n')

            if len(edgeList) != 0:
                stream.write('\nEdges{')
                for item in edgeList:
                    name = item.getName()
                    weight = item.getWeight()
                    startName = item.getStartVertex().getName()
                    endName = item.getEndVertex().getName()
                    result = str(name) + '(' + str(weight) + ',' + str(startName) + ',' + str(endName) + ')'
                    stream.write(result)
                    if item != edgeList[-1]:
                        stream.write(',')
                stream.write('}')
            stream.close()

    @pyqtSlot()
    def _saveToImage(self):
        fileName = self._saveCSVFileDialog()

        if len(fileName) != 0:
            pixmap = self._view.grab(self._view.sceneRect().toRect())
            pixmap.save(fileName)

    # Table widget
    @staticmethod
    def _createAdjacentTable():
        _adjacentTable = QtWidgets.QTableWidget()
        _adjacentTable.setFixedSize(TABLE_WIDTH, TABLE_HEIGHT)
        _adjacentTable.horizontalHeader().setDefaultSectionSize(30)
        _adjacentTable.verticalHeader().setDefaultSectionSize(30)
        # _adjacentTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        _adjacentTable.setStyleSheet('QWidget'
                                     '{'
                                     'background-color: #333333;'
                                     'color: #fffff8;'
                                     '}'
                                     'QHeaderView::section'
                                     '{'
                                     'background-color: #646464;'
                                     'padding: 4px;'
                                     'border: 1px solid #fffff8;'
                                     'font-size: 14pt;'
                                     '}'
                                     'QTableWidget'
                                     '{'
                                     'gridline-color: #fffff8;'
                                     'font-size: 12pt;'
                                     '}'
                                     'QTableWidget QTableCornerButton::section'
                                     '{'
                                     'background-color: #646464;'
                                     'border: 1px solid #fffff8;'
                                     '}')
        return _adjacentTable

    def updateAdjacentTable(self):
        vertexList = self._view.getGraph().getVertexList()
        edgeList = self._view.getGraph().getEdgeList()

        columnCount = rowCount = len(vertexList)
        self._adjacentTable.setColumnCount(columnCount)
        self._adjacentTable.setRowCount(rowCount)

        i = 0
        for item in vertexList:
            self._adjacentTable.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem(item.getName()))
            self._adjacentTable.setVerticalHeaderItem(i, QtWidgets.QTableWidgetItem(item.getName()))
            i += 1

        matrix = self._view.getGraph().getAdjacentMatrix()
        for i in range(columnCount):
            for j in range(rowCount):
                self._adjacentTable.setItem(i, j, QtWidgets.QTableWidgetItem(str(matrix[i][j])))

    # Buttons widget
    def _createButtons(self):
        button1 = QtWidgets.QPushButton('Undo', self)
        button1.setFixedSize(400, 70)
        button1.clicked.connect(self._undoButtonAction)

        button2 = QtWidgets.QPushButton('Redo', self)
        button2.setFixedSize(400, 70)
        button2.clicked.connect(self._redoButtonAction)

        button3 = QtWidgets.QPushButton('dummy button', self)
        button3.setFixedSize(400, 70)

        button4 = QtWidgets.QPushButton('dummy button', self)
        button4.setFixedSize(400, 70)

        button5 = QtWidgets.QPushButton('dummy button', self)
        button5.setFixedSize(400, 70)

        self._buttonsLayout.addWidget(button1)
        self._buttonsLayout.addWidget(button2)
        self._buttonsLayout.addWidget(button3)
        self._buttonsLayout.addWidget(button4)
        self._buttonsLayout.addWidget(button5)

    @pyqtSlot()
    def _undoButtonAction(self):
        graph = self._cache.getDecreasedState()

        if graph is not None:
            self._view.addGraph(graph)
            self.updateAdjacentTable()

    @pyqtSlot()
    def _redoButtonAction(self):
        graph = self._cache.getIncreasedState()

        if graph is not None:
            self._view.addGraph(graph)
            self.updateAdjacentTable()
