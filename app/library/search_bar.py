from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QFont


class SearchBar(QLineEdit):
    def __init__(self):
        super(SearchBar, self).__init__()
        self.setFont(QFont('Calibri', 16))
        self.setFrame(False)
        self.setFixedHeight(25)
        self.setPlaceholderText('Enter title here...')
        self.setToolTip('<b>Search</b><p>Enter text here to search your library.</p>')

    def query(self):
        return self.text().lower()

    def reset(self):
        self.clear()
