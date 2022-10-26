<<<<<<< HEAD
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent


class File:
    def __init__(self, path):
        self.path = path
        url = QUrl.fromLocalFile(path)
        self.content = QMediaContent(url)

    content = ''
=======
class File:
    def __init__(self):
        pass

>>>>>>> 37f97a83c15666840205e0cc9969a5dce433ba5a
    path = ""
    volume = 0

    def reverse(self):
        pass

    def split(self, time_point):
        pass

    def glue_to(self, another_file):
        pass

    def change_speed(self, new_speed):
        pass