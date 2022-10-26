<<<<<<< HEAD
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
=======
class Player:
    def __init__(self):
        pass
>>>>>>> 37f97a83c15666840205e0cc9969a5dce433ba5a
