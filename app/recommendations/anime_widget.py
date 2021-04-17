from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtSql import QSqlQueryModel, QSqlQuery
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont

from app.recommendations.page_selector import PageSelector
from app.recommendations.table import TableWidget
from app.recommendations.info_widget import InfoWidget

class TableLayout(QVBoxLayout):
    switch_page = pyqtSignal()
    record_clicked = pyqtSignal(int)
    double_clicked = pyqtSignal(tuple)

    def __init__(self, database, count):
        super(TableLayout, self).__init__()
        self.database = database
        self.switch = QPushButton('Switch to Manga.')
        self.switch.setFont(QFont('Calibri', 14))
        self.switch.clicked.connect(lambda: self.switch_page.emit())
        self.table = TableWidget()
        self.table.clicked.connect(lambda: self.record_clicked.emit(self.table.selectedIndexes()[0].data()))
        self.table.doubleClicked.connect(lambda: self.double_clicked.emit((self.table.selectedIndexes()[2].data(), self.table.selectedIndexes()[0].data())))
        self.model = QSqlQueryModel()
        self.table.setModel(self.model)
        self.table.setModel(self.model)
        self.query = QSqlQuery(db=self.database)
        self.query.prepare("""
                SELECT rank, cover, title, type, score
                FROM anime
                WHERE rank BETWEEN 1 AND 10
                ORDER BY rank
                """)
        self.query.exec_()
        self.model.setQuery(self.query)
        self.page_selector = PageSelector((count // 10) + 1)
        self.page_selector.page_bounds.connect(self.update_table)
        self.table.resizeRowsToContents()
        self.table.resizeColumnToContents(0)
        self.table.setColumnWidth(2, 250)
        self.addWidget(self.switch)
        self.addWidget(self.table)
        self.addLayout(self.page_selector)

    def update_table(self, bounds):
        self.query.prepare(f"""
                SELECT rank, cover, title, type, score
                FROM anime
                WHERE rank BETWEEN {bounds[0]} AND {bounds[1]}
                ORDER BY rank
                """)
        self.query.exec_()
        self.model.setQuery(self.query)
        self.table.resizeRowsToContents()
        self.table.resizeColumnToContents(0)
        self.table.setColumnWidth(2, 250)


class AnimeWidget(QWidget):
    rank = pyqtSignal(int)
    switch = pyqtSignal(int)
    double_clicked = pyqtSignal(tuple)

    def __init__(self, database, count):
        super(AnimeWidget, self).__init__()
        self.recommendation_table = TableLayout(database, count)
        self.recommendation_table.record_clicked.connect(self.rank)
        self.recommendation_table.double_clicked.connect(self.double_clicked)
        self.recommendation_table.switch_page.connect(lambda: self.switch.emit(1))
        self.info_widget = InfoWidget()
        layout = QHBoxLayout()
        layout.addLayout(self.recommendation_table)
        layout.addWidget(self.info_widget, 0, Qt.AlignTop)
        self.setLayout(layout)

    def table_clicked(self, data):
        anime, genres, studios = data
        self.info_widget.change_info(*anime, genres, studios)
