from Model.player import Player
from Model.file import File
from PyQt5 import QtCore

class Project:
    def __init__(self):
        self.files = []
        self.master_volume = 0
        self.player = Player()
        self.selected = 0

    def reverse(self, fragment):
        pass

    def delete(self, fragment):
        pass

    def change_speed(self, fragment, new_speed):
        pass

    def split(self, fragment, time_point):
        pass

    def glue_to_next(self, fragment):
        pass

    def import_file(self, path):
        pass

    def import_demo_file(self):
        file = File(QtCore.QDir.current().absoluteFilePath('met.wav'))
        self.files.append(file)
        self.player.set_content(file.content)

    def export_as_project(self):
        pass

    def export_as_file(self):
        pass
