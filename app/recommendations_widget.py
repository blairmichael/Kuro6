from PyQt5.QtCore import QObject, QRunnable, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QStackedLayout, QMessageBox
from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtGui import QFont
from jikanpy import APIException
from sqlite3 import Error

from app.recommendations.api import JikanAPI, AnimeEntry, MangaEntry
from app.recommendations.manga_widget import MangaWidget
from app.recommendations.anime_widget import AnimeWidget
from app.recommendations.add_to_library import AddToLibrary

from app.search.api import JikanAPI as LJikanAPI
from app.search.entry import AnimeEntry as LAnimeEntry
from app.search.entry import MangaEntry as LMangaEntry


class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(str)


class Worker(QRunnable):
    def __init__(self, api, connection, bubble1, bubble2):
        super(Worker, self).__init__()
        self.api = api
        self.connection = connection
        self.anime = bubble1[0]
        self.anime_genres = bubble1[1]
        self.manga = bubble2[0]
        self.manga_genres = bubble2[1]
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            self.anime(self.api, self.connection, self.anime_genres)
            self.manga(self.api, self.connection, self.manga_genres)
        except APIException as e:
            self.signals.error.emit(e.error_json['message'])
        finally:
            self.signals.finished.emit()


class DatabaseWorker(QRunnable):
    def __init__(self, library, category, *args, **kwargs):
        super(DatabaseWorker, self).__init__()
        self.library = library
        self.api = LJikanAPI()
        self.category = category
        self.id = args[0]
        if self.category.lower() == 'anime':
            self.inputs = ('Planning', 0, 0)
        else:
            self.inputs = ('Planning', 0, 0, 0)
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    def run(self):
        try:
            if self.category.lower() == 'anime':
                anime = self.api.anime(self.id)
                entry = LAnimeEntry(anime, self.inputs)
                self.library.add_anime(entry.data())
            else:
                manga = self.api.manga(self.id)
                entry = LMangaEntry(manga, self.inputs)
                self.library.add_manga(entry.data())
        except Error as e:
            self.signals.error.emit('Error occured when adding entry to library! Try Again!')
        finally:
            self.signals.finished.emit()


class RecommendationsWidget(QWidget):
    def __init__(self, thread_pool, recommendations, library, reset=False):
        super(RecommendationsWidget, self).__init__()
        self.api = JikanAPI()
        self.thread_pool = thread_pool
        self.recommendations_connection = recommendations
        self.library_connection = library
        self.anime_scores = self.get_scores(self.library_connection.get_anime_genres())
        self.manga_scores = self.get_scores(self.library_connection.get_manga_genres())
        if reset:
            self.populate()
        self.set_ranks(self.recommendations_connection.get_anime(), self.recommendations_connection.update_anime_rank, self.anime_scores)
        self.set_ranks(self.recommendations_connection.get_manga(), self.recommendations_connection.update_manga_rank, self.manga_scores)
        self.database = self.open_database()
        self.database.open()

        self.anime_widget = AnimeWidget(self.database, self.recommendations_connection.count_anime())
        self.anime_widget.switch.connect(self.change_widget)
        self.anime_widget.rank.connect(self.anime_clicked)
        self.anime_widget.double_clicked.connect(self.anime_double_clicked)
        self.manga_widget = MangaWidget(self.database, self.recommendations_connection.count_manga())
        self.manga_widget.switch.connect(self.change_widget)
        self.manga_widget.rank.connect(self.manga_clicked)
        self.manga_widget.double_clicked.connect(self.manga_double_clicked)

        self.main_layout = QStackedLayout()
        self.main_layout.addWidget(self.anime_widget)
        self.main_layout.addWidget(self.manga_widget)
        self.setLayout(self.main_layout)

    def change_widget(self, index):
        self.main_layout.setCurrentIndex(index)

    def anime_clicked(self, rank):
        self.anime_widget.table_clicked(self.recommendations_connection.anime_information(rank))

    def manga_clicked(self, rank):
        self.manga_widget.table_clicked(self.recommendations_connection.manga_information(rank))

    def anime_double_clicked(self, details):
        name, rank = details
        dlg = AddToLibrary(name)
        x = dlg.exec_()
        if x:
            id_ = self.recommendations_connection.get_anime_id(rank)
            self.library('anime', id_)

    def manga_double_clicked(self, details):
        name, rank = details
        dlg = AddToLibrary(name)
        x = dlg.exec_()
        if x:
            id_ = self.recommendations_connection.get_manga_id(rank)
            self.library('manga', id_)

    def library(self, category, id_):
        worker = DatabaseWorker(self.library_connection, category, id_)
        worker.signals.error.connect(self.error)
        worker.signals.finished.connect(self.added)
        self.thread_pool.start(worker)

    @staticmethod
    def open_database():
        database = QSqlDatabase('QSQLITE')
        database.setDatabaseName('recommendations.db')
        return database

    def get_scores(self, collection):
        # Stores a list of every instance of genre (genre id) the to list_of_genres.
        list_of_genres = [item[1] for item in collection]
        # Stores a dictionary for each unique genre in list_of_genres.
        # And calculates and stores the frequency of each unique genre in list_of_genres.
        dict_of_genres = {genre: {'frequency': list_of_genres.count(genre),
                                'score': 0
                                } for genre in set(list_of_genres)}
        min_ = 1
        max_ = max([dict_of_genres[genre]['frequency'] for genre in dict_of_genres])
        for genre in dict_of_genres:
            total = 0
            for item in collection:
                if item[1] == genre:
                    # Loops through the collection to calculate the sum of ratings given to the anime/manga.
                    total += item[0]
            average = total / dict_of_genres[genre]['frequency']
            # Tries to normalises the frequency of each genre.
            # And stores the product of the average rating and normalised frequency.
            try:
                normalised = (dict_of_genres[genre]['frequency'] - min_) / (max_ - min_)
                dict_of_genres[genre]['score'] = average * normalised
            # Catches the ZeroDivisionError and copies the average rating to the score key
            except ZeroDivisionError:
                dict_of_genres[genre]['score'] = average
        # Returns the dictionary
        return {genre: dict_of_genres[genre]['score'] for genre in dict_of_genres}

    @staticmethod
    def populate_anime(api, connection, genres):
        for genre in genres:
            try:
                responses = api.anime(genre)
                for response in responses:
                    entry = AnimeEntry(*response)
                    connection.add_anime(entry.data())
            except APIException as e:
                raise e

    @staticmethod
    def populate_manga(api, connection, genres):
        for genre in genres:
            try:
                responses = api.manga(genre)
                for response in responses:
                    entry = MangaEntry(*response)
                    connection.add_manga(entry.data())
            except APIException as e:
                raise e

    def populate(self):
        worker = Worker(self.api, self.recommendations_connection, (self.populate_anime, sorted(self.anime_scores, key=self.anime_scores.get, reverse=True)[:3]), (self.populate_manga, sorted(self.manga_scores, key=self.manga_scores.get, reverse=True)[:3]))
        worker.signals.finished.connect(self.completed)
        worker.signals.error.connect(self.error)
        self.thread_pool.start(worker)

    def set_ranks(self, collection, update, genres):
        # Loops through the collection and creates a dictionary entry for each unique anime/manga.
        dict_of_entries = {id_: {'genres': [item[1] for item in collection if item[0] == id_],
                                'score': 0
                                } for id_ in set([item[0] for item in collection])}
        # Loops through the dictionary.
        for entry in dict_of_entries:
            for genre in genres:
                # If the key is in the anime/manga genres then add the score to the anime/manga score.
                if genre in dict_of_entries[entry]['genres']:
                    dict_of_entries[entry]['score'] += genres[genre]
        # Formats the dictionary so it can be sorted by score.
        scores = {id_: dict_of_entries[id_]['score'] for id_ in dict_of_entries}
        # Passes the list of ids (keys) to the given update function to set the ranks in the database.
        update(sorted(scores, key=scores.get, reverse=True))

    @staticmethod
    def error(message):
        msg = QMessageBox()
        msg.setWindowTitle('Invalid Search!')
        msg.setText(message)
        msg.setFont(QFont('Calibri', 12))
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()

    @staticmethod
    def completed():
        msg = QMessageBox()
        msg.setWindowTitle('Updated recommendations!')
        msg.setText('Successfully updated the recommendations! Please restart application.')
        msg.setFont(QFont('Calibri', 12))
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    @staticmethod
    def added():
        msg = QMessageBox()
        msg.setWindowTitle('Added to library!')
        msg.setText('Successfully added to library!')
        msg.setFont(QFont('Calibri', 12))
        msg.setIcon(QMessageBox.Information)
        msg.exec_()



