from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent


class Player:
    player = QMediaPlayer()

    def __init__(self):
        pass

    def set_content(self, content):
        Player.player.setMedia(QMediaContent(QUrl.fromLocalFile(content)))

    def play(self):
        Player.player.play()

    def pause(self):
        Player.player.pause()

    def stop(self):
        Player.player.stop()

    def set_volume(self, volume_level):
        Player.player.setVolume(volume_level)
