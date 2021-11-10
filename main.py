# from PyQt5 import QtGui, QtCore, QtWidgets
# from classes.window import *
# import sys
#
# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     window = Window()
#     window.show()
#     sys.exit(app.exec())

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


class DrawField(QtWidgets.QGraphicsView):
    def __init__(self):
        super(DrawField, self).__init__()
        # Graph utils
        self._vertexList = list()
        self._vergeList = list()

        # Field settings
        self._scene = QtWidgets.QGraphicsScene(self)
        self._scene.setSceneRect(0, 0, FIELD_WIDTH, FIELD_HEIGHT)
        self._view = QtWidgets.QGraphicsView(self._scene, self)
        self._view.setFixedSize(FIELD_WIDTH, FIELD_HEIGHT)
        self._view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self._view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self._view.setStyleSheet('background-color: #151515;')

    def addVertex(self, x: int, y: int):
        if len(self._vertexList) == 0:
            name = '1'
        else:
            name = str(int(self._vertexList[-1].getName()) + 1)

        vertex = Vertex(x, y, name, VERTEX_COLOR)
        self._vertexList.append(vertex)

        pos_x, pos_y = vertex.getPos()
        brush = QtGui.QBrush(QtGui.QColor(VERTEX_COLOR))
        pen = QtGui.QPen(QtGui.QColor(FIELD_COLOR))
        ellipse = self._scene.addEllipse(pos_x, pos_y, VERTEX_SIZE, VERTEX_SIZE, pen, brush)
        ellipse.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)

    def getScene(self):
        return self._scene


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
        self._view = DrawField()
        self.button = QtWidgets.QPushButton('text', self)                           # delete after
        self.button.setFixedSize(395, 1200)

        self._view.addVertex(100, 100)
        self._view.addVertex(200, 100)

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


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
