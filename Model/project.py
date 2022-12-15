import os

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

    def delete(self, fragment_index):
        if self.fragments[fragment_index].is_reversed or self.fragments[fragment_index].speed != 1:
            os.remove(self.fragments[fragment_index].content)
        del self.fragments[fragment_index]

    def change_speed(self, fragment_index, speed_ratio):
        cmd = ChangeSpeed(self, fragment_index, speed_ratio)
        cmd.do()
        self.done_stack.append(cmd)

    def add_content(self, fragment_index):
        self.player.add_content(self.fragments[fragment_index].content)

    def split(self, fragment, time_point):
        pass

    def glue(self, fragment1, fragment2):
        pass

    def import_file(self, path):
        file = Fragment(path)
        self.fragments.append(file)
        # self.player.add_content(file.content)

    def import_demo_file(self):
        pass

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
            arguments = line.split()
            proj.fragments.append(Fragment(arguments[0], bool(arguments[1]), float(arguments[2])))
        return proj

    def pack(self):
        answer = []
        for fragment in self.fragments:
            answer.append(f'{fragment.content} {fragment.is_reversed} {fragment.speed}')
        return answer
