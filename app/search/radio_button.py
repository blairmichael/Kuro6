from PyQt5.QtWidgets import QRadioButton
from PyQt5.QtGui import QFont


class RadioButton(QRadioButton):
    def __init__(self, text, tooltip):
        super(RadioButton, self).__init__()
        self.setFont(QFont('Calibri', 14))
        self.setText(text)
        self.setToolTip(tooltip)
        self.setAutoExclusive(False)
