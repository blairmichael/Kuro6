from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QTabWidget, QVBoxLayout, QWidget
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel

from app.library.search_bar import SearchBar
from app.library.type_box import TypeBox
from app.library.progress_box import ProgressBox
from app.library.genre_box import GenreBox
from app.library.table import TableWidget
from app.library.display_dialogs import AnimeDialog, MangaDialog


class Library(QWidget):
    def __init__(self, category, connection):
        super(Library, self).__init__()
        self.setFont(QFont('Calibri', 14))
        self.default = str()
        self.connection = connection

        self.database = QSqlDatabase('QSQLITE')
        self.database.setDatabaseName('library.db')
        self.database.open()

        self.search_bar = SearchBar()
        self.search_bar.textChanged.connect(self.query_)
        self.type_box = TypeBox(category)
        self.type_box.currentTextChanged.connect(self.query_)
        self.progress_box = ProgressBox(category)
        self.progress_box.currentTextChanged.connect(self.query_)
        reset_button = QPushButton('Reset filters')
        reset_button.clicked.connect(self.reset_filters)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.search_bar)
        hbox1.addWidget(QLabel('Type:'))
        hbox1.addSpacing(0)
        hbox1.addWidget(self.type_box)
        hbox1.addWidget(QLabel('Progress:'))
        hbox1.addSpacing(0)
        hbox1.addWidget(self.progress_box)
        hbox1.addWidget(reset_button)

        self.genre_box = GenreBox(category)
        self.genre_box.changed.connect(self.query_)

        self.table = TableWidget()

        layout = QVBoxLayout()
        layout.addLayout(hbox1)
        layout.addWidget(self.genre_box)
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.model = QSqlQueryModel()
        self.table.setModel(self.model)
        self.query = QSqlQuery(db=self.database)

    def reset_filters(self):
        self.search_bar.reset()
        self.type_box.reset()
        self.progress_box.reset()
        self.query.prepare(self.default)
        self.query.exec_()
        self.model.setQuery(self.query)
        self.table.resizeRowsToContents()
        self.table.resizeColumnsToContents()

    def query_(self):
        pass


class AnimeLibrary(Library):
    genre_dict = {
        'action': 1,
        'adventure': 2,
        'cars': 3,
        'comedy': 4,
        'dementia': 5,
        'demons': 6,
        'mystery': 7,
        'drama': 8,
        'ecchi': 9,
        'fantasy': 10,
        'game': 11,
        'hentai': 12,
        'historical': 13,
        'horror': 14,
        'kids': 15,
        'magics': 16,
        'martial arts': 17,
        'mecha': 18,
        'music': 19,
        'parody': 20,
        'samurai': 21,
        'romance': 22,
        'school': 23,
        'sci fi': 24,
        'shoujo': 25,
        'shoujo ai': 26,
        'shounen': 27,
        'shounen ai': 28,
        'space': 29,
        'sports': 30,
        'super power': 31,
        'vampire': 32,
        'yaoi': 33,
        'yuri': 34,
        'harem': 35,
        'slice of life': 36,
        'supernatural': 37,
        'military': 38,
        'police': 39,
        'psychological': 40,
        'thriller': 41,
        'seinen': 42,
        'josei': 43
    }
    def __init__(self, category, connection):
        super().__init__(category, connection)
        self.default = 'SELECT id, cover as Cover, title as Title, type as Type, progress as Progress, episodes_watched as Watched, rating as Rating FROM anime'
        self.query.prepare(self.default)
        self.query.exec_()
        self.model.setQuery(self.query)
        self.table.doubleClicked.connect(lambda: self.display(self.table.data()))
        self.table.resizeRowsToContents()
        self.table.resizeColumnsToContents()

    def query_(self):
        statement = self.default
        text = self.search_bar.query()
        type_ = self.type_box.type()
        progress = self.progress_box.progress()
        genres = self.genre_box.genres()

        # Checks if list in not empty - no genres selected/checked.
        if genres:
            pool = ', '.join(map(str, [self.genre_dict[genre] for genre in genres]))
            statement += f' WHERE anime.id in (SELECT anime_genres_link.id FROM anime_genres_link WHERE anime_genres_link.genre_id in ({pool}))'
        # Checks if the string is not empty - the search bar is empty.
        if text:
            # Checks if there is the string 'WHERE' in the current statement to avoid any error.
            if 'WHERE' in statement:
                statement += f" AND anime.title LIKE '%{text}%'"
            else:
                statement += f" WHERE anime.title LIKE '%{text}%'"
        # checks if the type is not None - type not selected.
        if type_:
            # Checks if there is the string 'WHERE' in the current statement to avoid any error.
            if 'WHERE' in statement:
                statement += f" AND anime.type = '{type_}'"
            else:
                statement += f" WHERE anime.type = '{type_}'"
        # Checks if progress is not None - progress not selected.
        if progress:
            # Checks if there is the string 'WHERE' in the current statement to avoid any error.
            if 'WHERE' in statement:
                statement += f" AND anime.progress = '{progress}'"
            else:
                statement += f" WHERE anime.progress = '{progress}'"
        self.query.prepare(statement)
        self.query.exec_()
        self.model.setQuery(self.query)
        self.table.resizeRowsToContents()
        self.table.resizeColumnsToContents()

    def display(self, id):
        data = self.connection.anime_info(id)
        dialog = AnimeDialog(*data)
        dialog.exec_()


class MangaLibrary(Library):
    genre_dict = {
        'action': 1,
        'adventure': 2,
        'cars': 3,
        'comedy': 4,
        'dementia': 5,
        'demons': 6,
        'mystery': 7,
        'drama': 8,
        'ecchi': 9,
        'fantasy': 10,
        'game': 11,
        'hentai': 12,
        'historical': 13,
        'horror': 14,
        'kids': 15,
        'magics': 16,
        'martial arts': 17,
        'mecha': 18,
        'music': 19,
        'parody': 20,
        'samurai': 21,
        'romance': 22,
        'school': 23,
        'sci fi': 24,
        'shoujo': 25,
        'shoujo ai': 26,
        'shounen': 27,
        'shounen ai': 28,
        'space': 29,
        'sports': 30,
        'super power': 31,
        'vampire': 32,
        'yaoi': 33,
        'yuri': 34,
        'harem': 35,
        'slice of life': 36,
        'supernatural': 37,
        'military': 38,
        'police': 39,
        'psychological': 40,
        'seinen': 41,
        'josei': 42,
        'doujinshi': 43,
        'gender bender': 44,
        'thriller': 45
    }
    def __init__(self, category, connection):
        super().__init__(category, connection)
        self.default ='SELECT id, cover as Cover, title as Title, type as Type, progress as Progress, volumes_read as Volumes, chapters_read as Chapters, rating as Rating FROM manga'
        self.query.prepare(self.default)
        self.query.exec_()
        self.model.setQuery(self.query)
        self.table.doubleClicked.connect(lambda: self.display(self.table.data()))
        self.table.resizeRowsToContents()
        self.table.resizeColumnsToContents()

    def query_(self):
        statement = self.default
        text = self.search_bar.query()
        type_ = self.type_box.type()
        progress = self.progress_box.progress()
        genres = self.genre_box.genres()

        # Checks if list in not empty - no genres selected/checked.
        if genres:
            pool = ', '.join(map(str, [self.genre_dict[genre] for genre in genres]))
            statement += f' WHERE manga.id in (SELECT manga_genres_link.id FROM manga_genres_link WHERE manga_genres_link.genre_id in ({pool}))'
        # Checks if the string is not empty - the search bar is empty.
        if text:
            # Checks if there is the string 'WHERE' in the current statement to avoid any error.
            if 'WHERE' in statement:
                statement += f" AND manga.title LIKE '%{text}%'"
            else:
                statement += f" WHERE manga.title LIKE '%{text}%'"
        # checks if the type is not None - type not selected.
        if type_:
            # Checks if there is the string 'WHERE' in the current statement to avoid any error.
            if 'WHERE' in statement:
                statement += f" AND manga.type = '{type_}'"
            else:
                statement += f" WHERE manga.type = '{type_}'"
        # Checks if progress is not None - progress not selected.
        if progress:
            # Checks if there is the string 'WHERE' in the current statement to avoid any error.
            if 'WHERE' in statement:
                statement += f" AND manga.progress = '{progress}'"
            else:
                statement += f" WHERE manga.progress = '{progress}'"
        self.query.prepare(statement)
        self.query.exec_()
        self.model.setQuery(self.query)
        self.table.resizeRowsToContents()
        self.table.resizeColumnsToContents()

    def display(self, id):
        data = self.connection.manga_info(id)
        dialog = MangaDialog(*data)
        dialog.exec_()


class LibraryTabs(QTabWidget):
    def __init__(self, connection):
        super(LibraryTabs, self).__init__()
        self.setFont(QFont('Calibri', 14))
        self.anime = AnimeLibrary('anime', connection)
        self.manga = MangaLibrary('manga', connection)
        self.addTab(self.anime, 'Anime')
        self.addTab(self.manga, 'Manga')

