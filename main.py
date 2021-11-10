from PyQt5 import QtCore, QtGui, QtWidgets
from utils.defines import *
import sys


class Vertex(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, x: int, y: int, name: str, color: str):
        super(Vertex, self).__init__()
        self._x = x
        self._y = y
        self._name = name
        self._color = color
        self.adjacentVertexList = list()

    def getPos(self):
        return self._x, self._y

    def getName(self):
        return self._name


class Scene(QtWidgets.QGraphicsScene):
    def __init__(self):
        super(Scene, self).__init__()
        self._vertexList = list()
        self._vergeList = list()
        self.setSceneRect(0, 0, FIELD_WIDTH, FIELD_HEIGHT)

    def getVertexList(self):
        return self._vertexList

    def getVergeList(self):
        return self._vergeList


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Window settings
        self._width = WIN_WIDTH
        self._height = WIN_HEIGHT
        self.setWindowTitle("Pyside2 QGraphic View")
        self.setFixedSize(WIN_WIDTH, WIN_HEIGHT)
        self.setStyleSheet('background-color: #282828;')

        # Drawing field settings
        self._scene = Scene()
        self._view = QtWidgets.QGraphicsView(self._scene)
        self._view.setFixedSize(FIELD_WIDTH, FIELD_HEIGHT)
        self._view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self._view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self._view.setStyleSheet('background-color: #151515;')
        self._view.setMouseTracking(True)

        self.button = QtWidgets.QPushButton('text', self)                           # delete after
        self.button.setFixedSize(395, 1200)

        # Layout management
        self._mainWidget = QtWidgets.QWidget()
        self._mainLayout = QtWidgets.QHBoxLayout()

        self._sceneLayout = QtWidgets.QVBoxLayout()
        self._menuLayout = QtWidgets.QVBoxLayout()

        self._sceneLayout.addWidget(self._view)
        self._menuLayout.addWidget(self.button)                                      # delete after

        self._mainLayout.addLayout(self._sceneLayout)
        self._mainLayout.addLayout(self._menuLayout)

        self._mainWidget.setLayout(self._mainLayout)
        self.setCentralWidget(self._mainWidget)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            item = QtWidgets.QGraphicsEllipseItem(event.pos().x() - OFFSET, event.pos().y() - OFFSET, 50, 50)

            item.setBrush(QtCore.Qt.red)
            item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
            self._scene.addItem(item)

        elif event.button() == QtCore.Qt.RightButton:
            item = self._scene.itemAt(event.pos().x() + OFFSET + 2, event.pos().y() + OFFSET * 2, QtGui.QTransform())
            if item is not None:
                self._scene.removeItem(item)

def main():
    app = QtWidgets.QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()