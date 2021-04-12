from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QCheckBox, QGridLayout, QGroupBox
from PyQt5.QtGui import QFont


class GenreBox(QGroupBox):
    list_of_genres = ['action', 'adventure', 'cars', 'comedy', 'dementia', 'demons', 'mystery', 'drama', 'ecchi',
        'fantasy', 'game', 'hentai', 'historical', 'horror', 'kids', 'magics', 'martial arts', 'mecha',
        'music', 'parody', 'samurai', 'romance', 'school', 'sci fi', 'shoujo', 'shoujo ai', 'shounen',
        'shounen ai', 'space', 'sports', 'super power', 'vampire', 'yaoi', 'yuri', 'harem',
        'slice of life', 'supernatural', 'military', 'police', 'psychological', 'seinen', 'josei',
        'thriller', 'gender bender', 'doujinshi']
    changed = pyqtSignal()

    def __init__(self, category):
        super(GenreBox, self).__init__()
        self.setFont(QFont('Calibri', 14))
        self.setTitle('Genres')
        grid = QGridLayout()
        index = 0
        for i in range(4):
            for j in range(12):
                try:
                    checkbox = QCheckBox(self.list_of_genres[index].title())
                    checkbox.stateChanged.connect(lambda: self.changed.emit())
                    grid.addWidget(checkbox, i, j)
                    index += 1
                except IndexError:
                    pass
        self.setLayout(grid)

        if category == 'anime':
            self.layout().itemAt(43).widget().hide()
            self.layout().itemAt(44).widget().hide()

    def genres(self):
        genres_list = list()
        for i in range(self.layout().count()):
            if self.layout().itemAt(i).widget().isChecked():
                genres_list.append(self.layout().itemAt(i).widget().text().lower())
        return genres_list

    def reset(self):
        for i in range(self.layout().count()):
            self.layout().itemAt(i).widget().setChecked(False)

