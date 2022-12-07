from PyQt5.QtWidgets import QFileDialog

from Model.project import Project


class Session:
    def __init__(self):
        self.project = Project("untitled")

    def menu_file_new(self, name):
        pass

    def menu_file_open(self, path):
        pass

    def menu_file_save(self):
        pass

    def menu_file_save_as(self, path):
        pass

    def menu_file_import(self, path):
        pass

    def menu_file_export(self, path):
        pass

    def menu_edit_undo(self):
        pass

    def menu_edit_redo(self):
        pass

    def menu_help_about(self):
        pass

    def player_play(self):
        self.project.player.play()

    def player_pause(self):
        self.project.player.pause()

    def player_stop(self):
        self.project.player.stop()

    def player_set_volume(self, volume):
        self.project.player.set_volume(volume)

    def player_set_position(self, position):
        self.project.player.set_position(position)
