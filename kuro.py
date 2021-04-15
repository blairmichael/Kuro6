from PyQt5.QtWidgets import QTabWidget
from app.search_widget import SearchWidget
from app.database.library import Library
from app.library.library import LibraryTabs

class Kuro(QTabWidget):
    def __init__(self):
        super(Kuro, self).__init__()
        self.thread_pool = QThreadPool()
        self.library_connection = Library()
        self.search = SearchWidget(self.thread_pool, self.library_connection)
        self.library = LibraryTabs(self.library_connection)
        self.addTab(self.search, 'Search')
        self.addTab(self.library, 'Library')

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