from PyQt5.QtWidgets import QTableView, QAbstractItemView
from PyQt5.QtGui import QFont

from app.library.blob_delegate import BlobDelegate


class TableWidget(QTableView):
    def __init__(self):
        super(TableWidget, self).__init__()
        self.setFont(QFont('Calibri', 14))
        self.setItemDelegateForColumn(1, BlobDelegate(self))
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setShowGrid(False)
        self.verticalHeader().setVisible(False)

    def data(self):
        return self.selectedIndexes()[0].data()
