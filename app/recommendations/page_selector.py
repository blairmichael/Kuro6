from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSignal


class PageSelector(QHBoxLayout):
    page_bounds = pyqtSignal(tuple)

    def __init__(self, limit):
        super(PageSelector, self).__init__()
        self._font = QFont('Calibri', 14)
        self.previous = QPushButton('<')
        self.previous.clicked.connect(self.previous_page)
        self.previous.setFont(self._font)
        self.next = QPushButton('>')
        self.next.clicked.connect(self.next_page)
        self.next.setFont(self._font)
        self.limit = limit
        self.page = 1
        self.page_label = QLabel(f'Page: {self.page}')
        self.page_label.setFont(self._font)
        self.addStretch(0)
        self.addWidget(self.previous)
        self.addStretch(0)
        self.addWidget(self.page_label)
        self.addStretch(0)
        self.addWidget(self.next)
        self.addStretch(0)
        self.disable_buttons()

    def previous_page(self):
        self.page -= 1
        self.page_label.setText(f'Page: {self.page}')
        self.page_bounds.emit(self.bounds)
        self.disable_buttons()

    def next_page(self):
        self.page += 1
        self.page_label.setText(f'Page: {self.page}')
        self.page_bounds.emit(self.bounds)
        self.disable_buttons()

    def disable_buttons(self):
        if self.page == 1:
            self.previous.setEnabled(False)
        elif self.page == self.limit:
            self.next.setEnabled(False)
        else:
            self.previous.setEnabled(True)
            self.next.setEnabled(True)

    @property
    def bounds(self):
        return (self.page*10 - 10) + 1, self.page*10