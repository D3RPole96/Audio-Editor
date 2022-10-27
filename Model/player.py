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

    def set_position(self, value):
        Player.player.setPosition(value)

    def get_duration(self):
        return Player.player.duration()

    def get_progress(self):
        return Player.player.position() / Player.player.duration() if Player.player.duration() != 0 else 0
