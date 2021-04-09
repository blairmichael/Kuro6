from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QFont


class SearchBar(QLineEdit):
    def __init__(self):
        super(SearchBar, self).__init__()
        self.setFont(QFont('Calibri', 18))
        self.setPlaceholderText('Enter title here.')
        self.setToolTip('<b>Search:</b>title<p>Enter text here to search for anime/manga by title.</p>')
        self.setFixedHeight(25)
        self.setFrame(False)

    def query(self):
        return self.text().lower().replace(' ', '%20')

    def mal_id(self):
        return self.text()

    def is_valid_query(self):
        return self.query().isalnum()

    def is_valid_id(self):
        return self.mal_id().isnumeric()

    def disable(self):
        self.clear()
        self.setEnabled(False)

    def title_mode(self):
        self.clear()
        self.setPlaceholderText('Enter title here.')
        self.setToolTip('<b>Search:</b>title<p>Enter text here to search for anime/manga by title.</p>')
        self.setEnabled(True)

    def id_mode(self):
        self.clear()
        self.setPlaceholderText('Enter ID here.')
        self.setToolTip('<b>Search:</b>ID<p>Enter digits here to search for anime/manga by ID.</p>')
        self.setEnabled(True)
