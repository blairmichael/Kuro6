from PyQt5.QtWidgets import QComboBox
from PyQt5.QtGui import QFont


class CategoryBox(QComboBox):
    def __init__(self):
        super(CategoryBox, self).__init__()
        self.setFont(QFont('Calibri', 14))
        self.setPlaceholderText('---')
        self.setToolTip('<b>Category</b><p>Choose a category to search for anime or manga.</p>')
        self.addItems(['Anime', 'Manga'])

    def category(self):
        return self.currentText().lower()

    def index(self):
        return self.currentIndex()

    def reset(self):
        self.setCurrentIndex(-1)

    def is_valid(self):
        return self.currentIndex() != -1
