from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QDialog, QScrollArea, QVBoxLayout, QHBoxLayout, QLabel,
    QScrollArea)
from PyQt5.QtGui import QFont, QPixmap

from app.library.update_dialogs import UpdateAnime, UpdateManga

class AnimeDialog(QDialog):
    reset = pyqtSignal()

    def __init__(self, connection, anime, titles, genres, related, studios):
        super(AnimeDialog, self).__init__()
        self.setFont(QFont('Calibri', 14))
        self.connection = connection
        id_, cover, title, type_, progress, episodes_watched, rating, source, status, episodes, duration, synopsis, premiered = anime
        hbox1 = QHBoxLayout()
        hbox1.addWidget(QLabel(f'<font size=18><b>{title}</b></f>'))
        hbox1.addWidget(QLabel(f'Rating: {rating}/10'))

        image = QPixmap()
        image.loadFromData(cover)
        image_label = QLabel()
        image_label.setPixmap(image)
        image_label.setFixedSize(image.size())

        info = {
            'ID:': id_,
            'Synonyms:': titles,
            'Type:': type_,
            'Status:': status,
            'Source:': source,
            'Progress:': progress,
            'Episodes:': f'{episodes_watched}/{episodes if episodes else "?"}',
            'Rating:': str(rating),
            'Premiered:': premiered,
            'Duration:': duration,
            'Genres:': genres,
            'Studios:': studios
        }

        text = str()
        for key, value in info.items():
            text += (f'<p><b>{key} </b> {value}</p>')
        info_label = QLabel(text)
        info_label.setFont(QFont('Calibri', 14))
        info_label.setWordWrap(True)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(image_label)
        hbox2.addWidget(info_label)

        r_text = str()
        for key, value in related.items():
            r_text += (f'<p><b>{key}: </b> {value}</p>')

        related_label = QLabel(r_text)
        related_label.setFont(QFont('Calibri', 14))
        related_label.setWordWrap(True)
        related_scroll = QScrollArea()
        related_scroll.setWidgetResizable(True)
        related_scroll.setWidget(related_label)
        related_scroll.setMinimumHeight(150)


        synopsis_label = QLabel(synopsis)
        synopsis_label.setFont(QFont('Calibri', 16))
        synopsis_label.setWordWrap(True)
        synopsis_scroll = QScrollArea()
        synopsis_scroll.setWidgetResizable(True)
        synopsis_scroll.setWidget(synopsis_label)
        synopsis_scroll.setMinimumHeight(200)

        update_box = UpdateAnime(self.connection, id_, progress, (episodes_watched, episodes), (rating, 10))

        hbox3 = QHBoxLayout()
        hbox3.addWidget(update_box)
        hbox3.addWidget(synopsis_scroll)

        layout = QVBoxLayout()
        layout.addLayout(hbox1)
        layout.addLayout(hbox2)
        layout.addWidget(QLabel('Related:'))
        layout.addWidget(related_scroll)
        # layout.addWidget(QLabel('Synopsis:'))
        layout.addLayout(hbox3)
        self.setLayout(layout)

    def closeEvent(self, event):
        self.reset.emit()
        return super().closeEvent(event)


class MangaDialog(QDialog):
    reset = pyqtSignal()

    def __init__(self, connection, manga, titles, genres, related, authors):
        super(MangaDialog, self).__init__()
        self.setFont(QFont('Calibri', 14))
        self.connection = connection
        id_, cover, title, type_, progress, volumes_read, chapters_read, rating, status, volumes, chapters, synopsis, published = manga
        hbox1 = QHBoxLayout()
        hbox1.addWidget(QLabel(f'<font size=18><b>{title}</b></f>'))
        hbox1.addWidget(QLabel(f'Rating: {rating}/10'))

        image = QPixmap()
        image.loadFromData(cover)
        image_label = QLabel()
        image_label.setPixmap(image)
        image_label.setFixedSize(image.size())

        info = {
            'ID:': id_,
            'Synonyms:': titles,
            'Type:': type_,
            'Status:': status,
            'Progress:': progress,
            'Volumes:': f'{volumes_read}/{volumes if volumes else "?"}',
            'Chapters:': f'{chapters_read}/{chapters if chapters else "?"}',
            'Rating:': str(rating),
            'Published:': published,
            'Genres:': genres,
            'Authors:': authors
        }

        text = str()
        for key, value in info.items():
            text += (f'<p><b>{key} </b> {value}</p>')
        info_label = QLabel(text)
        info_label.setFont(QFont('Calibri', 14))
        info_label.setWordWrap(True)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(image_label)
        hbox2.addWidget(info_label)

        r_text = str()
        for key, value in related.items():
            r_text += (f'<p><b>{key}: </b> {value}</p>')

        related_label = QLabel(r_text)
        related_label.setFont(QFont('Calibri', 14))
        related_label.setWordWrap(True)
        related_scroll = QScrollArea()
        related_scroll.setWidgetResizable(True)
        related_scroll.setWidget(related_label)
        related_scroll.setMinimumHeight(150)


        synopsis_label = QLabel(synopsis)
        synopsis_label.setFont(QFont('Calibri', 16))
        synopsis_label.setWordWrap(True)
        synopsis_scroll = QScrollArea()
        synopsis_scroll.setWidgetResizable(True)
        synopsis_scroll.setWidget(synopsis_label)
        synopsis_scroll.setMinimumHeight(200)

        update_box = UpdateManga(self.connection, id_, progress, (volumes_read, volumes), (chapters_read, chapters), (rating, 10))

        hbox3 = QHBoxLayout()
        hbox3.addWidget(update_box)
        hbox3.addWidget(synopsis_scroll)

        layout = QVBoxLayout()
        layout.addLayout(hbox1)
        layout.addLayout(hbox2)
        layout.addWidget(QLabel('Related:'))
        layout.addWidget(related_scroll)
        layout.addWidget(QLabel('Synopsis:'))
        layout.addLayout(hbox3)
        self.setLayout(layout)

    def closeEvent(self, event):
        self.reset.emit()
        return super().closeEvent(event)


