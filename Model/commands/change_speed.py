from Model import ffmeg_editor
from Model.fragment import Fragment
from Model.commands.icommand import Command


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
    fragment_index = fragment_index
    speed_ratio = speed_ratio
    fragment = parent.fragments[fragment_index]
    path = fragment.content
    new_path = path[:-4] + '-s' + str(speed_ratio) + path[-4:]
    ffmeg_editor.change_speed(path, new_path, speed_ratio)
    new_fragment = Fragment(new_path)
    parent.fragments[fragment_index] = new_fragment
    # parent.temp_files.append(new_path)
