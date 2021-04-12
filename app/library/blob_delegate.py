from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon


class BlobDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        QStyledItemDelegate.__init__(self, parent)

    def paint(self, painter, option, index):
        path = index.model().data(index.model().index(index.row(), 1), Qt.DisplayRole)

        pixmap = QPixmap()
        pixmap.loadFromData(path)

        icon = QIcon(pixmap)
        icon.paint(painter, option.rect, Qt.AlignCenter)

    def sizeHint(self, option, index):
        return QSize(100, 140)
