import os
from copy import deepcopy

from Model import ffmeg_editor
from Model.fragment import Fragment
from Model.commands.icommand import Command
import re


class ChangeSpeed(Command):
    def __init__(self, parent, fragment_index, speed_ratio):
        super().__init__()
        self.parent = parent
        self.fragment_index = fragment_index
        self.speed_ratio = speed_ratio

    def do(self):
        change_speed(self.parent, self.fragment_index, self.speed_ratio)

    def undo(self):
        change_speed(self.parent, self.fragment_index, 1 / self.speed_ratio)


def change_speed(parent, fragment_index, speed_ratio):
    fragment = parent.fragments[fragment_index]

    path = deepcopy(fragment.content)
    if fragment.speed == 1:
        if speed_ratio != 1:
            new_path = path[:-4] + '-s' + str(speed_ratio) + path[-4:]
        else:
            new_path = path
    else:
        if speed_ratio * fragment.speed != 1:
            new_path = re.sub(r'\d+\.\d+s-', f'-s{speed_ratio * fragment.speed}'[::-1], path[::-1], 1)[::-1]
        else:
            new_path = re.sub(r'\d+\.\d+s-', '', path[::-1], 1)[::-1]

    ffmeg_editor.change_speed(path, new_path, speed_ratio)
    os.remove(path)

    new_fragment = Fragment(new_path)
    new_fragment.speed = fragment.speed * speed_ratio
    parent.fragments[fragment_index] = new_fragment
    # parent.temp_files.append(new_path)
