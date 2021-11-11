import sys

from PyQt5 import QtCore, QtGui

class GraphicsScene(QtGui.QGraphicsScene):
    def __init__(self, *args, **kwargs):
        QtGui.QGraphicsScene.__init__(self, *args, **kwargs)
        self.polygon = None

    def mousePressEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            self.polygon << ev.scenePos()
            item = QtGui.QGraphicsPolygonItem(self.polygon)
            item.setPen(QtGui.QPen(QtCore.Qt.red))
            item.setBrush(QtGui.QBrush(QtCore.Qt.red))
            self.addItem(item)
            # or
            # self.addPolygon(self.polygon, QtGui.QPen(QtCore.Qt.red), QtGui.QBrush(QtCore.Qt.red))
            self.polygon = None

        else:
            if self.polygon is None:
                self.polygon = QtGui.QPolygonF()
            self.polygon << ev.scenePos()


class Window(QtGui.QGraphicsView):
    def __init__(self, parent=None):
        QtGui.QGraphicsView.__init__(self, parent)
        self.scene = GraphicsScene(QtCore.QRectF(0, 0, 640, 480), self)
        self.scene.setBackgroundBrush(QtGui.QBrush(QtCore.Qt.darkGray, QtCore.Qt.SolidPattern))
        self.setScene(self.scene)
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)


class CityscapesLabelTool(QtGui.QMainWindow):
    def __init__(self, parent=None):

        QtGui.QMainWindow.__init__(self, parent)
        centralwidget = Window()
        self.setCentralWidget(centralwidget)

        centralwidget.scene.addPixmap(QtGui.QPixmap("exit.png"))


app = QtGui.QApplication(sys.argv)
GUI = CityscapesLabelTool()
GUI.show()
sys.exit(app.exec_())