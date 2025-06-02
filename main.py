import sys
import os
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow
from calculator import Calculator

def resource_path(relative_path):
    """Получает путь к ресурсу, работает и в PyInstaller, и в IDE."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 450)
        MainWindow.setWindowIcon(QtGui.QIcon(resource_path("icon.ico")))

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)

        self.label = QtWidgets.QLabel("", parent=self.centralwidget)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label.setStyleSheet("font-size: 28px; color: white; background-color: #222; padding: 10px; border-radius: 10px;")
        self.label.setMinimumHeight(60)
        self.gridLayout.addWidget(self.label, 0, 0, 1, 4)

        buttons = {
            (1, 0): ("C", self.clear_label),
            (1, 1): ("(", self.write_number),
            (1, 2): (")", self.write_number),
            (1, 3): ("\u232b", self.backspace),
            (2, 0): ("7", self.write_number),
            (2, 1): ("8", self.write_number),
            (2, 2): ("9", self.write_number),
            (2, 3): ("/", self.write_number),
            (3, 0): ("4", self.write_number),
            (3, 1): ("5", self.write_number),
            (3, 2): ("6", self.write_number),
            (3, 3): ("*", self.write_number),
            (4, 0): ("1", self.write_number),
            (4, 1): ("2", self.write_number),
            (4, 2): ("3", self.write_number),
            (4, 3): ("-", self.write_number),
            (5, 0): ("0", self.write_number),
            (5, 1): (".", self.write_number),
            (5, 2): ("=", self.calculate_result),
            (5, 3): ("+", self.write_number),
        }

        self.buttons = {}

        for pos, (text, handler) in buttons.items():
            btn = QtWidgets.QPushButton(text, parent=self.centralwidget)
            btn.setMinimumSize(0, 50)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 20px;
                    color: white;
                    background-color: #444;
                    border: none;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: #555;
                }
                QPushButton:pressed {
                    background-color: #666;
                }
            """)
            if text == "=":
                btn.setStyleSheet(btn.styleSheet().replace("#444", "#0066cc"))
            self.gridLayout.addWidget(btn, *pos)
            self.buttons[text] = btn
            if handler == self.write_number:
                btn.clicked.connect(lambda _, t=text: self.write_number(t))
            else:
                btn.clicked.connect(handler)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        MainWindow.setMenuBar(self.menubar)
        MainWindow.setStyleSheet("background-color: #121212;")

        self.calculator = Calculator()
        self.just_evaluated = False

        MainWindow.keyPressEvent = self.keyPressEvent

    def keyPressEvent(self, event):
        key = event.key()
        text = event.text()
        if text in "0123456789+-*/().":
            self.write_number(text)
        elif key == QtCore.Qt.Key.Key_Backspace:
            self.backspace()
        elif key == QtCore.Qt.Key.Key_Enter or key == QtCore.Qt.Key.Key_Return:
            self.calculate_result()
        elif key == QtCore.Qt.Key.Key_Escape:
            self.clear_label()

    def write_number(self, number):
        operators = "+-*/"
        current = self.label.text()

        if self.just_evaluated:
            if number in "0123456789.()":
                self.label.setText(number if number != "." else "0.")
            elif number in operators:
                self.label.setText(current + number)
            self.just_evaluated = False
            return

        if current == "Ошибка":
            if number in "0123456789.()":
                self.label.setText(number if number != "." else "0.")
            return

        last_char = current[-1] if current else ""

        if not current:
            if number in operators or number == ")":
                return
            if number == ".":
                self.label.setText("0.")
                return
            self.label.setText(number)
            return

        if number in operators and (last_char in operators or last_char == "."):
            return

        if number == ")":
            if current.count("(") <= current.count(")") or last_char in operators + "(":
                return

        if number == "(":
            if last_char.isdigit() or last_char == "." or last_char == ")":
                self.label.setText(current + "*" + number)
                return

        if number == ".":
            if last_char in operators + ".(" or not last_char.isdigit():
                return
            i = len(current) - 1
            while i >= 0 and (current[i].isdigit() or current[i] == "."):
                if current[i] == ".":
                    return
                i -= 1

        if number.isdigit():
            i = len(current) - 1
            while i >= 0 and (current[i].isdigit() or current[i] == "."):
                i -= 1
            token = current[i+1:]
            if token.startswith("0") and "." not in token and len(token) > 1:
                current = current[:i+1] + token.lstrip("0")
                if current == "":
                    current = "0"

        self.label.setText(current + number)
        self.just_evaluated = False

    def calculate_result(self):
        expression = self.label.text()
        try:
            result = self.calculator.calculate(expression)
            if isinstance(result, float):
                result = int(result) if result.is_integer() else round(result, 3)
            self.label.setText(str(result))
            self.just_evaluated = True
        except Exception:
            self.label.setText("Ошибка")
            self.just_evaluated = False

    def clear_label(self):
        self.label.setText("")

    def backspace(self):
        current = self.label.text()
        if current and current != "Ошибка":
            self.label.setText(current[:-1])
        else:
            self.label.setText("")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.setWindowTitle("Numbra")
    MainWindow.show()
    sys.exit(app.exec())