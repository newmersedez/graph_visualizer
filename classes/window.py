from PyQt5 import QtWidgets, QtGui, QtCore
from utils.defines import *
from classes.view import *
from classes.cache import *
import numpy as np


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
        # Menubar
        self.statusBar()
        self.menuBar = self.menuBar()
        self.menuBar.setNativeMenuBar(False)
        self.menuBar.addMenu('&File')
        self.menuBar.addMenu('|').setDisabled(True)
        self.menuBar.addMenu('&Tasks')
        self.menuBar.addMenu('|').setDisabled(True)
        self.menuBar.addMenu('&?')
        self.menuBar.addSeparator()

        # Realtime adjacency matrix
        self._adjacentTable = self._createAdjacentTable()
        self._tableLayout.addWidget(self._adjacentTable)

        # Buttons
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

    # Additional functions
    def _viewGetVertexList(self):
        return self._view.getVertexList()

    def _viewGetVergeList(self):
        return self._view.getVergeLise()

    def getCache(self):
        return self._cache

    # Widget creation
    @staticmethod
    def _createAdjacentTable():
        _adjacentTable = QtWidgets.QTableWidget()
        _adjacentTable.setFixedSize(TABLE_WIDTH, TABLE_HEIGHT)
        _adjacentTable.horizontalHeader().setDefaultSectionSize(30)
        _adjacentTable.verticalHeader().setDefaultSectionSize(30)
        _adjacentTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
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
        vertexList = self._viewGetVertexList()
        vergeList = self._viewGetVergeList()

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

            posStart = vertexList.index(startVertex)
            posEnd = vertexList.index(endVertex)

            if verge.isDirected():
                matrix[posStart][posEnd] = '1'

            else:
                matrix[posStart][posEnd] = '1'
                matrix[posEnd][posStart] = '1'

        for i in range(columnCount):
            for j in range(rowCount):
                self._adjacentTable.setItem(i, j, QtWidgets.QTableWidgetItem(matrix[i][j]))

    # Buttons actions
    def _undoButtonAction(self):
        vertexList, vergeList = self._cache.getDecreasedState()

        scene = self._view.getScene()
        oldVertexList = self._view.getVertexList()
        oldVergeList = self._view.getVergeLise()

        for vertex in oldVertexList:
            scene.removeItem(vertex)

        for verge in oldVergeList:
            scene.removeItem(verge)

        self._view.setVertexList(vertexList)
        self._view.setVergeList(vergeList)

        for vertex in vertexList:
            scene.addItem(vertex)

        for verge in vergeList:
            scene.addItem(verge)

        self.updateAdjacentTable()

    def _redoButtonAction(self):
        vertexList, vergeList = self._cache.getIncreasedState()

        scene = self._view.getScene()
        oldVertexList = self._view.getVertexList()
        oldVergeList = self._view.getVergeLise()

        for vertex in oldVertexList:
            scene.removeItem(vertex)

        for verge in oldVergeList:
            scene.removeItem(verge)

        self._view.setVertexList(vertexList)
        self._view.setVergeList(vergeList)

        for vertex in vertexList:
            scene.addItem(vertex)

        for verge in vergeList:
            scene.addItem(verge)

        self.updateAdjacentTable()
