import os
from copy import deepcopy

from Model import ffmeg_editor
from Model.fragment import Fragment
from Model.commands.icommand import Command
import re


class ChangeSpeed(Command):
    def __init__(self, parent, fragment_index, speed_ratio):
        self.speed_ratio = speed_ratio
        super().__init__(parent, fragment_index)

    def operate(self):
        ratio = self.speed_ratio
        fragment_path = self.old_file.content
        suffix = get_last_suffix(fragment_path)
        print(suffix)
        if suffix == '' or suffix[:2] != '-s':
            new_path = fragment_path[:-4] + '-s' + str(ratio) + fragment_path[-4:]
            ffmeg_editor.change_speed(fragment_path, new_path, ratio)
            return Fragment(new_path)

        previous_ratio = float(suffix[2:])
        previous_path = fragment_path[:(-4-len(suffix))] + fragment_path[-4:]
        new_ratio = ratio * previous_ratio
        new_path = previous_path[:-4] + '-s' + str(new_ratio) + previous_path[-4:]
        ffmeg_editor.change_speed(previous_path, new_path, new_ratio)
        return Fragment(new_path)


def get_last_suffix(line):
    answer = ''
    for i in range(len(line) - 5, -1, -1):
        answer += line[i]
        if line[i] == '-':
            return answer[::-1]
    return ''


def change_speed(parent, fragment_index, speed_ratio):
    fragment = parent.active_fragments[fragment_index]

    path = deepcopy(fragment.content)
    if fragment.speed == 1:
        if speed_ratio != 1:
            new_path = path[:-4] + '-s' + str(speed_ratio) + path[-4:]
            ffmeg_editor.change_speed(path, new_path, speed_ratio)
        else:
            new_path = path
    else:
        if speed_ratio * fragment.speed != 1:
            original_path = re.sub(r'\d+\.\d+s-', '', path[::-1], 1)[::-1]
            new_path = re.sub(r'\d+\.\d+s-', f'-s{speed_ratio * fragment.speed}'[::-1], path[::-1], 1)[::-1]
            ffmeg_editor.change_speed(original_path, new_path, speed_ratio * fragment.speed)
            os.remove(path)
        else:
            new_path = re.sub(r'\d+\.\d+s-', '', path[::-1], 1)[::-1]
            os.remove(path)

    new_fragment = Fragment(new_path)
    new_fragment.speed = fragment.speed * speed_ratio
    parent.active_fragments[fragment_index] = new_fragment
