from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent


class Fragment:
    last_id = 0

    def __init__(self, content, is_reversed=False, speed=1):
        self.length = 0
        self.id = Fragment.last_id
        Fragment.last_id += 1
        self.content = content
        volume = 0

        self.speed = speed

    def __eq__(self, other):
        return self.id == other.id
