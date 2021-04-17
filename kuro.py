from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialogButtonBox, QLabel, QTabWidget, QDialog, QVBoxLayout

from app.database.library import Library
from app.database.recommendations import Recommendations
from app.search_widget import SearchWidget
from app.library.library import LibraryTabs
from app.recommendations_widget import RecommendationsWidget


class OptionalRecommendations(QDialog):
    def __init__(self):
        super(OptionalRecommendations, self).__init__()
        self.setWindowTitle(f'Refresh Recommendations')
        self.setFont(QFont('Calibri', 12))
        dialog_buttons = QDialogButtonBox()
        dialog_buttons.addButton(QDialogButtonBox.Ok)
        dialog_buttons.addButton(QDialogButtonBox.Cancel)
        dialog_buttons.accepted.connect(self.accept)
        dialog_buttons.rejected.connect(self.reject)
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f'Do you want to refresh your recommendations? <p>Note: This will take a few minutes.</p>'))
        layout.addWidget(dialog_buttons)
        self.setLayout(layout)


class Kuro(QTabWidget):
    def __init__(self):
        super(Kuro, self).__init__()
        self.thread_pool = QThreadPool()
        self.library_connection = Library()
        self.recommendations_connection = Recommendations()
        self.search = SearchWidget(self.thread_pool, self.library_connection)
        self.library = LibraryTabs(self.library_connection)
        refresh = self.refresh_recommendations()
        self.recommendations = RecommendationsWidget(self.thread_pool, self.recommendations_connection, self.library_connection, refresh)
        self.addTab(self.search, 'Search')
        self.addTab(self.library, 'Library')
        self.addTab(self.recommendations, 'Recommendations')

    @staticmethod
    def refresh_recommendations():
        msg = OptionalRecommendations()
        x = msg.exec_()
        if x:
            return True
        else:
            return False

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication, QTabWidget
    from PyQt5.QtCore import QThreadPool, Qt
    from PyQt5.QtGui import QPalette, QColor
    import sys
    app = QApplication(sys.argv)
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(53, 53, 53))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Highlight, QColor(142, 45, 197).lighter())
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)
    app.setStyle('fusion')
    window = Kuro()
    window.show()
    sys.exit(app.exec_())