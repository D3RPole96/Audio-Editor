from Model.player import Player
<<<<<<< HEAD
from Model.file import File
=======

>>>>>>> 37f97a83c15666840205e0cc9969a5dce433ba5a

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

<<<<<<< HEAD
    def import_demo_file(self):
        file = File('met.wav')
        self.files.append(file)
        self.player.set_content(file.content)

=======
>>>>>>> 37f97a83c15666840205e0cc9969a5dce433ba5a
    def export_as_project(self):
        pass

    def export_as_file(self):
        pass
