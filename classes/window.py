from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QGraphicsEllipseItem
from utils.defines import *
from classes.vertex import *
from classes.verge import *


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Service stuff
        self._click = None
        self._operation = None
        self._event_x = None
        self._event_y = None
        self._objectInFocus = None
        self._vertexList = list()
        self._vergeList = list()

        # Window defauls
        self._width = WIN_WIDTH
        self._height = WIN_HEIGHT
        self._title = WIN_TITLE

        # Window settings
        self.setWindowTitle('Graph Visualizer')
        self.setFixedSize(WIN_WIDTH, WIN_HEIGHT)
        self.setStyleSheet("QMainWindow {background: '#282828';}");
        self.setMouseTracking(True)

        # Layout management
        self._mainWidget = QtWidgets.QWidget()
        self._mainLayout = QtWidgets.QHBoxLayout()

        self._displayLayout = QtWidgets.QVBoxLayout()
        self._menuLayout = QtWidgets.QVBoxLayout()

        self._image = QtWidgets.QLabel()
        self._canvas = QtGui.QPixmap(FIELD_SIZE, FIELD_SIZE)
        self._canvas.fill(QtGui.QColor('#151515'))
        self._image.setPixmap(self._canvas)
        self._displayLayout.addWidget(self._image)

        self._mainLayout.addLayout(self._displayLayout)
        self._mainLayout.addLayout(self._menuLayout)

        self._mainWidget.setLayout(self._mainLayout)
        self.setCentralWidget(self._mainWidget)

    # Vertex functions
    def _point_on_vertex(self, x: int, y: int):
        for vertex in self._vertexList:
            if vertex.collidePoint(x, y):
                return vertex
            else:
                if vertex.draggingStatus():
                    vertex.draggingStop()
        return None

    def _addNewVertex(self, x: int, y: int):
        if len(self._vertexList) == 0:
            name = '1'
        else:
            name = str(int(self._vertexList[-1].getName()) + 1)

        vertex = Vertex(x + 20, y + 20, name, VERTEX_COLOR)
        self._objectInFocus = vertex
        self._vertexList.append(vertex)

    def _removeVertex(self, vertex: Vertex):
        self._objectInFocus = vertex
        self._vertexList.remove(vertex)

    # Verge functions
    def _point_on_verge(self, x: int, y: int):
        for verge in self._vergeList:
            if verge.collidePoint(x, y):
                return True
        return False

    # Events
    def paintEvent(self, event):
        painter = QtGui.QPainter(self._image.pixmap())
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        pen = QtGui.QPen(QtGui.QColor(FIELD_COLOR))
        painter.setPen(pen)

        if self._click == MOUSE_LEFT and self._operation == ADD_VERTEX and self._objectInFocus is not None:
            brush = QtGui.QBrush(QtGui.QColor(VERTEX_COLOR))
            painter.setBrush(brush)
            painter.drawEllipse(self._event_x, self._event_y, VERTEX_RADIUS, VERTEX_RADIUS)
            painter.setFont(QtGui.QFont('Arial', 12))
            painter.drawText(self._event_x + 12, self._event_y + 25, self._objectInFocus.getName())
            self._operation = None
            self._objectInFocus = None

        elif self._click == MOUSE_RIGHT and self._operation == DELETE_VERTEX:
            brush = QtGui.QBrush(QtGui.QColor(FIELD_COLOR))
            painter.setBrush(brush)
            painter.drawEllipse(self._event_x - 20, self._event_y - 20, VERTEX_RADIUS, VERTEX_RADIUS)
            self._operation = None
            self._objectInFocus = None

        elif self._click == MOUSE_MIDDLE and self._operation == ADD_VERGE:
            pen = QtGui.QPen(QtGui.QColor(QtCore.Qt.white))
            painter.setPen(pen)

            x1, y1 = self._vertexList[0].getPos()
            x2, y2 = self._vertexList[1].getPos()
            painter.drawLine(x1, y1, x2, y2)

        painter.end()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self._click = MOUSE_LEFT
            self._event_x = event.pos().x() - 10
            self._event_y = event.pos().y() - 10
            vertex = self._point_on_vertex(self._event_x, self._event_y)

            if vertex is None:
                self._operation = ADD_VERTEX
                self._addNewVertex(self._event_x, self._event_y)
            else:
                vertex.draggingStart()

        elif event.button() == QtCore.Qt.RightButton:
            self._click = MOUSE_RIGHT
            self._event_x = event.pos().x() - 10
            self._event_y = event.pos().y() - 10
            vertex = self._point_on_vertex(self._event_x, self._event_y)

            if vertex is not None:
                self._event_x, self._event_y = vertex.getPos()
                self._operation = DELETE_VERTEX
                self._removeVertex(vertex)

        elif event.button() == QtCore.Qt.MiddleButton:
            self._click = MOUSE_MIDDLE
            self._event_x = event.pos().x()
            self._event_y = event.pos().y()

            if len(self._vertexList) == 2:
                self._operation = ADD_VERGE

        self.update()

    def mouseMoveEvent(self, event) -> None:
        print(event.pos().x(), event.pos().y())
