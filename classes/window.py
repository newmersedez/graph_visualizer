from PyQt5 import QtWidgets, QtGui, QtCore
from utils.defines import *
from classes.view import *


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        # View settings
        self._view = View(self)
        self.close()

        # Window settings
        self.setFixedSize(WIN_WIDTH, WIN_HEIGHT)
        self.setWindowTitle(WIN_TITLE)
        self.setFont(QtGui.QFont('Arial', 15))
        self.setStyleSheet('background-color: #303030; color: white; QMainWindow::separator {width: 20px};')
        self.setCentralWidget(self._view)

        # Layout management
        self._mainWidget = QtWidgets.QWidget()
        self._mainLayout = QtWidgets.QHBoxLayout()

        self._sceneLayout = QtWidgets.QVBoxLayout()
        self._menuLayout = QtWidgets.QVBoxLayout()

        self._sceneLayout.addWidget(self._view)

        self._mainLayout.addLayout(self._sceneLayout)
        self._mainLayout.addLayout(self._menuLayout)

        self._mainWidget.setLayout(self._mainLayout)
        self.setCentralWidget(self._mainWidget)

        self._initUI()

    def _viewGetVertexList(self):
        return self._view.getVertexList()

    def _viewGetVergeList(self):
        return self._view.getVergeLise()

    @staticmethod
    def _createAdjacentTable():
        adjacentTable = QtWidgets.QTableWidget()
        adjacentTable.setFixedSize(TABLE_WIDTH, TABLE_HEIGHT)
        adjacentTable.horizontalHeader().setDefaultSectionSize(30)
        adjacentTable.verticalHeader().setDefaultSectionSize(30)
        adjacentTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        adjacentTable.setStyleSheet('QWidget'
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
        return adjacentTable

    def _updateAdjacentTable(self):
        vertexList = self._viewGetVertexList()
        vergeList = self._viewGetVergeList()

        columnCount = rowCount = len(vertexList)
        self.adjacentTable.setColumnCount(columnCount)
        self.adjacentTable.setRowCount(rowCount)

        i = 0
        for item in vertexList:
            self.adjacentTable.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem(item.getName()))
            self.adjacentTable.setVerticalHeaderItem(i, QtWidgets.QTableWidgetItem(item.getName()))
            i += 1

        for i in range(columnCount):
            for j in range(rowCount):
                self.adjacentTable.setItem(i, j, QtWidgets.QTableWidgetItem('0'))

        # for verge in vergeList:

    def _initUI(self):
        # Realtime adjacency matrix
        self.adjacentTable = self._createAdjacentTable()
        self._menuLayout.addWidget(self.adjacentTable)

        # Buttons
        button1 = QtWidgets.QPushButton('Change color theme', self)
        button1.setFixedSize(400, 70)

        button2 = QtWidgets.QPushButton('Create vertex', self)
        button2.setFixedSize(400, 70)

        button3 = QtWidgets.QPushButton('Delete vertex', self)
        button3.setFixedSize(400, 70)

        self._menuLayout.addWidget(button1)
        self._menuLayout.addWidget(button2)
        self._menuLayout.addWidget(button3)
