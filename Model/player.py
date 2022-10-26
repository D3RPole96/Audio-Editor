from PyQt5.QtMultimedia import QMediaPlayer



class Player:
    def __init__(self):
        self.player = QMediaPlayer()

    def set_content(self, content):
        self.player.setMedia(content)

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()
