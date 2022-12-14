import os

from Model import ffmeg_editor
from Model.fragment import Fragment
from Model.commands.icommand import Command
from copy import deepcopy


class Reverse(Command):
    def __init__(self, parent, fragment_index):
        super().__init__()
        self.fragment_index = fragment_index
        self.parent = parent

    def do(self):
        reverse(self.parent, self.fragment_index)

    def undo(self):
        reverse(self.parent, self.fragment_index)


def reverse(parent, fragment_index):
    fragment = parent.fragments[fragment_index]

    path = deepcopy(fragment.content)
    if not fragment.is_reversed:
        new_path = path[:-4] + '-r' + path[-4:]
        ffmeg_editor.reverse(path, new_path)
    else:
        new_path = path[::-1].replace('-r'[::-1], '', 1)[::-1]
        os.remove(path)

    new_fragment = Fragment(new_path)
    new_fragment.is_reversed = not fragment.is_reversed
    parent.fragments[fragment_index] = new_fragment
    # parent.temp_files.append(new_path)
