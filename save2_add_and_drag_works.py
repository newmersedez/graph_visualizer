from PyQt5 import QtWidgets, QtCore, QtGui
from utils.defines import *
import sys


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self._scene = QtWidgets.QGraphicsScene()
        self._scene.setSceneRect(0, 0, FIELD_WIDTH, FIELD_HEIGHT)

        self._view = QtWidgets.QGraphicsView(self._scene)
        # self._view.setStyleSheet('background-color: #151515;')
        self._view.setScene(self._scene)

        self.setFixedSize(WIN_WIDTH, WIN_HEIGHT)
        # self.setStyleSheet('background-color: #282828;')
        self.setCentralWidget(self._view)
        self.setMouseTracking(True)

        circle = QtWidgets.QGraphicsEllipseItem(10, 10, VERTEX_SIZE, VERTEX_SIZE)
        circle.setBrush(QtGui.QColor(VERTEX_COLOR))
        circle.setFlag(QtWidgets.QGraphicsEllipseItem.ItemIsMovable)
        self._scene.addItem(circle)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            pos_x, pos_y = event.pos().x(), event.pos().y()
            circle = QtWidgets.QGraphicsEllipseItem(pos_x, pos_y, VERTEX_SIZE, VERTEX_SIZE)
            circle.setBrush(QtGui.QColor(VERTEX_COLOR))
            circle.setFlag(QtWidgets.QGraphicsEllipseItem.ItemIsMovable)
            self._scene.addItem(circle)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
