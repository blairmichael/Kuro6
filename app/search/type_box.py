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
                self.addItems()
            else:
                self.addItems()
        else:
            if top:
                self.addItems()
            else:
                self.addItems()

    def typ(self):
        return self.currentText().lower()

    def is_valid(self):
        return self.currentIndex() != -1

    def reset(self):
        self.clear()
