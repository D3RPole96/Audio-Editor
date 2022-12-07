from PyQt5.QtCore import QUrl

from Model.commands.change_speed import ChangeSpeed
from Model.commands.reverse import Reverse
from Model.player import Player
from Model.fragment import Fragment
from PyQt5 import QtCore
from Model import ffmeg_editor


class Project:
    def __init__(self, name):
        self.path = ""
        self.name = name
        self.fragments = []
        self.master_volume = 0
        self.player = Player()
        self.done_stack = []
        self.undone_stack = []
        self.have_unsaved_changes = True


    def reverse(self, fragment_index):
        cmd = Reverse(self, fragment_index)
        cmd.do()
        self.done_stack.append(cmd)

    def delete(self, fragment):
        pass

    def change_speed(self, fragment_index, speed_ratio):
        cmd = ChangeSpeed(self, fragment_index, speed_ratio)
        cmd.do()
        self.done_stack.append(cmd)

    def split(self, fragment, time_point):
        pass

    def glue(self, fragment1, fragment2):
        pass

    def import_file(self, path):
        file = Fragment(path)
        self.fragments.append(file)
        # self.player.add_content(file.content)

    def import_demo_file(self):
        path = Fragment(QtCore.QDir.current().absoluteFilePath('DemoFiles/met.wav'))
        self.fragments.append(path)
        self.player.add_content(path.content)
        path = Fragment(QtCore.QDir.current().absoluteFilePath('DemoFiles/met2.mp3'))
        self.fragments.append(path)
        self.player.add_content(path.content)

    def export_as_project(self, path):
        pass

    def export_as_file(self, path):
        pass

    def undo(self):
        cmd = self.done_stack.pop()
        cmd.undo()
        self.undone_stack.append(cmd)

    def redo(self):
        cmd = self.undone_stack.pop()
        cmd.do()

    @staticmethod
    def unpack(pack_array, name, path):
        proj = Project(name)
        proj.path = path
        proj.have_unsaved_changes = False
        for line in pack_array:
            proj.fragments.append(Fragment(line[1:]))
        return proj


    def pack(self):
        answer = []
        for fragment in self.fragments:
            answer.append(fragment.content)
        return answer

