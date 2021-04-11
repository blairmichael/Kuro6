from PyQt5.QtWidgets import QComboBox
from PyQt5.QtGui import QFont


class TypeBox(QComboBox):
    def __init__(self):
        super(TypeBox, self).__init__()
        self.setFont(QFont('Calibri', 14))
        self.setPlaceholderText('---')
        self.setToolTip('<b>Type</b><p>Choose a type to search for.</p>')

    def mode(self, category, top):
        self.clear()
        if category:
            if top:
                self.addItems(['Manga', 'Novels', 'Oneshots', 'Doujin', 'Manwha', 'Manhua'])
            else:
                self.addItems(['Manga', 'Novel', 'Doujin', 'Manwha', 'Manhua'])
        else:
            if top:
                self.addItems(['Airing', 'Upcoming', 'Movie', 'OVA', 'Special'])
            else:
                self.addItems(['TV', 'OVA', 'Movie', 'Special', 'ONA'])

    def typ(self):
        return self.currentText().lower() if self.currentIndex() != -1 else None

    def is_valid(self):
        return self.currentIndex() != -1

    def reset(self):
        self.clear()
