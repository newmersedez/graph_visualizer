from PyQt5.QtGui import QPainter, QTransform
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtWidgets import (QAction, QMenu, QApplication,
                             QGraphicsView, QGraphicsScene,
                             QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsItem)


class View(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)

    def contextMenuEvent(self, e):
        pos = e.pos()
        mnu = QMenu()
        mnu.addAction('Add vertex').setObjectName('add vertex')
        mnu.addAction('Delete vertex').setObjectName('delete vertex')
        mnu.addAction('Clear all').setObjectName('clear all')
        ret = mnu.exec_(self.mapToGlobal(pos))
        if not ret:
            return
        obj = ret.objectName()
        if obj == 'add vertex':
            item = QGraphicsEllipseItem(0, 0, 50, 50)
            item.setBrush(Qt.green)
            item.setFlags(QGraphicsItem.ItemIsMovable)
            self.scene.addItem(item)
            item.setPos(self.mapToScene(pos))
        elif obj == 'delete vertex':
            pos_x, pos_y = e.pos().x(), e.pos().y()
            item = self.scene.itemAt(pos_x, pos_y, QTransform())
            if item is not None:
                self.scene.removeItem(item)

    def resizeEvent(self, e):
        w, h = self.viewport().width(), self.viewport().height()
        self.setSceneRect(0, 0, w, h)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = View()
    w.resize(600, 400)
    w.show()
    sys.exit(app.exec_())