from PyQt5 import QtWidgets, QtGui, QtCore
from utils.defines import *
from classes.view import *


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        # View settings
        self._view = View()

        # Window settings
        self.setFixedSize(WIN_WIDTH, WIN_HEIGHT)
        self.setWindowTitle('Graph Visualizer')
        self.setStyleSheet('background-color: #303030;')
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

        self.initUI()

    def initUI(self):
        button1 = QtWidgets.QPushButton('Change color theme', self)
        button1.setFixedSize(395, 100)

        button2 = QtWidgets.QPushButton('Create vertex', self)
        button2.setFixedSize(395, 100)

        button3 = QtWidgets.QPushButton('Delete vertex', self)
        button3.setFixedSize(395, 100)

        self._menuLayout.addWidget(button1)
        self._menuLayout.addWidget(button2)
        self._menuLayout.addWidget(button3)
