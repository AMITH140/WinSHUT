import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QRadioButton, QButtonGroup, QPushButton, QLineEdit
from PyQt5.QtGui import QFont,QIcon
from PyQt5.QtCore import QTimer, Qt

class ShutdownSleepTimer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("WinShut")
        self.setGeometry(100, 100, 300, 200)
        self.setStyleSheet("background-color: rgb(0, 0, 12);")

        layout = QVBoxLayout()

        timer_label = QLabel("Set Timer (minutes):")
        timer_label.setFont(QFont("roboto", 12))
        timer_label.setStyleSheet("color: white;")
        layout.addWidget(timer_label)

        self.timer_entry = QLineEdit()
        self.timer_entry.setFont(QFont("roboto", 12))
        self.timer_entry.setStyleSheet("color: white;")
        layout.addWidget(self.timer_entry)

        option_group = QButtonGroup()

        shutdown_radio = QRadioButton("Shutdown")
        shutdown_radio.setFont(QFont("roboto", 12))
        shutdown_radio.setStyleSheet("color: white;")
        layout.addWidget(shutdown_radio)

        sleep_radio = QRadioButton("Sleep")
        sleep_radio.setFont(QFont("roboto", 12))
        sleep_radio.setStyleSheet("color: white;")
        option_group.addButton(sleep_radio)
        layout.addWidget(sleep_radio)

        start_button = QPushButton("Start")
        start_button.setFont(QFont("roboto", 14))
        start_button.setStyleSheet("background-color: blue; color: white;")
        start_button.clicked.connect(self.shutdown_or_sleep)
        layout.addWidget(start_button)

        self.setLayout(layout)

    def shutdown_or_sleep(self):
        selected_option = "Shutdown" if self.sender().isChecked() else "Sleep"
        time_in_minutes = int(self.timer_entry.text())
        time_in_seconds = time_in_minutes * 60

        # Disable the Start button
        self.sender().setEnabled(False)

        # Create a QTimer to delay the shutdown/sleep
        timer = QTimer(self)
        timer.setSingleShot(True)
        timer.timeout.connect(lambda: self.perform_shutdown_sleep(selected_option))
        timer.start(time_in_seconds * 1000)  # Convert to milliseconds

    def perform_shutdown_sleep(self, selected_option):
        if selected_option == "Shutdown":
            import subprocess
            subprocess.call(["shutdown", "/s", "/t", "0"])
        else:
            import ctypes
            ctypes.windll.PowrProf.SetSuspendState(0, 1, 0)

        # Re-enable the Start button
        self.sender().setEnabled(True)
        self.setWindowIcon(QIcon("MYOWNPROJECTS/Winshut/icon.png"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ShutdownSleepTimer()
    app.setWindowIcon(QIcon("MYOWNPROJECTS/Winshut/icon.png"))
    window.show()
    sys.exit(app.exec_())
