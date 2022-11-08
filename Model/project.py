from Model.player import Player
from Model.fragment import Fragment
from PyQt5 import QtCore


class Project:
    def __init__(self, name):
        self.name = name
        self.fragments = []
        self.master_volume = 0
        self.player = Player()
        self.selected = 0
        self.done_stack = []
        self.undone_stack = []

    def reverse(self, fragment):
        pass

    def delete(self, fragment):
        pass

    def change_speed(self, fragment, new_speed):
        pass

    def split(self, fragment, time_point):
        pass

    def glue(self, fragment1, fragment2):
        pass

    def import_file(self, path):
        pass

    def import_demo_file(self):
        file = Fragment(QtCore.QDir.current().absoluteFilePath('DemoFiles/met.wav'))
        self.fragments.append(file)
        self.player.add_content(file.content)
        # file = Fragment(QtCore.QDir.current().absoluteFilePath('met2.wav'))
        # self.fragments.append(file)
        # self.player.add_content(file.content)

    def export_as_project(self, path):
        pass

    def export_as_file(self, path):
        pass
