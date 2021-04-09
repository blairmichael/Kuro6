from app.search_widget import SearchWidget

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import QThreadPool
    import sys
    app = QApplication(sys.argv)
    window = SearchWidget(QThreadPool())
    window.show()
    app.setStyle('fusion')
    sys.exit(app.exec_())