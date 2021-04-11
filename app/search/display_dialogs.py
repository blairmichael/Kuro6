from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QScrollArea, QWidget, QSizePolicy)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
import requests


class ViewAnime(QDialog):
    def __init__(self, mal_id, image_url, title, synonyms, type_, source, episodes, synopsis,
        premiered, status, duration, score, studios, genres, related):
        super(ViewAnime, self).__init__()
        self.setWindowTitle(title)
        title_label = QLabel(title)
        title_label.setFont(QFont('Calibri', 18))
        title_label.setStyleSheet(
            'border-style: none none solid none; border-width: 1px; border-color: purple'
        )

        image = QPixmap()
        image.loadFromData(requests.get(image_url).content)
        image_label = QLabel()
        image_label.setPixmap(image)
        image_label.setFixedSize(image.size())

        synopsis_label = QLabel(synopsis)
        synopsis_label.setWordWrap(True)
        synopsis_label.setFont(QFont('Calibri', 12))
        synopsis_label.setStyleSheet(
            'border-style: solid none none none; border-width: 0.5px; border-color: purple;'
        )

        info_label = QLabel(self.format_info(mal_id, synonyms, type_, episodes, status, premiered,
            studios, source, duration, score, genres))
        info_label.setFont(QFont('Calibri', 14))
        related_scroll = self.format_related(related)

        hbox = QHBoxLayout()
        hbox.addWidget(image_label)
        hbox.setSpacing(2)
        hbox.addWidget(info_label)

        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addLayout(hbox)
        layout.addWidget(related_scroll)
        layout.addWidget(synopsis_label)

        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))

    @staticmethod
    def format_info(mal_id, synonyms, type_, episodes, status, premiered,
            studios, source, duration, score, genres):
        dictionary = {
            'ID:': str(mal_id),
            'Synonyms:': ', '.join(synonyms),
            'Type:': type_,
            'Genres': ', '.join(genre['name'] for genre in genres),
            'Episodes:': str(episodes),
            'Status:': status,
            'Premiered:': premiered,
            'Studios:': ', '.join([studio['name'] for studio in studios]),
            'Source:': source,
            'Duration:': duration,
            'Score:': str(score)
        }
        text = str()
        print(dictionary.items())
        for key, value in dictionary.items():
            text += (f'<p><b>{key}:</b> {value}</p>')
        return text

    @staticmethod
    def format_related(related):
        dictionary = {relation: ', '.join([item['name'] for item in related[relation]]) for relation in related}
        text = str()
        for key, value in dictionary.items():
            text += (f'<p><b>{key}:</b> {value}</p>')
        label = QLabel(text)
        label.setFont(QFont('Calibri', 14))
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(label)
        return scroll


class ViewManga(QDialog):
    def __init__(self, mal_id, image_url, title, synonyms, type_, volumes, chapters, synopsis, published, status,
            score, authors, genres, related):
        super(ViewManga, self).__init__()
        self.setWindowTitle(title)
        title_label = QLabel(title)
        title_label.setFont(QFont('Calibri', 18))
        title_label.setStyleSheet(
            'border-style: none none solid none; border-width: 1px; border-color: purple'
        )

        image = QPixmap()
        image.loadFromData(requests.get(image_url).content)
        image_label = QLabel()
        image_label.setPixmap(image)
        image_label.setFixedSize(image.size())

        synopsis_label = QLabel(synopsis)
        synopsis_label.setWordWrap(True)
        synopsis_label.setFont(QFont('Calibri', 12))
        synopsis_label.setStyleSheet(
            'border-style: solid none none none; border-width: 0.5px; border-color: purple;'
        )

        info_label = QLabel(self.format_info(mal_id, synonyms, type_, volumes, chapters, status, published,
            authors, score, genres))
        info_label.setFont(QFont('Calibri', 14))
        related_scroll = self.format_related(related)

        hbox = QHBoxLayout()
        hbox.addWidget(image_label)
        hbox.setSpacing(2)
        hbox.addWidget(info_label)

        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addLayout(hbox)
        layout.addWidget(related_scroll)
        layout.addWidget(synopsis_label)

        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))

    @staticmethod
    def format_info(mal_id, synonyms, type_, volumes, chapters, status, published,
            authors, score, genres):
        dictionary = {
            'ID:': str(mal_id),
            'Synonyms:': ', '.join(synonyms),
            'Type:': type_,
            'Genres': ', '.join(genre['name'] for genre in genres),
            'Volumes:': str(volumes),
            'Chapters:': str(chapters),
            'Status:': status,
            'Published:': published['string'],
            'Studios:': ', '.join([author['name'] for author in authors]),
            'Score:': str(score)
        }
        text = str()
        for key, value in dictionary.items():
            text += (f'<p><b>{key}:</b> {value}</p>')
        return text

    @staticmethod
    def format_related(related):
        dictionary = {relation: ', '.join([item['name'] for item in related[relation]]) for relation in related}
        text = str()
        for key, value in dictionary.items():
            text += (f'<p><b>{key}:</b> {value}</p>')
        label = QLabel(text)
        label.setFont(QFont('Calibri', 14))
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(label)
        return scroll

