from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QProgressBar, QMessageBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import (Qt, QThreadPool, QRunnable, QTimer, QObject, pyqtSignal, pyqtSlot)#

from app.search.api import JikanAPI
from app.search.category_box import CategoryBox
from app.search.results_table import ResultsTable
from app.search.type_box import TypeBox
from app.search.radio_button import RadioButton
from app.search.library_dialog import AnimeDialog, MangaDialog
from app.search.search_bar import SearchBar
from app.search.genre_box import GenreBox
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
        pass

