from PyQt5.QtCore import *
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from random import sample
from random import randint

from astar import Astar_search
from puzzle import count_inversions
from rbfs import recursive_best_first_search


class PuzzleElement(QLabel):
    def __init__(self, num):
        super().__init__()
        self.setFixedSize(70, 70)
        self.setStyleSheet("background-color: white;")
        self.setText(str(num))

        font = self.font()
        font.setPointSize(20)
        self.setFont(font)

        self.setAlignment(Qt.AlignCenter)

    def update_value(self, num):
        self.setText(str(num))


class InputPuzzleElement(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setFixedSize(40, 40)
        self.setStyleSheet("background-color: white;")

    def check_value(self):
        if (self.text().isdigit() and int(self.text()) < 9 and int(self.text()) != 0) or self.text() == "":
            self.setStyleSheet("background-color: white;")
            return True
        else:
            self.setStyleSheet("background-color: #FE896E;")
            return False

    def setRed(self):
        self.setStyleSheet("background-color: #FE896E;")

    def setWhite(self):
        self.setStyleSheet("background-color: white;")

    def get_value(self):
        if self.check_value():
            return self.text()
        else:
            return None


class PuzzleLayout(QGridLayout):
    def __init__(self, arr):
        super().__init__()
        self.setSpacing(10)
        self.setVerticalSpacing(10)
        self.elements = []
        for i in range(9):
            element = PuzzleElement(arr[i])
            self.addWidget(element, i // 3, i % 3)
            self.elements.append(element)

    def update_layout(self, arr):
        for i in range(9):
            self.elements[i].update_value(arr[i])

    def setSize(self, size):
        for i in range(9):
            self.elements[i].setFixedSize(size, size)


class PuzzleInputLayout(QGridLayout):
    def __init__(self):
        super().__init__()
        self.setSpacing(10)
        self.setVerticalSpacing(10)
        self.elements = []
        for i in range(9):
            element = InputPuzzleElement()
            self.addWidget(element, i // 3, i % 3)
            self.elements.append(element)
        self.arr = None

    def setWhite(self):
        for element in self.elements:
            element.setStyleSheet("background-color: white;")

    def get_puzzle_values(self):
        try:
            values = []
            is_unique = True
            is_valid = True
            for element in self.elements:
                value = element.get_value()
                if value is None:
                    is_valid = False
                    continue

                if (value != '' and int(value) in values) or (value == '' and " " in values):
                    is_unique = False
                    element.setStyleSheet("background-color: #FE896E;")
                values.append(int(value) if value.isdigit() else " ")
            if is_unique and is_valid:
                return values
            else:
                return None
        except Exception as e:
            import traceback
            traceback.print_exc()

    def set_values(self, values):
        for i in range(9):
            self.elements[i].setText(str(values[i]))


class PuzzleInputDialog(QDialog):
    start_puzzle = None
    end_puzzle = None

    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(300, 500))
        self.setStyleSheet("background-color: #BFDB7F;")
        self.setWindowTitle("Введення головоломки")
        self.layout = QVBoxLayout(self)

        self.labelStart = QLabel("Введіть початковий стан:")
        self.laberEnd = QLabel("Введіть кінцевий стан:")
        self.input_start_layout = PuzzleInputLayout()
        self.input_start_layout.setAlignment(Qt.AlignHCenter)
        self.input_end_layout = PuzzleInputLayout()
        self.input_end_layout.setAlignment(Qt.AlignHCenter)

        self.classic_endButton = QPushButton("Класична кінцева розстановка")
        self.classic_endButton.setStyleSheet("background-color: #FFD798;")
        self.classic_endButton.setFixedSize(QSize(200, 30))
        self.classic_endButton.clicked.connect(self.classic_end)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.setStyleSheet("background-color: #FFD798;")
        self.button_box.accepted.connect(self.validate_input)
        self.button_box.rejected.connect(self.reject)

        self.layout.setSpacing(20)
        self.layout.addWidget(self.labelStart)
        self.layout.addLayout(self.input_start_layout)
        self.layout.addWidget(self.laberEnd)
        self.layout.addLayout(self.input_end_layout)
        self.layout.addWidget(self.classic_endButton)
        self.layout.itemAt(4).setAlignment(Qt.AlignHCenter)
        self.layout.addWidget(self.button_box)
        self.layout.itemAt(5).setAlignment(Qt.AlignHCenter)

    def classic_end(self):
        self.input_end_layout.set_values([1, 2, 3, 4, 5, 6, 7, 8, ''])

    def validate_input(self):
        self.input_start_layout.setWhite()
        self.input_end_layout.setWhite()
        self.start_puzzle = self.input_start_layout.get_puzzle_values()
        self.end_puzzle = self.input_end_layout.get_puzzle_values()
        if self.start_puzzle is not None and self.end_puzzle is not None:
            self.accept()

    def get_puzzle_input(self):
        return self.start_puzzle, self.end_puzzle


class RandomPuzzleDialog(QDialog):
    def __init__(self, start, end):
        super().__init__()
        self.setFixedSize(QSize(300, 500))
        self.setStyleSheet("background-color: #BFDB7F;")
        self.setWindowTitle("Випадкова головоломка")
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignVCenter)

        layout.addLayout(PuzzleLayout(start))
        layout.itemAt(0).setSize(40)
        layout.itemAt(0).setAlignment(Qt.AlignHCenter)

        arrow = QLabel("↓")
        font = QFont("Arial", 24)
        arrow.setFont(font)
        layout.addWidget(arrow)
        layout.itemAt(1).setAlignment(Qt.AlignHCenter)

        layout.addLayout(PuzzleLayout(end))
        layout.itemAt(2).setSize(40)
        layout.itemAt(2).setAlignment(Qt.AlignHCenter)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.setStyleSheet("background-color: #FFD798;")
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        layout.itemAt(3).setAlignment(Qt.AlignHCenter)


class MainWindow(QMainWindow):
    start = None
    goal = None
    solution_path = None

    def __init__(self):
        super().__init__()

        self.setWindowTitle("8 puzzle solver")
        self.setStyleSheet("background-color: #FFD798;")
        self.setFixedSize(QSize(500, 600))

        mainWidget = QWidget()
        mainLayout = QVBoxLayout(mainWidget)

        enterButton = QPushButton("Ввести")
        randomButton = QPushButton("Рандом")
        startButton = QPushButton("Вирішити задачу")
        enterButton.setStyleSheet("background-color: #BFDB7F;")
        randomButton.setStyleSheet("background-color: #BFDB7F;")
        startButton.setStyleSheet("background-color: #BFDB7F;")
        enterButton.setFixedSize(QSize(90, 30))
        randomButton.setFixedSize(QSize(90, 30))
        startButton.setFixedSize(QSize(150, 30))
        enterButton.clicked.connect(self.enter_button_clicked)
        randomButton.clicked.connect(self.random_button_clicked)
        startButton.clicked.connect(self.start_button_clicked)

        buttonsLayout = QHBoxLayout()
        buttonsLayout.setSpacing(20)
        buttonsLayout.addWidget(enterButton)
        buttonsLayout.addWidget(randomButton)
        buttonsLayout.setAlignment(Qt.AlignHCenter)

        radio_astar = QRadioButton("A*")
        radio_rbfs = QRadioButton("RBFS")
        self.radio_astar = radio_astar
        self.radio_rbfs = radio_rbfs

        radioLayout = QHBoxLayout()
        radioLayout.addWidget(radio_astar)
        radioLayout.addWidget(radio_rbfs)

        self.puzzleLayout = PuzzleLayout([" ", " ", " ", " ", " ", " ", " ", " ", " "])

        fileButton = QPushButton("Записати в файл")
        fileButton.setStyleSheet("background-color: #BFDB7F;")
        fileButton.setFixedSize(QSize(150, 30))
        fileButton.clicked.connect(self.file_button_clicked)

        mainLayout.setAlignment(Qt.AlignHCenter)
        mainLayout.setSpacing(20)
        mainLayout.addLayout(buttonsLayout)
        mainLayout.addWidget(radio_astar)
        mainLayout.addWidget(radio_rbfs)
        mainLayout.addWidget(startButton)
        mainLayout.itemAt(3).setAlignment(Qt.AlignHCenter)
        mainLayout.addLayout(self.puzzleLayout)
        mainLayout.addWidget(fileButton)
        mainLayout.itemAt(5).setAlignment(Qt.AlignHCenter)
        self.setCentralWidget(mainWidget)

        self.error_box = QMessageBox()
        self.error_box.setWindowTitle("Помилка")
        self.error_box.setStyleSheet("QMessageBox { background-color: #FE896E;}"
                                   "QPushButton { background-color: #FFD798; }")
        self.error_box.addButton(QMessageBox.Ok)

        self.message_box = QMessageBox()
        self.message_box.setWindowTitle("Повідомлення")
        self.message_box.setStyleSheet("QMessageBox { background-color: #BFDB7F;}"
                                     "QPushButton { background-color: #FFD798; }")
        self.message_box.addButton(QMessageBox.Ok)

    def start_button_clicked(self):
        try:
            if self.start is None or self.goal is None:
                self.error_box.setText("Оберіть початковий і кінцевий стани")
                self.error_box.exec()
                return
            if self.radio_astar.isChecked():
                self.solution_path = Astar_search(self.start, self.goal)
            elif self.radio_rbfs.isChecked():
                self.solution_path = recursive_best_first_search(self.start, self.goal)
            else:
                self.error_box.setText("Будь ласка, оберіть один з алгоритмів")
                self.error_box.exec()
                return
            if self.solution_path is None:
                self.error_box.setText("Задача не має розв'язку")
                self.error_box.exec()
                return
            path = self.solution_path[:]

            self.display_solution(path)
        except Exception as e:
            import traceback
            traceback.print_exc()

    def display_solution(self, path):
        if not path:
            self.message_box.setText("Готово!!!")
            QTimer.singleShot(1500, lambda: self.message_box.exec())
            return

        step = path.pop(0)
        QTimer.singleShot(1000, lambda step=step: self.update_puzzle(step, path))
        QApplication.processEvents()

    def update_puzzle(self, step, path):
        self.puzzleLayout.update_layout(step)
        QApplication.processEvents()
        self.display_solution(path)

    def enter_button_clicked(self):
        puzzle_input_dialog = PuzzleInputDialog()

        if puzzle_input_dialog.exec_() == QDialog.Accepted:
            self.start, self.goal = puzzle_input_dialog.get_puzzle_input()
            self.puzzleLayout.update_layout(self.start)

    def random_button_clicked(self):
        start = sample(range(1, 9), 8)
        end = sample(range(1, 9), 8)
        while count_inversions(start) % 2 != count_inversions(end) % 2:
            end = sample(range(1, 9), 8)
        start.insert(randint(0, 8), " ")
        end.insert(randint(0, 8), " ")

        random_dialog = RandomPuzzleDialog(start, end)

        if random_dialog.exec_() == QDialog.Accepted:
            self.start = start[:]
            self.goal = end[:]
            self.puzzleLayout.update_layout(self.start)

    def str_puzzle(self, i):
        state = self.solution_path[i]
        state[state.index(" ")] = "_"
        return str(' '.join(map(str, state[0:3])) + '\n' + ' '.join(map(str, state[3:6])) + '\n' + ' '.join(map(str, state[6:9])))

    def file_button_clicked(self):
        if self.solution_path is None:
            self.error_box.setText("Жодногорозв'язку знайдено не було")
            self.error_box.exec()
            return
        with open("solution.txt", 'w') as file:
            file.write(self.str_puzzle(0))
            for i in range(1, len(self.solution_path)):
                file.write("\n\n  | \n \\|/ \n\n")
                file.write(self.str_puzzle(i))
 
        self.message_box.setText("Розв'язок записано у файл solution.txt")
        self.message_box.exec()


