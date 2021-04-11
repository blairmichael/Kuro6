from PyQt5.QtWidgets import QCheckBox, QGroupBox, QHBoxLayout, QComboBox, QLabel, QSpinBox
from PyQt5.QtGui import QFont
from datetime import date


class SeasonFilters(QGroupBox):
    def __init__(self):
        super(SeasonFilters, self).__init__()
        self.setFont(QFont('Calibri', 14))
        self.setTitle('Season')
        self.year = QSpinBox()
        self.year.setRange(1917, date.today().year)
        self.year.setValue(self.year.maximum())
        self.year.setToolTip('<p><b>Year</b></p><p>Choose a year to search from.</p>')
        self.season = QComboBox()
        self.season.setPlaceholderText('Season')
        self.season.addItems(['Winter', 'Spring', 'Summer', 'Fall'])
        self.season.setToolTip('<p><b>Season</b></p><p>Choose a season to find anime from.</p>')
        self.shuffle = QCheckBox('Shuffle')
        self.shuffle.setToolTip('<p><b>Shuffle</b></p><p>Check to get a randomized result.</p>')
        layout = QHBoxLayout()
        layout.addWidget(QLabel('Year: '))
        layout.addSpacing(0)
        layout.addWidget(self.year)
        layout.addWidget(QLabel('Season: '))
        layout.addSpacing(0)
        layout.addWidget(self.season)
        layout.addWidget(self.shuffle)
        layout.addStretch()
        self.setLayout(layout)

    def data(self):
        return self.year.value(), self.season.currentText().lower(), self.shuffle.isChecked()

    def is_valid(self):
        return self.season.currentIndex() != -1

    def reset(self):
        self.year.setValue(self.year.maximum())
        self.season.setCurrentIndex(-1)

    def showEvent(self, event) -> None:
        self.reset()
        return super().showEvent(event)
