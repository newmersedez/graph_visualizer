from PyQt5 import QtWidgets, QtCore, QtGui
from utils.defines import *
import sys


class Scene(QtWidgets.QGraphicsScene):
    def __init__(self):
        super(Scene, self).__init__()
        self.setSceneRect(0, 0, FIELD_WIDTH, FIELD_HEIGHT)


class View(QtWidgets.QGraphicsView):
    def __init__(self):
        super(View, self).__init__()
        self._scene = Scene()
        self.setScene(self._scene)
        self.setStyleSheet('background-color: #151515;')
        self.setFixedSize(FIELD_WIDTH + 20, FIELD_HEIGHT + 20)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        pos_x, pos_y = event.pos().x(), event.pos().y()

        if event.button() == QtCore.Qt.LeftButton:
            item = self._scene.itemAt(pos_x - 10, pos_y - 10, QtGui.QTransform())

            if item is None:
                circle = QtWidgets.QGraphicsEllipseItem(pos_x - OFFSET - 10, pos_y - OFFSET - 10, VERTEX_SIZE, VERTEX_SIZE)
                circle.setBrush(QtGui.QColor(VERTEX_COLOR))
                circle.setFlag(QtWidgets.QGraphicsEllipseItem.ItemIsMovable)
                self._scene.addItem(circle)

        if event.button() == QtCore.Qt.RightButton:
            item = self._scene.itemAt(pos_x - OFFSET / 2, pos_y - OFFSET / 2, QtGui.QTransform())

            if item is not None:
                self._scene.removeItem(item)

        super(View, self).mousePressEvent(event)


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        # View settings
        self._view = View()

        # Window settings
        self.setFixedSize(WIN_WIDTH, WIN_HEIGHT)
        self.setWindowTitle('Graph Visualizer')
        self.setStyleSheet('background-color: #282828;')
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

        self.button = QtWidgets.QPushButton('Text')
        self.button.setFixedSize(400, 990)
        self._menuLayout.addWidget(self.button)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
