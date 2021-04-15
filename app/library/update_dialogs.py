from PyQt5.QtWidgets import (QDialog, QDialogButtonBox, QFormLayout, QGroupBox, QLabel, QVBoxLayout,
    QHBoxLayout, QPushButton, QSpinBox, QComboBox, QMessageBox)
from PyQt5.QtGui import QFont


class ProgressBox(QComboBox):
    def __init__(self, progress, anime=True):
        super(ProgressBox, self).__init__()
        self.setFont(QFont('Calibri', 14))
        if anime:
            self.addItems(['Planning', 'Watching', 'Completed', 'Dropped'])
        else:
            self.addItems(['Planning', 'Reading', 'Completed', 'Dropped'])
        self.setCurrentText(progress)

    def progress(self):
        return self.currentText()

class SpinBox(QSpinBox):
    def __init__(self, value, range_):
        super(SpinBox, self).__init__()
        self.setFont(QFont('Calibri', 14))
        if range_:
            self.setSuffix(f'/{range_}')
            self.setRange(0, int(range_))
        else:
            self.setSuffix(f'/?')
            self.setRange(0, 10000)
        self.setValue(value)

class DeleteMessage(QDialog):
    def __init__(self, category):
        super(DeleteMessage, self).__init__()
        self.setWindowTitle(f'Delete {category}')
        self.setFont(QFont('Calibri', 12))
        dialog_buttons = QDialogButtonBox()
        dialog_buttons.addButton(QDialogButtonBox.Ok)
        dialog_buttons.addButton(QDialogButtonBox.Cancel)
        dialog_buttons.accepted.connect(self.accept)
        dialog_buttons.rejected.connect(self.reject)
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f'Are you sure you want to delete this {category}?'))
        layout.addWidget(dialog_buttons)
        self.setLayout(layout)

class UpdateAnime(QGroupBox):
    def __init__(self, connection, id_, progress, episodes, rating):
        super(UpdateAnime, self).__init__()
        self.connection = connection
        self.id = id_
        self.setTitle('Update Anime')
        self.progress_box = ProgressBox(progress)
        self.episodes_box = SpinBox(*episodes)
        self.rating_box = SpinBox(*rating)
        form = QFormLayout()
        form.addRow(QLabel('Progress:'), self.progress_box)
        form.addRow(QLabel('Episodes:'), self.episodes_box)
        form.addRow(QLabel('Rating:'), self.rating_box)

        self.update_button = QPushButton('Update')
        self.update_button.clicked.connect(self.update_anime)
        self.delete_button = QPushButton('Delete')
        self.delete_button.clicked.connect(self.delete_anime)
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.update_button)
        hbox1.addWidget(self.delete_button)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addLayout(hbox1)
        self.setLayout(layout)

    def update_anime(self):
        progress = self.progress_box.progress()
        episodes = self.episodes_box.value()
        rating = self.rating_box.value()
        self.connection.update_anime((progress, episodes, rating, self.id))

    def delete_anime(self):
        msg = DeleteMessage('anime')
        x = msg.exec_()
        if x:
            self.connection.delete_anime(self.id)
            self.update_button.setEnabled(False)
            self.delete_button.setEnabled(False)


class UpdateManga(QGroupBox):
    def __init__(self, connection, id_, progress, volumes, chapters, rating):
        super(UpdateManga, self).__init__()
        self.connection = connection
        self.id = id_
        self.setTitle('Update Anime')
        self.progress_box = ProgressBox(progress)
        self.volumes_box = SpinBox(*volumes)
        self.chapters_box = SpinBox(*chapters)
        self.rating_box = SpinBox(*rating)
        form = QFormLayout()
        form.addRow(QLabel('Progress:'), self.progress_box)
        form.addRow(QLabel('Volumes:'), self.volumes_box)
        form.addRow(QLabel('Chapters:'), self.chapters_box)
        form.addRow(QLabel('Rating:'), self.rating_box)

        self.update_button = QPushButton('Update')
        self.update_button.clicked.connect(self.update_manga)
        self.delete_button = QPushButton('Delete')
        self.delete_button.clicked.connect(self.delete_manga)
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.update_button)
        hbox1.addWidget(self.delete_button)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addLayout(hbox1)
        self.setLayout(layout)

    def update_manga(self):
        progress = self.progress_box.progress()
        volumes = self.volumes_box.value()
        chapters = self.chapters_box.value()
        rating = self.rating_box.value()
        self.connection.update_manga((progress, volumes, chapters, rating, self.id))

    def delete_manga(self):
        msg = DeleteMessage('manga')
        x = msg.exec_()
        if x:
            self.connection.delete_manga(self.id)
            self.update_button.setEnabled(False)
            self.delete_button.setEnabled(False)



