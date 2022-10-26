from PyQt6.QtWidgets import QWidgetAction

def create_menubar(self):
    textManageAction = QWidgetAction(self)
    textManageAction.setText("File")
    #textManageAction.triggered.connect(self.show_text_manager_window)

    helpAction = QWidgetAction(self)
    helpAction.setText("О программе")
    #helpAction.triggered.connect(self.show_help_screen)

    leaderboard_table_action = QWidgetAction(self)
    leaderboard_table_action.setText("Таблица лидеров")
    #leaderboard_table_action.triggered.connect(self.show_leaderboard_screen)

    menuBar = self.menuBar()

    settingsMenu = menuBar.addMenu("Настройки")
    settingsMenu.addSeparator()
    settingsMenu.addAction(textManageAction)

    leaderboard_menu = menuBar.addMenu("Рейтинг")
    leaderboard_menu.addAction(leaderboard_table_action)
    helpMenu = menuBar.addMenu("Помощь")
    helpMenu.addAction(helpAction)