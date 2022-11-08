from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import  QPushButton, QHBoxLayout, QWidget, QVBoxLayout, QTableWidget, QMainWindow, QWidgetAction, QFileDialog
#from PyQt6.QtWidgets import
import threading

#from GUI.menubar import create_menubar
from GUI.jump_slider import QJumpSlider


class MainWindow(QMainWindow):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.setWindowTitle(session.project.name + " - AudioEditor")
        self.setFixedSize(QSize(1280, 640))

        self.create_menubar()

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

        self.check_progress_bar()


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
        self.play_button.clicked.connect(lambda: self.session.player_play())
        self.pause_button = QPushButton('Pause')
        self.pause_button.setFixedSize(100, 100)
        self.pause_button.clicked.connect(lambda: self.session.player_pause())
        self.stop_button = QPushButton('Stop')
        self.stop_button.setFixedSize(100, 100)
        self.stop_button.clicked.connect(lambda: self.session.player_stop())

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

        self.global_volume_slider.valueChanged.connect(self.session.player_set_volume)

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

        self.progress_slider.set_run_on_click_function(self.session.player_set_position)

        self.progress_slider_layout = QHBoxLayout()
        self.progress_slider_layout.addWidget(self.progress_slider)

        self.lower_bottom_layout.addLayout(self.progress_slider_layout)

        self.progress_slider_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def check_progress_bar(self):
        threading.Timer(0.001, self.check_progress_bar).start()
        self.progress_slider.setValue(self.session.project.player.get_progress() * self.progress_slider.maximum())

    def create_menubar(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("Файл")

        new_file = QWidgetAction(self)
        new_file.setText("Создать")
        file_menu.addAction(new_file)
        open_file = QWidgetAction(self)
        open_file.setText("Открыть")
        open_file.triggered.connect(self.import_file)
        file_menu.addAction(open_file)
        save_file = QWidgetAction(self)
        save_file.setText("Сохранить")
        file_menu.addAction(save_file)
        save_as_file = QWidgetAction(self)
        save_as_file.setText("Сохранить как")
        file_menu.addAction(save_as_file)
        import_file = QWidgetAction(self)
        file_menu.addSeparator()
        import_file.setText("Импорт медиа")
        file_menu.addAction(import_file)
        export_file = QWidgetAction(self)
        export_file.setText("Экспорт медиа")
        file_menu.addAction(export_file)

        edit_menu = menu_bar.addMenu("Правка")

        undo = QWidgetAction(self)
        undo.setText("Отменить")
        edit_menu.addAction(undo)
        redo = QWidgetAction(self)
        redo.setText("Повторить")
        edit_menu.addAction(redo)


    def import_file(self):
        path = QFileDialog.getSaveFileName(self, caption="Сохранит как...............")
