from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView, QStyledItemDelegate
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import QSize, Qt
import requests


class ReadOnlyDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        pass


class ResultsTable(QTableWidget):
    def __init__(self):
        super(ResultsTable, self).__init__()
        self.setFont(QFont('Calibri', 14))
        self.setColumnCount(5)
        self.setIconSize(QSize(150, 150))
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)
        self.setShowGrid(False)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

    def anime(self, data):
        url, mal_id, title, category, type_, episodes = data
        image = QPixmap()
        image.loadFromData(requests.get(url).content)
        cover = QTableWidgetItem()
        cover.setIcon(QIcon(image))
        cover.setData(Qt.UserRole, (mal_id, image, title, category, episodes))
        row = self.rowCount()
        self.insertRow(row)
        self.setItem(row, 0, cover)
        self.setItem(row, 1, QTableWidgetItem(f'<font size=16>{title}</f>'))
        self.setItem(row, 2, QTableWidgetItem(f'Type:{type_}'))
        self.setItem(row, 3, QTableWidgetItem(f'Episodes: {episodes}'))
        self.setItemDelegateForRow(row, ReadOnlyDelegate(self))
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def manga(self, data):
        try:
            url, mal_id, title, category, type_, volumes, chapters = data
        except ValueError:
            url, mal_id, title, category, type_, volumes = data
            chapters = None
        image = QPixmap()
        image.loadFromData(requests.get(url).content)
        cover = QTableWidgetItem()
        cover.setIcon(QIcon(image))
        cover.setData(Qt.UserRole, (mal_id, image, title, category, volumes, chapters))
        row = self.rowCount()
        self.insertRow(row)
        self.setItem(row, 0, cover)
        self.setItem(row, 1, QTableWidgetItem(f'<font size=16>{title}</f>'))
        self.setItem(row, 2, QTableWidgetItem(f'Type:{type_}'))
        self.setItem(row, 3, QTableWidgetItem(f'Volumes: {volumes if volumes else "Unknown"}'))
        if chapters is not None:
            self.setItem(row, 4, QTableWidgetItem(f'Chapters: {chapters if volumes else "Unknown"}'))
        self.setItemDelegateForRow(row, ReadOnlyDelegate(self))
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def data(self):
        return self.selectedItems()[0].data(Qt.UserRole)
