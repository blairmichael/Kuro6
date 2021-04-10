from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QProgressBar, QMessageBox, QLabel)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import (Qt, QThreadPool, QRunnable, QTimer, QObject, pyqtSignal, pyqtSlot)
from jikanpy.exceptions import APIException

from app.search.api import JikanAPI
from app.search.category_box import CategoryBox
from app.search.table import ResultsTable
from app.search.type_box import TypeBox
from app.search.radio_button import RadioButton
from app.search.library_dialog import AnimeDialog, MangaDialog
from app.search.search_bar import SearchBar
from app.search.genre_box import GenreBox
from app.search.season_filters import SeasonFilters
from app.search.results_page import ResultsPageBox
# from app.search.entry import AnimeEntry, MangaEntry


class WorkerSignals(QObject):
    finished = pyqtSignal()
    result = pyqtSignal(object)
    error = pyqtSignal(str)
    anime = pyqtSignal(tuple)
    manga = pyqtSignal(tuple)


class Worker(QRunnable):
    api = JikanAPI()
    def __init__(self, type_, *args, **kwargs):
        super(Worker, self).__init__()
        self.type = type_
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            if self.type == 'search':
                results = self.api.search(*self.args, **self.kwargs)
                self.signals.result.emit(results)
            elif self.type == 'id':
                results = self.api.id(*self.args, **self.kwargs)
                self.signals.result.emit(results)
            elif self.type == 'genre':
                results = self.api.genre(*self.args, **self.kwargs)
                self.signals.result.emit(results)
            elif self.type == 'top':
                results = self.api.top(*self.args, **self.kwargs)
                self.signals.result.emit(results)
            elif self.type == 'season':
                results = self.api.season(*self.args, **self.kwargs)
                self.signals.result.emit(results)
            elif self.type == 'anime':
                results = self.api.anime(*self.args, **self.kwargs)
                self.signals.result.emit(results)
            elif self.type == 'manga':
                results = self.api.manga(*self.args, **self.kwargs)
                self.signals.result.emit(results)
        except APIException as e:
            self.signals.error.emit(e.error_json['message'])
        finally:
            self.signals.finished.emit()

class DatabaseWorker(QRunnable):
    pass


class SearchWidget(QWidget):
    def __init__(self, thread_pool):
        super(SearchWidget, self).__init__()
        # create library here
        self.thread_pool = thread_pool
        self.timer = QTimer()
        self.timer.setInterval(200)
        # self.timer.timeout.connect(self.update_progress)

        self.setFont(QFont('Calibri', 14))

        self.search_bar = SearchBar()
        self.radio_id = RadioButton('ID', '<p><b>ID</b></p><p>Check to search by ID</p>')
        self.radio_id.toggled.connect(self.id_toggled)
        self.radio_genre = RadioButton('Genre', '<p><b>Genre</b></p><p>Check to search by genre</p>')
        self.radio_genre.toggled.connect(self.genre_toggled)
        self.radio_top = RadioButton('Top', '<p><b>Top</b></p><p>Check to search for the top anime/manga.</p>')
        self.radio_top.toggled.connect(self.top_toggled)
        self.radio_season = RadioButton('Season', '<p><b>Season</b></p><p>Check to search by season</p>')
        self.radio_season.toggled.connect(self.season_toggled)
        self.category_box = CategoryBox()
        # self.category_box.currentIndexChanged.connect(self.category_changed)
        self.type_box = TypeBox()
        reset_button = QPushButton('Reset Filters')
        reset_button.clicked.connect(self.reset_filters)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.search_bar)
        hbox1.addWidget(self.radio_id)
        hbox1.addWidget(self.radio_genre)
        hbox1.addWidget(self.radio_top)
        hbox1.addWidget(self.radio_season)
        hbox1.addSpacing(40)
        hbox1.addWidget(QLabel('Category: '))
        hbox1.addSpacing(0)
        hbox1.addWidget(self.category_box)
        hbox1.addWidget(QLabel('Type: '))
        hbox1.addSpacing(0)
        hbox1.addWidget(self.type_box)
        hbox1.addWidget(reset_button)

        self.genre_box = GenreBox()
        self.season_filters = SeasonFilters()
        self.results_page_box = ResultsPageBox()

        self.table = ResultsTable()
        # self.table.doubleClicked.connect(lambda: self.open_dialog(self.table.selectedItems()[0].data(Qt.UserRole)))

        self.progress_bar = QProgressBar()
        self.search_button = QPushButton('Search')
        # self.search_button.clicked.connect(self.search_clicked)

        layout = QVBoxLayout()
        layout.addLayout(hbox1)
        layout.addWidget(self.genre_box)
        layout.addWidget(self.season_filters)
        layout.addWidget(self.results_page_box)
        layout.addWidget(self.table)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.search_button)
        self.setLayout(layout)

        self.season_filters.hide()
        self.results_page_box.hide()

    @staticmethod
    def error(message):
        msg = QMessageBox()
        msg.setWindowTitle('Invalid Search!')
        msg.setText(message)
        msg.setFont(QFont('Calibri', 12))
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()

    def reset_filters(self):
        self.search_bar.title_mode()
        self.radio_id.setChecked(False)
        self.radio_genre.setChecked(False)
        self.radio_top.setChecked(False)
        self.radio_season.setChecked(False)
        self.category_box.reset()
        self.type_box.reset()
        self.genre_box.show()
        self.results_page_box.hide()
        self.season_filters.hide()
        self.table.setRowCount(0)
        self.progress_bar.setValue(0)

    def id_toggled(self, state):
        if state:
            self.radio_genre.setChecked(False)
            self.radio_top.setChecked(False)
            self.radio_season.setChecked(False)
            self.genre_box.hide()
            self.season_filters.hide()
            self.results_page_box.hide()
            self.search_bar.id_mode()
        else:
            self.search_bar.title_mode()
            self.genre_box.show()

    def genre_toggled(self, state):
        if state:
            self.radio_id.setChecked(False)
            self.radio_top.setChecked(False)
            self.radio_season.setChecked(False)
            self.genre_box.show()
            self.season_filters.hide()
            self.results_page_box.show()
            self.results_page_box.mode(1)
            self.search_bar.disable()
        else:
            self.search_bar.title_mode()
            self.results_page_box.hide()

    def top_toggled(self, state):
        if state:
            self.radio_id.setChecked(False)
            self.radio_genre.setChecked(False)
            self.radio_season.setChecked(False)
            self.genre_box.hide()
            self.season_filters.hide()
            self.results_page_box.show()
            self.results_page_box.mode(0)
            self.search_bar.disable()
        else:
            self.search_bar.title_mode()
            self.genre_box.show()
            self.results_page_box.hide()

    def season_toggled(self, state):
        if state:
            self.radio_id.setChecked(False)
            self.radio_genre.setChecked(False)
            self.radio_top.setChecked(False)
            self.genre_box.hide()
            self.season_filters.show()
            self.results_page_box.hide()
            self.search_bar.disable()
        else:
            self.search_bar.title_mode()
            self.genre_box.show()
            self.season_filters.hide()

    def category_changed(self):
        self.type_box.mode(self.category_box.index(), self.radio_top.isChecked())

    def check_search(self):
        if not self.search_bar.is_valid_query():
            self.error('Not enough characters (Min: 2)!')
            return False
        elif not self.category_box.is_valid():
            self.error('Category not chosen!')
            return False
        elif not self.type_box.is_valid():
            self.error('Type not chosen!')
            return False
        elif not self.genre_box.is_valid_text():
            self.error('Genre(s) not chosen!')
            return False
        else:
            return True

    def check_id(self):
        if not self.search_bar.is_valid_id():
            return False
        elif not self.category_box.is_valid():
            self.error('Category not chosen!')
            return False
        else:
            return True

    def check_genre(self):
        if not self.genre_box.is_valid_genre():
            self.error('Must select one genre!')
            return False
        elif not self.category_box.is_valid():
            self.error('Category not chosen!')
            return False
        else:
            return True

    def check_top(self):
        if not self.category_box.is_valid_genre():
            self.error('Category not chosen!')
            return False
        elif not self.type_box.is_valid():
            self.error('Type not chosen!')
            return False
        else:
            return True

    def check_season(self):
        if not self.season_filters.is_valid():
            self.error('Must select a year and season!')
            return False
        else:
            return True
