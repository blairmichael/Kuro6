from PyQt5.QtWidgets import (QDialog, QScrollArea, QVBoxLayout, QHBoxLayout, QLabel,
    QScrollArea)
from PyQt5.QtGui import QFont, QPixmap


class AnimeDialog(QDialog):
    def __init__(self, anime, titles, genres, related, studios):
        super(AnimeDialog, self).__init__()
        self.setFont(QFont('Calibri', 14))
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

        layout = QVBoxLayout()
        layout.addLayout(hbox1)
        layout.addLayout(hbox2)
        layout.addWidget(QLabel('Related:'))
        layout.addWidget(related_scroll)
        layout.addWidget(QLabel('Synopsis:'))
        layout.addWidget(synopsis_scroll)
        self.setLayout(layout)


class MangaDialog(QDialog):
    def __init__(self, manga, titles, genres, related, authors):
        super(MangaDialog, self).__init__()
        self.setFont(QFont('Calibri', 14))
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

        layout = QVBoxLayout()
        layout.addLayout(hbox1)
        layout.addLayout(hbox2)
        layout.addWidget(QLabel('Related:'))
        layout.addWidget(related_scroll)
        layout.addWidget(QLabel('Synopsis:'))
        layout.addWidget(synopsis_scroll)
        self.setLayout(layout)

