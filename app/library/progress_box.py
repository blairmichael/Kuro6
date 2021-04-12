from PyQt5.QtWidgets import QComboBox
from PyQt5.QtGui import QFont


class ProgressBox(QComboBox):
    def __init__(self, category):
        super(ProgressBox, self).__init__()
        self.setFont(QFont('Calibri', 14))
        self.setPlaceholderText('---')
        if category.lower() == 'anime':
            self.addItems(['Planning', 'Watching', 'Completed', 'Dropped'])
        else:
            self.addItems(['Planning', 'Reading', 'Completed', 'Dropped'])
        self.setToolTip('<b>Progress</b><p>Select progress to filter entries in your library.</p>')

    def progress(self):
        return self.currentText() if self.currentIndex() != -1 else None

    def reset(self):
        self.setCurrentIndex(-1)
