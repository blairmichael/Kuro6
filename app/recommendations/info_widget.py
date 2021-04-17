from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QVBoxLayout, QScrollArea
from PyQt5.QtGui import QFont, QPixmap


class InfoWidget(QWidget):
    def __init__(self):
        super(InfoWidget, self).__init__()
        self._font = QFont('Calibri', 14)
        self.setFont(self._font)

        self.rank = QLabel()
        self.rank.setFont(QFont('Calibri', 18))
        self.image = QLabel()
        self.title = QLabel()
        self.title.setFont(QFont('Calibri', 24))
        self.title.setWordWrap(True)
        self.synopsis_title = QLabel()
        self.synopsis_title.setFont(QFont('Calibri', 18))
        self.synopsis = QLabel()
        self.synopsis.setWordWrap(True)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.synopsis)
        self.scroll_area.hide()

        self.info = QVBoxLayout()
        self.info_id = QLabel()
        self.info_type = QLabel()
        self.info_score = QLabel()
        self.info_genres = QLabel()
        self.info_creator = QLabel()
        self.info.addWidget(self.info_id)
        self.info.setSpacing(2)
        self.info.addWidget(self.info_type)
        self.info.setSpacing(2)
        self.info.addWidget(self.info_score)
        self.info.setSpacing(2)
        self.info.addWidget(self.info_genres)
        self.info.setSpacing(2)
        self.info.addWidget(self.info_creator)
        self.info.addStretch(0)

        top = QHBoxLayout()
        top.addWidget(self.title)
        top.addStretch(0)
        top.addWidget(self.rank)

        middle = QHBoxLayout()
        middle.addWidget(self.image)
        middle.setSpacing(2)
        middle.addLayout(self.info)

        layout = QVBoxLayout()
        layout.addLayout(top)
        layout.addLayout(middle)
        layout.addWidget(self.synopsis_title)
        layout.addWidget(self.scroll_area)

        self.setLayout(layout)
        self.setFixedWidth(650)

    def change_info(self, id_, image, title, type_, score, synopsis, rank, genres, creator, anime=True):
        self.rank.setText(f'<font color="Yellow">Rank: {rank}</font>')
        pixmap = QPixmap()
        pixmap.loadFromData(image)
        size = pixmap.size()
        self.image.setPixmap(pixmap)
        self.image.setFixedSize(size)
        self.title.setText(title)
        self.synopsis_title.setText('<b>Synopsis:</b>')
        self.synopsis.setText(synopsis)
        self.scroll_area.show()
        self.format_info(id_, type_, score, genres, creator, anime)

    def format_info(self, id_, type_, score, genres, creator, anime):
        for label in range(self.info.count()):
            widget = self.info.itemAt(label).widget()
            if widget:
                widget.setWordWrap(True)
                widget.setFont(QFont('Calibri', 14))
                widget.setStyleSheet('border-style: none none solid none; border-width: 1px; border-color: purple;')
        self.info_id.setText(f'<b>ID:</b> {id_}')
        self.info_type.setText(f'<b>Type:</b> {type_}')
        self.info_score.setText(f'<b>Score:</b> {score}')
        self.info_genres.setText(f'<b>Genres:</b> {genres}')
        self.info_creator.setText(f'<b>{"Studios" if anime else "Authors"}:</b> {creator}')
