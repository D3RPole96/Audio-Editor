import os

from Model import ffmeg_editor
from Model.fragment import Fragment
from Model.commands.icommand import Command
from copy import deepcopy


class Reverse(Command):
    def __init__(self, parent, fragment_index):
        super().__init__(parent, fragment_index)

    def operate(self, *args):
        fragment_path = self.old_file.content
        path_after = str(fragment_path[:-4] + '-r' + fragment_path[-4:])
        path_before = str(fragment_path[:-6] + fragment_path[-4:])

        if path_after in [x.content for x in self.parent.project_files]:
            return Fragment(path_after)
        elif path_before in [x.content for x in self.parent.project_files]:
            return Fragment(path_before)
        else:
            ffmeg_editor.reverse(fragment_path, path_after)
            fragment = Fragment(path_after)
            self.parent.project_files.append(fragment)
            return fragment
