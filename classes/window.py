from classes.sceneview import *


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Window settings
        self._width = WIN_WIDTH
        self._height = WIN_HEIGHT
        self._backgroundColor = WIN_DARK_COLOR
        self._scene = Scene()
        self._view = QtWidgets.QGraphicsView(self._scene)

        self._view.setScene(self._scene)
        self.setWindowTitle("Graph Visualizer")
        self.setFixedSize(WIN_WIDTH, WIN_HEIGHT)
        self.setStyleSheet('background-color: #282828;')

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
        # button1.clicked.connect(self.changeColorTheme)

        button2 = QtWidgets.QPushButton('Create vertex', self)
        button2.setFixedSize(395, 100)
        # button2.clicked.connect(self._view.addVertex)

        button3 = QtWidgets.QPushButton('Delete vertex', self)
        button3.setFixedSize(395, 100)
        # button3.clicked.connect(self._view.deleteVertex)

        self._menuLayout.addWidget(button1)
        self._menuLayout.addWidget(button2)
        self._menuLayout.addWidget(button3)

    def changeColorTheme(self):
        if self._backgroundColor == WIN_DARK_COLOR:
            self._backgroundColor = WIN_BRIGHT_COLOR
            self.setStyleSheet('background-color: white;')
            self._view.changeViewColor()

        elif self._backgroundColor == WIN_BRIGHT_COLOR:
            self._backgroundColor = WIN_DARK_COLOR
            self.setStyleSheet('background-color: #282828;')
            self._view.changeViewColor()
