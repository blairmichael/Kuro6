from PyQt5.QtWidgets import QTableView, QAbstractItemView, QStyledItemDelegate
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import QSize, Qt


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


class TableWidget(QTableView):
    def __init__(self):
        super(TableWidget, self).__init__()
        self._font = QFont('Calibri', 14)
        self.setFont(self._font)
        self.setItemDelegateForColumn(1, BlobDelegate(self))
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.verticalHeader().setVisible(False)
        self.setShowGrid(False)
        self.setWordWrap(True)
        self.setFixedWidth(600)
