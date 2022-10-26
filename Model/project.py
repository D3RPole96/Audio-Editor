from Model.player import Player


class Project:
    def __init__(self):
        pass

    files = []
    master_volume = 0
    player = Player()
    selected = 0

    def reverse(self, fragment):
        pass

    def delete(self, fragment):
        pass

    def change_speed(self, fragment, new_speed):
        pass

    def split(self, fragment, time_point):
        pass

    def glue_to_next(self, fragment):
        pass

    def import_file(self, path):
        pass

    def export_as_project(self):
        pass

    def export_as_file(self):
        pass
