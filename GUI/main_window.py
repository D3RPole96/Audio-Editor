from PyQt5.QtCore import QSize, Qt, QUrl
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QWidget, QVBoxLayout, QTableWidget, QMainWindow, QWidgetAction, \
    QFileDialog, QTableWidgetItem, QInputDialog, QLabel, QMessageBox, QDialog, QLineEdit, QDialogButtonBox, QFormLayout
import threading

from GUI.jump_slider import QJumpSlider
from Model.project import Project




class MainWindow(QMainWindow):
    def __init__(self, session):
        super().__init__()
        self.session = session

        self.audio_name = QLabel()
        self.audio_name.setText('-')
        self.audio_name.setFont(QFont('Arial', 24))
        self.duration_text = QLabel()
        self.duration_text.setText('0:00 / 0:00')
        self.duration_text.setFont(QFont('Arial', 24))

        self.refresh()
        self.create_menubar()

    def refresh(self):
        self.setWindowTitle(self.session.project.name + " - AudioEditor")
        self.setFixedSize(QSize(1280, 640))

        self.general_layout = QVBoxLayout()
        self.top_layout = QHBoxLayout()
        self.bottom_layout = QVBoxLayout()

        self.general_layout.addLayout(self.top_layout)
        self.general_layout.addLayout(self.bottom_layout)

        self.set_top_layout()
        self.set_bottom_layout()

        self.container = QWidget()
        self.container.setLayout(self.general_layout)

        self.setCentralWidget(self.container)
        self.update_progress()

    def set_top_layout(self):
        self.left_top_layout = QVBoxLayout()
        self.right_top_layout = QHBoxLayout()
        self._set_fragments_table()

        self.top_layout.addLayout(self.left_top_layout)
        self.top_layout.addLayout(self.right_top_layout)

    def _set_fragments_table(self):
        self.table = QTableWidget()
        self.table.setFixedSize(550, 300)
        rows_count = len(self.session.project.active_fragments)
        self.table.setColumnCount(3)  # Set three columns
        self.table.setRowCount(rows_count)  # and one row
        self.table.setColumnWidth(2, 220)

        self.table.setHorizontalHeaderLabels(["Название", "Длина", "Действия"])
        for i in range(rows_count):
            self.add_table_row(i)

        self.fragments_table_layout = QHBoxLayout()
        self.fragments_table_layout.addWidget(self.table)

        self.left_top_layout.addLayout(self.fragments_table_layout)

        self.fragments_table_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    def add_table_row(self, i):
        self.table.setRowHeight(i, 50)
        name = QUrl(self.session.project.active_fragments[i].content).fileName()
        self.table.setItem(i, 0, QTableWidgetItem(name))
        length = self.session.project.active_fragments[i].duration
        self.table.setItem(i, 1, QTableWidgetItem(length))
        tools_panel = QHBoxLayout()

        delete_button = QPushButton('D')
        delete_button.clicked.connect(lambda: self.editor_delete_fragment(i))
        tools_panel.addWidget(delete_button)
        reverse_button = QPushButton('R')
        reverse_button.clicked.connect(lambda: self.editor_reverse_fragment(i))
        tools_panel.addWidget(reverse_button)
        speed_button = QPushButton('>>')
        speed_button.clicked.connect(lambda: self.editor_change_speed(i))
        tools_panel.addWidget(speed_button)
        glue_button = QPushButton('G')
        glue_button.clicked.connect(lambda: self.editor_concat(i))
        tools_panel.addWidget(glue_button)
        split_button = QPushButton('T')
        split_button.clicked.connect(lambda: self.editor_trim(i))
        tools_panel.addWidget(split_button)
        clone_button = QPushButton('C')
        clone_button.clicked.connect(lambda: self.editor_clone(i))
        tools_panel.addWidget(clone_button)
        up_button = QPushButton('↑')
        up_button.clicked.connect(lambda: self.editor_up(i))
        tools_panel.addWidget(up_button)
        down_button = QPushButton('↓')
        down_button.clicked.connect(lambda: self.editor_down(i))
        tools_panel.addWidget(down_button)
        play_button = QPushButton('P')
        play_button.clicked.connect(lambda: self.editor_add_content(i))
        tools_panel.addWidget(play_button)

        tools_panel_widget = QWidget()
        tools_panel_widget.setLayout(tools_panel)
        self.table.setCellWidget(i, 2, tools_panel_widget)

    def set_bottom_layout(self):
        self.upper_bottom_layout = QHBoxLayout()
        self.lower_bottom_layout = QHBoxLayout()
        self._set_main_buttons()
        self.__set_main_text()
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

    def __set_main_text(self):
        self.main_text_layout = QVBoxLayout()
        self.main_text_layout.addWidget(self.audio_name)
        self.main_text_layout.addWidget(self.duration_text)

        self.empty_label = QLabel()
        self.empty_label.setFixedWidth(100)

        self.upper_bottom_layout.addWidget(self.empty_label)
        self.upper_bottom_layout.addLayout(self.main_text_layout)

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

    def update_progress(self):
        threading.Timer(0.001, self.update_progress).start()
        progress = self.session.project.player.get_progress()

        # Не убирай коммент, иначе компу смерть

        #if self.session.project.player.playing_fragment is not None:
        #    self.duration_text.setText(
        #        self.duration_text.setText(f'{get_duration_with_percent(self.session.project.player.playing_fragment, progress)}'
        #                                   f' / {get_duration(self.session.project.player.playing_fragment)}'))

        self.progress_slider.setValue(progress * self.progress_slider.maximum())

    def create_menubar(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("Файл")

        new_file = QWidgetAction(self)
        new_file.setText("Создать")
        new_file.triggered.connect(self.menu_new)
        file_menu.addAction(new_file)

        open_file = QWidgetAction(self)
        open_file.setText("Открыть")
        open_file.triggered.connect(self.menu_open_file)
        file_menu.addAction(open_file)

        save_file = QWidgetAction(self)
        save_file.setText("Сохранить")
        save_file.triggered.connect(self.menu_save_file)
        file_menu.addAction(save_file)

        save_as_file = QWidgetAction(self)
        save_as_file.setText("Сохранить как")
        save_as_file.triggered.connect(self.menu_save_as_file)
        file_menu.addAction(save_as_file)

        file_menu.addSeparator()

        import_file = QWidgetAction(self)
        import_file.setText("Импорт медиа")
        import_file.triggered.connect(self.menu_import_file)
        file_menu.addAction(import_file)

        export_file = QWidgetAction(self)
        export_file.setText("Экспорт медиа")
        export_file.triggered.connect((self.menu_export_file))
        file_menu.addAction(export_file)

        edit_menu = menu_bar.addMenu("Правка")

        undo = QWidgetAction(self)
        undo.setText("Отменить")
        undo.triggered.connect(self.menu_undo)
        edit_menu.addAction(undo)
        redo = QWidgetAction(self)
        redo.setText("Повторить")
        redo.triggered.connect(self.menu_redo)
        edit_menu.addAction(redo)

    def menu_open_file(self):
        url = QFileDialog.getOpenFileUrl(self, caption="Открыть")
        path = url[0].path()[1:]
        if path != '':
            with open(path, 'r') as f:
                lines = f.readlines()
                self.session.project = Project.unpack(lines, url[0].fileName(), path)
        self.refresh()

    def menu_save_file(self):
        if self.session.project.path == "":
            self.menu_save_as_file()
        else:
            data = self.session.project.pack()
            with open(self.session.project.path, 'w') as f:
                for line in data:
                    f.write(line)

    def menu_save_as_file(self):
        url = QFileDialog.getSaveFileUrl(self, caption="Сохранить как...", filter=".artl")
        path = url[0].path() + '.artl'
        self.session.project.path = path
        self.session.project.name = url[0].fileName()
        data = self.session.project.pack()
        with open(path[1:], 'w') as f:
            for line in data:
                f.write(line + '\n')
        self.refresh()

    def menu_import_file(self):
        path = QFileDialog.getOpenFileUrl(self, caption="Импортировать")
        s = path[0].path()[1:]
        if s != '':
            self.session.project.import_file(s)
        self.refresh()

    def menu_export_file(self):
        path = QFileDialog.getSaveFileUrl(self, caption="Сохранить как", filter=(".wav"), )[0].path() + ".wav"
        self.session.project.export_as_file(path)


    def editor_delete_fragment(self, fragment_index):
        self.session.project.delete(fragment_index)
        self.refresh()

    def editor_up(self, fragment_index):
        self.session.project.up(fragment_index)
        self.refresh()

    def editor_down(self, fragment_index):
        self.session.project.down(fragment_index)
        self.refresh()

    def editor_clone(self, fragment_index):
        self.session.project.clone(fragment_index)
        self.refresh()
    def editor_reverse_fragment(self, fragment_index):
        self.session.project.reverse(fragment_index)
        self.refresh()

    def editor_change_speed(self, fragment_index):
        ratio, ok = QInputDialog.getDouble(self, "Изменение скорости", "Введите коэфицент")
        if ok:
            self.session.project.change_speed(fragment_index, float(ratio))
            self.refresh()

    def editor_add_content(self, fragment_index):
        self.session.project.player.set_content(self.session.project.active_fragments[fragment_index])
        self.audio_name.setText(QUrl(self.session.project.player.fragment_name.content).fileName())
        self.duration_text.setText(f'0:00 / {self.session.project.player.duration}')
        self.refresh()

    def editor_concat(self, fragment_index):
        fragments = [x.content for x in self.session.project.active_fragments]
        choice, ok = QInputDialog.getItem(self, 'Склеить', 'Выбирите фрагмент, с которым нужно склеить текущий', fragments)
        if ok:
            next_fragment_index = fragments.index(choice)
            if next_fragment_index == fragment_index:
                msg = QMessageBox()
                msg.setText("Ошибка")
                msg.setInformativeText('Нельзя склеить элемент с самим собой')
                msg.exec_()
            else:
                self.session.project.concat(fragment_index, next_fragment_index)
        self.refresh()

    def editor_trim(self, fragment_index):
        a = TrimDialog(self)
        a.exec()
        results = a.getInputs()
        self.session.project.trim(fragment_index, results[0], results[1])
        self.refresh()

    def menu_new(self):
        name, ok = QInputDialog.getText(self, "Новый проект", "Введите название")
        if ok:
            self.session.project = Project(name)
        self.refresh()

    def menu_undo(self):
        self.session.project.undo()
        self.refresh()

    def menu_redo(self):
        self.session.project.redo()
        self.refresh()

class TrimDialog(QDialog):
    # T0D0 Сделать нормальный ползунок, а не два поля
    def __init__(self, parent):
        super().__init__(parent)
        self.first = QLineEdit(self)
        self.second = QLineEdit(self)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        layout = QFormLayout(self)
        layout.addRow("Начало", self.first)
        layout.addRow("Конец", self.second)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def getInputs(self):
        return self.first.text(), self.second.text()
