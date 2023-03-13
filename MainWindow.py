from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from pathlib import Path
from pygame import mixer
import sys, os

def playMusic(path:str):
    mixer.music.load(path)
    mixer.music.play()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.path = ""
        mixer.init()

        self.setWindowTitle("Musix Player")

        layout = QGridLayout()
        self.setLayout(layout)

        self.dir_input = QTextEdit()
        self.dir_input.setFixedHeight(30)
        self.dir_browse = QPushButton("Browse")
        self.dir_browse.clicked.connect(self.onBrowse)
        
        self.label = QLabel("THIS IS A MUSIC PLAYER")
        button = QPushButton("Push here")
        button.clicked.connect(self.changeText)

        self.songList = QListView()
        self.model = QStandardItemModel()
        self.songList.setModel(self.model)
        self.songList.clicked[QModelIndex].connect(self.onSongSelected)

        layout.addWidget(self.dir_input, 0, 1)
        layout.addWidget(self.dir_browse, 0, 2)

        layout.addWidget(self.songList, 2,0,1,2,Qt.AlignmentFlag.AlignCenter)

        self.show()


    def changeText(self, clicked):
        self.label.setText("Clicked")

    def onSongSelected(self, idx):
        song = self.model.itemFromIndex(idx)
        playMusic(self.path + "/" + song.text())

    def onBrowse(self):
        filename = QFileDialog.getExistingDirectory(self, "Select a Directory", "")

        if filename:
            self.path = str(Path(filename))
            self.dir_input.setText(self.path)

            songs = os.listdir(self.path)
            for song in songs:
                if any(x in song for x in [".flac", ".mp3"]):
                    self.model.appendRow(QStandardItem(song))