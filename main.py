import sys

import ffmpeg
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QHBoxLayout, QWidget, QVBoxLayout, QSlider, \
    QTableWidget, QStyleOptionSlider, QStyle
from PyQt5.uic.properties import QtWidgets, QtCore, QtGui

from Screens.menubar import create_menubar
from Model.project import Project


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.project = Project()
        self.project.import_demo_file()

        self.setWindowTitle("Audio Editor")
        self.setFixedSize(QSize(1280, 640))
        self.general_layout = QVBoxLayout()
        self.top_layout = QHBoxLayout()
        self.bottom_layout = QVBoxLayout()

        self.general_layout.addLayout(self.top_layout)
        self.general_layout.addLayout(self.bottom_layout)

        self.set_top_layout()
        self.set_bottom_layout()

        container = QWidget()
        container.setLayout(self.general_layout)

        self.setCentralWidget(container)

    def set_top_layout(self):
        self.left_top_layout = QVBoxLayout()
        self.right_top_layout = QHBoxLayout()
        self._set_fragments_table()

        self.top_layout.addLayout(self.left_top_layout)
        self.top_layout.addLayout(self.right_top_layout)

    def _set_fragments_table(self):
        self.fragments_table = QTableWidget()
        self.fragments_table.setFixedSize(250, 300)

        self.fragments_table_layout = QHBoxLayout()
        self.fragments_table_layout.addWidget(self.fragments_table)

        self.left_top_layout.addLayout(self.fragments_table_layout)

        self.fragments_table_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    def set_bottom_layout(self):
        self.upper_bottom_layout = QHBoxLayout()
        self.lower_bottom_layout = QHBoxLayout()
        self._set_main_buttons()
        self._set_global_volume_slider()
        self._set_progress_slider()
        self.upper_bottom_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.bottom_layout.addLayout(self.upper_bottom_layout)
        self.bottom_layout.addLayout(self.lower_bottom_layout)

    def _set_main_buttons(self):
        self.play_button = QPushButton('Play')
        self.play_button.setFixedSize(100, 100)
        self.play_button.clicked.connect(lambda: self.project.player.play())
        self.pause_button = QPushButton('Pause')
        self.pause_button.setFixedSize(100, 100)
        self.pause_button.clicked.connect(lambda: self.project.player.pause())
        self.stop_button = QPushButton('Stop')
        self.stop_button.setFixedSize(100, 100)
        self.stop_button.clicked.connect(lambda: self.project.player.stop())

        self.main_buttons_layout = QHBoxLayout()
        self.main_buttons_layout.addWidget(self.pause_button)
        self.main_buttons_layout.addWidget(self.play_button)
        self.main_buttons_layout.addWidget(self.stop_button)

        self.upper_bottom_layout.addLayout(self.main_buttons_layout)

        self.main_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignTop
                                              | Qt.AlignmentFlag.AlignLeft)

    def _set_global_volume_slider(self):
        self.global_volume_slider = QJumpSlider(Qt.Horizontal)
        self.global_volume_slider.setFixedSize(250, 25)

        self.global_volume_slider.setMinimum(0)
        self.global_volume_slider.setMaximum(100)
        self.global_volume_slider.setSingleStep(1)
        self.global_volume_slider.setValue(100)

        self.global_volume_slider.valueChanged.connect(self.project.player.set_volume)

        self.global_volume_slider_layout = QHBoxLayout()
        self.global_volume_slider_layout.addWidget(self.global_volume_slider)

        self.upper_bottom_layout.addLayout(self.global_volume_slider_layout)

        self.global_volume_slider_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

    def _set_progress_slider(self):
        self.progress_slider = QJumpSlider(Qt.Horizontal)
        self.progress_slider.setFixedSize(1100, 200)

        self.progress_slider.setMinimum(0)
        self.progress_slider.setMaximum(1000)

        self.progress_slider.setSingleStep(1)
        self.progress_slider.setValue(0)

        self.progress_slider_layout = QHBoxLayout()
        self.progress_slider_layout.addWidget(self.progress_slider)

        self.lower_bottom_layout.addLayout(self.progress_slider_layout)

        self.progress_slider_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)


class QJumpSlider(QSlider):
    def __init__(self, parent=None):
        super(QJumpSlider, self).__init__(parent)

    def mousePressEvent(self, event):
        self.setValue(QStyle.sliderValueFromPosition(self.minimum(), self.maximum(),
                                                     event.x() if self.orientation() == Qt.Horizontal else -event.y(),
                                                     self.width() if self.orientation() == Qt.Horizontal
                                                     else self.height()))

    def mouseMoveEvent(self, event):
        self.setValue(QStyle.sliderValueFromPosition(self.minimum(), self.maximum(),
                                                     event.x() if self.orientation() == Qt.Horizontal else -event.y(),
                                                     self.width() if self.orientation() == Qt.Horizontal
                                                     else self.height()))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
