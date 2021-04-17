from PyQt5.QtWidgets import QDialogButtonBox, QDialog, QLabel, QVBoxLayout
from PyQt5.QtGui import QFont


class AddToLibrary(QDialog):
    def __init__(self, name):
        super(AddToLibrary, self).__init__()
        self.setFont(QFont('Calibri', 14))
        self.setWindowTitle('Add to library!')
        self.label = QLabel(f'Would you like to add <b>{name}</b> to your library?')
        self.label.setWordWrap(True)
        self.dialog_buttons = QDialogButtonBox()
        self.dialog_buttons.addButton(QDialogButtonBox.Ok)
        self.dialog_buttons.addButton(QDialogButtonBox.Cancel)
        self.dialog_buttons.accepted.connect(self.accept)
        self.dialog_buttons.rejected.connect(self.reject)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.dialog_buttons)
        self.setLayout(layout)