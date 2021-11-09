from PyQt5 import QtWidgets, QtGui, QtCore
from utils.defines import *


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.click = 0
        self.event_x = 0
        self.event_y = 0
        self.width = WIN_WIDTH
        self.height = WIN_HEIGHT
        self.title = WIN_TITLE
        self.setWindowTitle('Graph Visualizer')
        self.setMouseTracking(True)
        self.resize(WIN_WIDTH, WIN_HEIGHT)
        self.setStyleSheet("QMainWindow {background: '#282828';}");

        self.mainWidget = QtWidgets.QWidget()
        self.mainLayout = QtWidgets.QHBoxLayout()

        self.displayLayout = QtWidgets.QVBoxLayout()
        self.menuLayout = QtWidgets.QVBoxLayout()

        self.image = QtWidgets.QLabel()
        self.canvas = QtGui.QPixmap(FIELD_SIZE, FIELD_SIZE)
        self.canvas.fill(QtGui.QColor('#151515'))
        self.image.setPixmap(self.canvas)

        self.displayLayout.addWidget(self.image)

        self.mainLayout.addLayout(self.displayLayout)
        self.mainLayout.addLayout(self.menuLayout)

        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self.image.pixmap())
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        brush = QtGui.QBrush(QtGui.QColor(VERTEX_COLOR))
        pen = QtGui.QPen(QtGui.QColor(FIELD_COLOR))
        painter.setBrush(brush)
        painter.setPen(pen)

        if self.click == 1:
            painter.drawEllipse(self.event_x - VERTEX_RADIUS, self.event_y - VERTEX_RADIUS,
                                VERTEX_RADIUS * 2, VERTEX_RADIUS * 2)
            painter.end()

        if self.click == 2:
            brush = QtGui.QBrush(QtGui.QColor(FIELD_COLOR))
            painter.setBrush(brush)
            painter.drawEllipse(self.event_x - VERTEX_RADIUS, self.event_y - VERTEX_RADIUS,
                                VERTEX_RADIUS * 2, VERTEX_RADIUS * 2)
            painter.end()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.click = 1
            self.event_x, self.event_y = event.x(), event.y()
            self.update()

        elif event.button() == QtCore.Qt.RightButton:
            self.click = 2
            self.event_x, self.event_y = event.x(), event.y()
            self.update()
