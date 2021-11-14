import numpy
from PyQt5 import QtWidgets, QtGui, QtCore
from utils.defines import *
from classes.view import *
from classes.vertex import *
from classes.verge import *
from classes.cache import *
import numpy as np
import csv
import random


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        # View settings
        self._view = View(self)
        self._cache = Cache(CACHE_SIZE)

        # Window settings
        # self.resize(WIN_WIDTH, WIN_HEIGHT)
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

        # Cache
        cacheItem = CacheItem(self._view.getVertexList(), self._view.getVergeList())
        self._cache.updateCache(cacheItem)

        # Realtime adjacency matrix
        self._adjacentTable = self._createAdjacentTable()
        self._tableLayout.addWidget(self._adjacentTable)

        # Buttons
        self._createButtons()

    # Cache methods
    def getCache(self):
        return self._cache

    # Menu bar and menu methods
    def _createMenuBar(self):
        # Menu initialization
        menuBar = self.menuBar()
        menuBar.setNativeMenuBar(False)
        fileMenu = menuBar.addMenu('&Файл')
        tasksMenu = menuBar.addMenu('&Задачи теории графов')
        qaMenu = menuBar.addMenu('&?')

        # Load from file
        fileOpenMenu = QtWidgets.QMenu('Загрузить граф из файла', self)
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
        fileSaveMenu = QtWidgets.QMenu('Сохранить граф в файл', self)
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

        # Save as image
        fileSaveImageAction = QtWidgets.QAction('&Сохранить граф в виде изображения', self)
        fileSaveImageAction.triggered.connect(self._saveToImage)
        fileMenu.addAction(fileSaveImageAction)

        # Exit from app
        fileExitAction = QtWidgets.QAction('&Выйти из программы', self)
        fileExitAction.triggered.connect(QtWidgets.qApp.quit)
        fileMenu.addAction(fileExitAction)

        # Tasks menu
        # fill when program is finished

        # QA menu
        qaProgramAction = QtWidgets.QAction('&О программе', self)
        qaProgramAction.setStatusTip('Program info')
        qaMenu.addAction(qaProgramAction)

        qaAuthorAction = QtWidgets.QAction('&Об авторе', self)
        qaAuthorAction.setStatusTip('Program author')
        qaMenu.addAction(qaAuthorAction)

        return menuBar

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
                                                            "Matrix file (*.csv)", options=options)
        return fileName

    def _clearAll(self):
        scene = self._view.getScene()
        vertexList = self._view.getVertexList()
        vergeList = self._view.getVergeList()

        scene.clear()
        vertexList.clear()
        vergeList.clear()
        self.updateAdjacentTable()
        self._cache.clear()

    @staticmethod
    def _isSquareNumpyMatrix(matrix):
        if matrix is not None:
            matrixSize = len(matrix)
            for item in matrix:
                itemSize = len(item)
                if itemSize != matrixSize:
                    return False
        return True

    def _loadAdjacentMatrixFromFile(self):
        fileName = self._openCSVFileDialog()

        if len(fileName) != 0:
            reader = csv.reader(open(fileName, "rt"), delimiter=',')
            lst = list(reader)

            try:
                adjMatrix = np.array(lst).astype('int')
                adjMatrixSize = len(adjMatrix)

                pass

            except ValueError:
                print('incorrect file')                # throw message window in future

    def _loadIncidenceMatrixFromFile(self):
        fileName = self._openCSVFileDialog()

        if len(fileName) != 0:
            reader = csv.reader(open(fileName, "rt"), delimiter=',')
            lst = list(reader)

            try:
                IncMatrix = np.array(lst).astype('int')
                print(IncMatrix)

            except ValueError:
                print('incorrect file')  # throw message window in future

    def _loadConfigurationFromFile(self):
        print('config file')

        scene = self._view.getScene()
        vertexList = self._view.getVertexList()
        vergeList = self._view.getVergeList()

        scene.clear()
        vertexList.clear()
        vergeList.clear()
        self.updateAdjacentTable()
        self._cache.clear()

    def _saveAdjacentMatrixToFile(self):
        print('save adj')
        fileName = self._saveCSVFileDialog()

        if len(fileName) != 0:
            stream = open(fileName, 'w')
            delimiter = ','
            columnCount = rowCount = self._adjacentTable.columnCount()

            for i in range(0, columnCount):
                for j in range(0, rowCount):
                    stream.write(self._adjacentTable.item(i, j).text())
                    if j != rowCount - 1:
                        stream.write(delimiter)
                if i != columnCount - 1:
                    stream.write('\n')
            stream.close()

    def _saveIncidenceMatrixToFile(self):
        print('save inc')
        fileName = self._saveCSVFileDialog()

        if len(fileName) != 0:
            stream = open(fileName, 'w')
            delimiter = ','
            columnCount = rowCount = self._adjacentTable.columnCount()
            vertexList = self._view.getVertexList()
            vergeList = self._view.getVergeList()

            for vertex in vertexList:
                for verge in vergeList:
                    if verge.isDirected():
                        if vertex == verge.getStartVertex():
                            stream.write('1')
                            stream.write(delimiter)

                        elif vertex == verge.getEndVertex():
                            stream.write('-1')
                            stream.write(delimiter)

                        else:
                            stream.write('0')
                            stream.write(delimiter)

                    else:
                        if (vertex == verge.getStartVertex()) or (vertex == verge.getEndVertex()):
                            stream.write('1')
                            stream.write(delimiter)

                        else:
                            stream.write('0')
                            stream.write(delimiter)

                stream.write('\n')
            stream.close()

    def _saveConfigurationToFile(self):
        print('save adj matrix to file')
        # self._saveCSVFileDialog()

    def _saveToImage(self):
        print('save to image')
        # self._saveCSVFileDialog()

    # Table methods
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

    def updateAdjacentTable(self, adjMatrix=None):
        vertexList = self._view.getVertexList()
        vergeList = self._view.getVergeList()

        columnCount = rowCount = len(vertexList)
        self._adjacentTable.setColumnCount(columnCount)
        self._adjacentTable.setRowCount(rowCount)

        i = 0
        for item in vertexList:
            self._adjacentTable.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem(item.getName()))
            self._adjacentTable.setVerticalHeaderItem(i, QtWidgets.QTableWidgetItem(item.getName()))
            i += 1

        n = len(vertexList)
        matrix = np.array([['0'] * n] * n)
        for verge in vergeList:
            startVertex = verge.getStartVertex()
            endVertex = verge.getEndVertex()
            posStart, posEnd = None, None

            if startVertex in vertexList:
                posStart = vertexList.index(startVertex)
            if endVertex in vertexList:
                posEnd = vertexList.index(endVertex)

            if (posStart is not None) and (posEnd is not None):
                if verge.isDirected():
                    matrix[posStart][posEnd] = '1'

                else:
                    matrix[posStart][posEnd] = '1'
                    matrix[posEnd][posStart] = '1'

        for i in range(columnCount):
            for j in range(rowCount):
                self._adjacentTable.setItem(i, j, QtWidgets.QTableWidgetItem(matrix[i][j]))

    # Buttons methods
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

    def _undoButtonAction(self):
        vertexList, vergeList = self._cache.getDecreasedState()
        scene = self._view.getScene()
        oldVertexList = self._view.getVertexList()
        oldVergeList = self._view.getVergeList()

        if vertexList is not None:
            for vertex in oldVertexList:
                scene.removeItem(vertex)

            self._view.setVertexList(vertexList)

            for vertex in vertexList:
                scene.addItem(vertex)

        if vergeList is not None:
            for verge in oldVergeList:
                scene.removeItem(verge)
            self._view.setVergeList(vergeList)

            for verge in vergeList:
                scene.addItem(verge)

        self.updateAdjacentTable()

    def _redoButtonAction(self):
        vertexList, vergeList = self._cache.getIncreasedState()
        scene = self._view.getScene()
        oldVertexList = self._view.getVertexList()
        oldVergeList = self._view.getVergeList()

        if vertexList is not None:
            for vertex in oldVertexList:
                scene.removeItem(vertex)

            self._view.setVertexList(vertexList)

            for vertex in vertexList:
                scene.addItem(vertex)

        if vergeList is not None:
            for verge in oldVergeList:
                scene.removeItem(verge)
            self._view.setVergeList(vergeList)

            for verge in vergeList:
                scene.addItem(verge)

        self.updateAdjacentTable()
