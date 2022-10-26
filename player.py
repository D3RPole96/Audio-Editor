from PyQt5 import QtCore, QtWidgets, QtMultimedia


class Player:
    def __init__(self, path):
        filename = 'met.mp3'
        fullpath = QtCore.QDir.current().absoluteFilePath(filename)
        url = QtCore.QUrl.fromLocalFile(fullpath)
        content = QtMultimedia.QMediaContent(url)
        player = QtMultimedia.QMediaPlayer()
        player.setMedia(content)
        player.play()

    def play(self):
        pass

    def pause(self):
        pass

    def stop(self):
        pass

    def change_track(self, path):
        path