from PyQt5.QtWidgets import (QDialog, QDialogButtonBox, QLabel, QSpinBox, QFormLayout, QComboBox,
    QGridLayout, QMessageBox, QVBoxLayout, QPushButton)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QRunnable, QObject, Qt, pyqtSignal, pyqtSlot
from jikanpy import APIException

from app.search.display_dialogs import ViewManga, ViewAnime
from app.search.api import JikanAPI


class WorkerSignals(QObject):
    finished = pyqtSignal()
    result = pyqtSignal(object)
    error = pyqtSignal(str)
    info = pyqtSignal(tuple)


class Worker(QRunnable):
    api = JikanAPI()
    def __init__(self, category, *args, **kwargs):
        super(Worker, self).__init__()
        self.category = category
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            if self.category.lower() == 'anime':
                results = self.api.anime_info(*self.args, **self.kwargs)
            else:
                results = self.api.manga_info(*self.args, **self.kwargs)
        except APIException as e:
            self.signals.error.emit(e.error_json['message'])
        finally:
            self.signals.info.emit(results)


class ProgressBox(QComboBox):
    def __init__(self, anime=True):
        super(ProgressBox, self).__init__()
        self.setFont(QFont('Calibri', 14))
        if anime:
            self.addItems(['Planning', 'Watching', 'Completed', 'Dropped'])
        else:
            self.addItems(['Planning', 'Reading', 'Completed', 'Dropped'])

    def progress(self):
        return self.currentText()


class SpinBox(QSpinBox):
    def __init__(self, range_):
        super(SpinBox, self).__init__()
        self.setFont(QFont('Calibri', 14))
        self.setRange(0, range_)


class Dialog(QDialog):
    def __init__(self, thread_pool, mal_id, pixmap, title, category):
        super(Dialog, self).__init__()
        self.setFont(QFont('Calibri', 14))
        self.thread_pool = thread_pool
        self.id = mal_id
        self.category = category
        self.setWindowTitle('Add to library!')

        image = QLabel()
        image.setPixmap(pixmap)
        image.setFixedSize(pixmap.size())

        title_label = QLabel(f'Would you like to add <b>{title}</b> to your library?')
        title_label.setWordWrap(True)
        title_label.setFont(QFont('Calibri', 18))

        self.input_form = QFormLayout()

        view_info = QPushButton('View Info')
        view_info.clicked.connect(self.info_clicked)

        dialog_buttons = QDialogButtonBox()
        dialog_buttons.addButton(QDialogButtonBox.Ok)
        dialog_buttons.addButton(QDialogButtonBox.Cancel)
        dialog_buttons.accepted.connect(self.accept)
        dialog_buttons.rejected.connect(self.reject)

        layout = QGridLayout()
        layout.addWidget(title_label, 0, 0, 1, 2)
        layout.addWidget(image, 1, 0)
        layout.addLayout(self.input_form, 1, 1)
        layout.addWidget(view_info, 2, 0)
        layout.addWidget(dialog_buttons, 2, 1)

        self.setLayout(layout)

    @staticmethod
    def error(message):
        msg = QMessageBox()
        msg.setWindowTitle('Error!')
        msg.setText(message)
        msg.setFont(QFont('Calibri', 12))
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()


class AnimeDialog(Dialog):
    def __init__(self, thread_pool, mal_id, pixmap, title, category, episodes):
        super().__init__(thread_pool, mal_id, pixmap, title, category)
        self.progress = ProgressBox()
        self.episodes = SpinBox(episodes)
        self.rating = SpinBox(10)

        self.input_form.addRow(QLabel('Progress:'), self.progress)
        self.input_form.addRow(QLabel('Episodes:'), self.episodes)
        self.input_form.addRow(QLabel('Ratings:'), self.rating)

    def info_clicked(self):
        worker = Worker('anime', self.id)
        worker.signals.info.connect(self.display_dialog)
        worker.signals.error.connect(self.error)

        self.thread_pool.start(worker)

    @staticmethod
    def display_dialog(data):
        dialog = ViewAnime(*data)
        dialog.exec_()

    def data(self):
        return self.id, self.progress.progress(), self.episodes.value(), self.rating.value()


class MangaDialog(Dialog):
    def __init__(self, thread_pool, mal_id, pixmap, title, category, volumes, chapters=None):
        super().__init__(thread_pool, mal_id, pixmap, title, category)
        self.progress = ProgressBox()
        self.volumes = SpinBox(volumes if volumes else 10000)
        self.chapters = SpinBox(chapters if chapters else 10000)
        self.rating = SpinBox(10)

        self.input_form.addRow(QLabel('Progress:'), self.progress)
        self.input_form.addRow(QLabel('Volumes:'), self.volumes)
        self.input_form.addRow(QLabel('Chapters:'), self.chapters)
        self.input_form.addRow(QLabel('Ratings:'), self.rating)

    def info_clicked(self):
        worker = Worker('manga', self.id)
        worker.signals.info.connect(self.display_dialog)
        worker.signals.error.connect(self.error)

        self.thread_pool.start(worker)

    @staticmethod
    def display_dialog(data):
        dialog = ViewManga(*data)
        dialog.exec_()

    def data(self):
        return self.id, self.progress.progress(), self.volumes.value(), self.chapters.value(), self.rating.value()
