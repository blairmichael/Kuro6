from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QLabel, QSpinBox, QComboBox
from PyQt5.QtGui import QFont


class ResultsPageBox(QGroupBox):
    def __init__(self):
        super(ResultsPageBox, self).__init__()
        self.setFont(QFont('Calibri', 14))
        self.setTitle('Filters')
        self.results = QComboBox()
        self.page = QSpinBox()
        self.page.setRange(1, 10)
        layout = QHBoxLayout()
        layout.addWidget(QLabel('Results: '))
        layout.addSpacing(0)
        layout.addWidget(self.results)
        layout.addWidget(QLabel('Page: '))
        layout.addSpacing(0)
        layout.addWidget(self.page)
        self.setLayout(layout)

    def data(self):
        return self.results.currentText().lower().split('-'), self.page.value()

    def mode(self, mode):
        if mode:
            self.reset()
            self.results.addItems(['1-10', '11-20', '21-30', '31-40', '41-50'])
        else:
            self.reset()
            self.results.addItems(['1-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81-90', '91-100'])

    def reset(self):
        self.results.clear()
        self.page.setValue(1)

    def showEvent(self, event) -> None:
        self.reset()
        return super().showEvent(event)
