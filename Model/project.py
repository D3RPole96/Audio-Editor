import os

from PyQt5.QtCore import QUrl

from Model.commands.change_speed import ChangeSpeed
from Model.commands.concat import Concat
from Model.commands.reverse import Reverse
from Model.commands.delete import Delete
from Model.player import Player
from Model.fragment import Fragment
from PyQt5 import QtCore
from Model import ffmeg_editor


class Project:
    def __init__(self, name):
        self.path = ""
        self.name = name

        self.project_files = []
        self.active_fragments = []

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
        cmd = Delete(self, fragment_index)
        cmd.do()
        self.done_stack.append(cmd)

    def change_speed(self, fragment_index, speed_ratio):
        cmd = ChangeSpeed(self, fragment_index, speed_ratio)
        cmd.do()
        self.done_stack.append(cmd)

    def add_content(self, fragment_index):
        self.player.add_content(self.active_fragments[fragment_index].content)

    def split(self, fragment, time_point):
        pass

    def concat(self, fragment1, fragment2):
        cmd = Concat(self, fragment1, fragment2)
        cmd.do()
        self.done_stack.append(cmd)

    def import_file(self, path):
        file = Fragment(path)
        self.project_files.append(file)
        self.active_fragments.append(file)


    def import_demo_file(self):
        pass

    def export_as_project(self, path):
        pass

    def export_as_file(self, path):
        pass

    def undo(self):
        if len(self.done_stack) == 0:
            return
        cmd = self.done_stack.pop()
        cmd.undo()
        self.undone_stack.append(cmd)

    def redo(self):
        if len(self.undone_stack) == 0:
            return
        cmd = self.undone_stack.pop()
        cmd.do()
        self.done_stack.append(cmd)

    @staticmethod
    def unpack(pack_array, name, path):
        proj = Project(name)
        proj.path = path
        proj.have_unsaved_changes = False
        for line in pack_array:
            arguments = line.split()
            proj.active_fragments.append(Fragment(arguments[0], bool(arguments[1]), float(arguments[2])))
        return proj

    def pack(self):
        answer = []
        for fragment in self.active_fragments:
            answer.append(f'{fragment.content} {fragment.is_reversed} {fragment.speed}')
        return answer
