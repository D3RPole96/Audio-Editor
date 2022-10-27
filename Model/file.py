from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent


class File:
    def __init__(self, file):
        self.content = file
        volume = 0

    def reverse(self):
        pass

    def split(self, time_point):
        pass

    def glue_to(self, another_file):
        pass

    def change_speed(self, new_speed):
        pass
