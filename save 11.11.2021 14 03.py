from PyQt5 import QtWidgets, QtCore, QtGui
from utils.defines import *
import sys


class Scene(QtWidgets.QGraphicsScene):
    def __init__(self):
        super(Scene, self).__init__()
        self.setSceneRect(0, 0, FIELD_WIDTH, FIELD_HEIGHT)

    # def mousePressEvent(self, event):
    #     if event.button() == QtCore.Qt.LeftButton:
    #         pos_x = event.pos().x()
    #         pos_y = event.pos().y()
    #         circle = QtWidgets.QGraphicsEllipseItem(pos_x, pos_y, VERTEX_SIZE, VERTEX_SIZE)
    #         circle.setBrush(QtGui.QColor(VERTEX_COLOR))
    #         circle.setFlag(QtWidgets.QGraphicsEllipseItem.ItemIsMovable)
    #         self.addItem(circle)
    #
    #     elif event.button() == QtCore.Qt.RightButton:
    #         pos_x = event.pos().x()
    #         pos_y = event.pos().y()
    #         print(pos_x, pos_y)
    #         item = self.itemAt(pos_x, pos_y, QtGui.QTransform())
    #         if item is not None:
    #             print('ahhaha')
    #             self.removeItem(item)
    #     super(Scene, self).mousePressEvent(event)


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
        circle = QtWidgets.QGraphicsEllipseItem(10, 10, VERTEX_SIZE, VERTEX_SIZE)
        circle.setBrush(QtGui.QColor(VERTEX_COLOR))
        circle.setFlag(QtWidgets.QGraphicsEllipseItem.ItemIsMovable)
        self._scene.addItem(circle)

    def mousePressEvent(self, event):
        pos_x, pos_y = event.pos().x(), event.pos().y()

        if event.button() == QtCore.Qt.LeftButton:
            item = self._scene.itemAt(pos_x, pos_y, QtGui.QTransform())

            if item is None:
                circle = QtWidgets.QGraphicsEllipseItem(pos_x - 25, pos_y - 25, VERTEX_SIZE, VERTEX_SIZE)
                circle.setBrush(QtGui.QColor(VERTEX_COLOR))
                circle.setFlag(QtWidgets.QGraphicsEllipseItem.ItemIsMovable)
                self._scene.addItem(circle)

        if event.button() == QtCore.Qt.RightButton:
            item = self._scene.itemAt(pos_x, pos_y, QtGui.QTransform())

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


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
