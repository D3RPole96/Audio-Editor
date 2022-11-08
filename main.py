import sys

from PyQt5.QtWidgets import QApplication

from GUI.mail_window import MainWindow
from Model.session import Session

if __name__ == "__main__":
    app = QApplication(sys.argv)

    session = Session()
    session.project.import_demo_file()

    window = MainWindow(session)
    window.show()

    app.exec()
