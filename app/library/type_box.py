from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QComboBox


class TypeBox(QComboBox):
    def __init__(self, category):
        super(TypeBox, self).__init__()
        self.setFont(QFont('Calibri', 14))
        self.setPlaceholderText('---')
        if category.lower() == 'anime':
            self.addItems(["TV", "OVA", "Movie", "Special", "ONA"])
        else:
            self.addItems(["Manga", "Novel", "Doujin", "Manhwa", "Manhua"])
        self.setToolTip('<b>Type</b><p>Select type to filter entries in your library.</p>')

    def type(self):
        return self.currentText() if self.currentIndex() != -1 else None

    def reset(self):
        self.setCurrentIndex(-1)
