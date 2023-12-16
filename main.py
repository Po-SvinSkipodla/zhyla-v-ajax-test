import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QPushButton, QVBoxLayout, QWidget
from terminal import Terminal


class COMTerminalApp(QMainWindow):
    def __init__(self):
        super(COMTerminalApp, self).__init__()
        self.index = 0
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        self.add_new_tab()
        add_tab_button = QPushButton("Add terminal")
        add_tab_button.clicked.connect(self.add_new_tab)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        main_layout.addWidget(add_tab_button)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        self.setCentralWidget(central_widget)
        self.setWindowTitle("COM Terminal")

    def add_new_tab(self):
        new_terminal = Terminal()
        self.index += 1
        index = self.tabs.addTab(new_terminal, f"COM Terminal {self.index}")
        self.tabs.setCurrentIndex(index)

    def close_tab(self, index):
        widget_to_remove = self.tabs.widget(index)
        widget_to_remove.deleteLater()  # Видаляємо вкладку
        self.tabs.removeTab(index)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = COMTerminalApp()
    main_window.show()
    sys.exit(app.exec_())
