from Model.commands.icommand import Command


class Split(Command):
    def __init__(self, parent, fragment_index, point):
        self.point = point
        super().__init__(parent, fragment_index)

    def operate(self):
        pass