import json
import sys
from functools import partial

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import *


class Create(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(0, 148)
        self.setWindowTitle('Create Test')

        self.grid = QGridLayout()
        self.grid.setSpacing(20)
        self.setLayout(self.grid)

        self.combo_box_of_type = QComboBox()
        self.combo_box_of_type.addItems(['One Answer', 'Multiple Answers', 'Subsequence'])
        self.combo_box_of_type.currentIndexChanged.connect(self.evt_changer)
        self.grid.addWidget(self.combo_box_of_type, 0, 0, 1, 0)

        self.question_panel()
        self.down_panel()
        self.answer_list = []
        self.answer_y = 2
        self.answer_x = 0

        self.tasks = {}

    def evt_changer(self):
        for i in range(3, self.grid.count()):
            self.grid.itemAt(i).widget().deleteLater()
        self.question.setText('')
        self.answer_list = []
        self.answer_y = 2
        self.answer_x = 0
        self.down_panel()

    def next_task(self):
        if self.combo_box_of_type.currentIndex() == 0:
            self.tasks[f'{len(self.tasks) + 1}'] = {
                'type': 0,
                'question': self.question.toPlainText(),
                'answers': [i[1].text() for i in self.answer_list],
                'correct_answers': [i for i in range(0, len(self.answer_list)) if self.answer_list[i][0].isChecked()]
            }
        elif self.combo_box_of_type.currentIndex() == 1:
            self.tasks[f'{len(self.tasks) + 1}'] = {
                'type': 1,
                'question': self.question.toPlainText(),
                'answers': [i[1].text() for i in self.answer_list],
                'correct_answers': [i for i in range(0, len(self.answer_list)) if self.answer_list[i][0].isChecked()]
            }
        else:
            self.tasks[f'{len(self.tasks) + 1}'] = {
                'type': 2,
                'question': self.question.toPlainText(),
                'answers': [i[1].text() for i in self.answer_list],
                'correct_answers': [i[0].currentIndex() for i in self.answer_list]
            }
        self.evt_changer()

    def finish_tasks(self):
        for i in range(self.grid.count()):
            self.grid.itemAt(i).widget().deleteLater()

        name = QLabel('Creator Name:')
        description = QLabel('Description:')
        file_name = QLabel('File Name:')

        self.get_name = QLineEdit()
        self.get_description = QLineEdit()
        self.get_file_name = QLineEdit()

        confirm = QPushButton("Confirm")
        confirm.clicked.connect(self.save_file)

        self.grid.addWidget(name, 0, 0)
        self.grid.addWidget(self.get_name, 0, 1)
        self.grid.addWidget(description, 1, 0)
        self.grid.addWidget(self.get_description, 1, 1)
        self.grid.addWidget(file_name, 2, 0)
        self.grid.addWidget(self.get_file_name, 2, 1)
        self.grid.addWidget(confirm, 3, 0, 1, 0)
        self.resize(425, 170)

    def save_file(self):
        url = str(QFileDialog.getExistingDirectory())
        self.tasks['info'] = {
            'Creator Name': self.get_name.text(),
            'Description': self.get_description.text()
        }
        with open(f'{url}/{self.get_file_name.text()}.ht', 'w', encoding='utf-8') as file:
            json.dump(self.tasks, file, indent=4, ensure_ascii=False)
        sys.exit()

    def add_btn(self, index):
        if index == 0 or index == 1:
            radio_btn = QRadioButton()
            if index == 1:
                radio_btn.setAutoExclusive(False)
            text = QLineEdit()
            text.setMinimumWidth(100)

            self.grid.addWidget(radio_btn, self.answer_y, self.answer_x)
            self.grid.addWidget(text, self.answer_y, self.answer_x + 1)
            self.answer_list.append((radio_btn, text, 0))
        else:
            combo_box = QComboBox()
            combo_box.addItems(list(map(lambda x: str(x), list(range(1, len(self.answer_list) + 1)))))
            text = QLineEdit()
            text.setMinimumWidth(100)

            self.grid.addWidget(combo_box, self.answer_y, self.answer_x)
            self.grid.addWidget(text, self.answer_y, self.answer_x + 1)
            self.answer_list.append((combo_box, text, 2))

            for i in self.answer_list:
                i[0].addItems([str(len(self.answer_list))])

        if self.answer_y % 10 == 0:
            self.answer_y = 2
            self.answer_x += 2
        else:
            self.answer_y += 1

    def del_btn(self, index):
        try:
            self.answer_list[-1][0].deleteLater()
            self.answer_list[-1][1].deleteLater()

            del self.answer_list[-1]

            if self.answer_y % 10 == 0 and self.answer_y != 2:
                self.answer_y = 2
                self.answer_x -= 2
            else:
                self.answer_y -= 1
        except:
            pass

        if index == 2:
            try:
                for i in self.answer_list:
                    i[0].removeItem(len(self.answer_list))
            except:
                pass

    def question_panel(self):
        label = QLabel('Question:')
        label.setMaximumWidth(80)
        label.setFont(QFont("Arial", 13))
        self.grid.addWidget(label, 1, 0)

        self.question = QTextEdit()
        self.question.setMaximumHeight(60)
        self.question.setFont(QFont("Arial", 15))
        self.grid.addWidget(self.question, 1, 1, 1, 3)

    def down_panel(self):
        self.minus = QPushButton('-')

        self.plus = QPushButton('+')
        self.plus.setMaximumWidth(80)

        if self.combo_box_of_type.currentIndex() == 0:
            self.plus.clicked.connect(partial(self.add_btn, 0))
            self.minus.clicked.connect(partial(self.del_btn, 0))
        elif self.combo_box_of_type.currentIndex() == 1:
            self.plus.clicked.connect(partial(self.add_btn, 1))
            self.minus.clicked.connect(partial(self.del_btn, 1))
        else:
            self.plus.clicked.connect(partial(self.add_btn, 2))
            self.minus.clicked.connect(partial(self.del_btn, 2))

        self.next = QPushButton('Next')
        self.next.clicked.connect(self.next_task)

        self.finish = QPushButton("Finish")
        self.finish.clicked.connect(self.finish_tasks)

        self.grid.addWidget(self.minus, 11, 0)
        self.grid.addWidget(self.plus, 11, 1)
        self.grid.addWidget(self.next, 11, 2)
        self.grid.addWidget(self.finish, 11, 3)


class Pass(QWidget):
    def __init__(self):
        super().__init__()

        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.url = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "",
            "HlebTest (*.ht)",
        )
        if self.url[0] == '':
            sys.exit()

        with open(self.url[0], 'r') as file:
            self.tasks = json.load(file)

        creator = QLabel(f"Creator: {self.tasks['info']['Creator Name']}")
        creator.setFont(QFont("Arial", 15))
        description = QLabel(f"Description: {self.tasks['info']['Description']}")
        description.setFont(QFont("Arial", 15))

        self.grid.addWidget(creator, 0, 0)
        self.grid.addWidget(description, 1, 0)

        btn = QPushButton("Start")
        btn.clicked.connect(self.start)
        self.grid.addWidget(btn, 2, 0)

    def start(self):
        for i in range(0, self.grid.count()):
            self.grid.itemAt(i).widget().deleteLater()

        self.tasks_numbers = list(self.tasks.keys())[:-1]
        self.current_task = 1
        self.all_answers = []

        self.show_task()

    def next_task(self):
        for i in range(0, self.grid.count()):
            self.grid.itemAt(i).widget().deleteLater()

        if self.tasks[f'{self.current_task}']['type'] == 0:
            if self.answers[int(self.tasks[f'{self.current_task}']['correct_answers'][0])].isChecked():
                self.all_answers.append((self.current_task, self.tasks[f'{self.current_task}']['correct_answers'], 1))
            else:
                for i in range(0, len(self.answers)):
                    if self.answers[i].isChecked():
                        self.all_answers.append((self.current_task, [i], 0))

        elif self.tasks[f'{self.current_task}']['type'] == 1:
            answers = []
            for i in self.tasks[f'{self.current_task}']['correct_answers']:
                if self.answers[i].isChecked():
                    answers.append(i)
            if answers == self.tasks[f'{self.current_task}']['correct_answers']:
                self.all_answers.append((self.current_task, self.tasks[f'{self.current_task}']['correct_answers'], 1))
            else:
                answers = []
                for i in range(0, len(self.answers)):
                    if self.answers[i].isChecked():
                        answers.append(i)
                self.all_answers.append((self.current_task, answers, 0))

        else:
            answers = []
            for i, j in zip(self.tasks[f'{self.current_task}']['correct_answers'], self.answers):
                if i == j.currentIndex():
                    answers.append(i)

            if answers == self.tasks[f'{self.current_task}']['correct_answers']:
                self.all_answers.append((self.current_task, self.tasks[f'{self.current_task}']['correct_answers'], 1))
            else:
                answers = []
                for i in self.answers:
                    answers.append(i.currentIndex())
                self.all_answers.append((self.current_task, answers, 0))

        self.current_task += 1

        if self.current_task > len(self.tasks_numbers):
            self.show_result()
        else:
            self.show_task()

    def show_task(self):
        self.number_of_task = QLabel()
        self.question = QLabel()
        self.next_button = QPushButton('Next Task')
        self.next_button.clicked.connect(self.next_task)

        for i in range(0, self.grid.count()):
            self.grid.itemAt(i).widget().deleteLater()

        self.answer_y = 2
        self.answer_x = 0
        self.answers = []

        self.grid.addWidget(QLabel(f'{self.current_task}/{len(self.tasks_numbers)}'), 0, 0)
        self.grid.addWidget(QLabel(f'{self.tasks[f"{self.current_task}"]["question"]}'), 1, 0)

        if self.tasks[f'{self.current_task}']['type'] == 0 or self.tasks[f'{self.current_task}']['type'] == 1:
            for i in self.tasks[f'{self.current_task}']['answers']:
                radio_button = QRadioButton(i)
                if self.tasks[f'{self.current_task}']['type'] == 1:
                    radio_button.setAutoExclusive(False)
                self.grid.addWidget(radio_button, self.answer_y, self.answer_x)
                self.answers.append(radio_button)

                if self.answer_y % 10 == 0:
                    self.answer_y = 2
                    self.answer_x += 2
                else:
                    self.answer_y += 1
        else:
            for i in self.tasks[f'{self.current_task}']['answers']:
                combo_box = QComboBox()
                label = QLabel(i)

                self.grid.addWidget(combo_box, self.answer_y, self.answer_x)
                self.grid.addWidget(label, self.answer_y, self.answer_x + 1)
                self.answers.append(combo_box)

                if self.answer_y % 10 == 0:
                    self.answer_y = 2
                    self.answer_x += 2
                else:
                    self.answer_y += 1

            for i in self.answers:
                i.addItems(list(map(lambda x: str(x), list(range(1, len(self.answers) + 1)))))

        self.grid.addWidget(self.next_button, 12, 0)

    def show_result(self):
        for i in range(0, self.grid.count()):
            self.grid.itemAt(i).widget().deleteLater()

        self.grid.setSpacing(5)
        self.grid.setHorizontalSpacing(30)

        correct_answers = 0
        for i in self.all_answers:
            if i[2] == 1:
                correct_answers += 1
        self.setWindowTitle(
            f'{correct_answers}/{len(self.all_answers)}  {(correct_answers / len(self.all_answers) * 100):.2f}%')

        y = 0
        x = 0
        for i in self.all_answers:
            if i[2] == 1:
                label = QLabel(f'{i[0]}: {self.tasks[f"{i[0]}"]["question"]}')
                label.setStyleSheet('color: green')

                answers = ''
                for j in i[1]:
                    answers += f'{self.tasks[f"{i[0]}"]["answers"][j]}; '

                label_answers = QLabel(f'Your answers: {answers}')
                self.grid.addWidget(label, y, x)
                self.grid.addWidget(label_answers, y + 1, x)
                y += 2
            else:
                label = QLabel(f'{i[0]}: {self.tasks[f"{i[0]}"]["question"]}')
                label.setStyleSheet('color: red')

                answers = ''
                for j in self.tasks[f"{i[0]}"]['correct_answers']:
                    answers += f'{self.tasks[f"{i[0]}"]["answers"][j]}; '

                label_correct_answers = QLabel(f'Correct answers: {answers}')

                answers = ''
                for j in i[1]:
                    answers += f'{self.tasks[f"{i[0]}"]["answers"][j]}; '

                label_uncorrect_answers = QLabel(f'Your answers: {answers}')
                self.grid.addWidget(label, y, x)
                self.grid.addWidget(label_correct_answers, y + 1, x)
                self.grid.addWidget(label_uncorrect_answers, y + 2, x)
                y += 3

            if i[0] % 15 == 0:
                y = 0
                x += 1


class StartWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.windows = []

        self.setFixedSize(300, 200)

        grid = QGridLayout()
        grid.setSpacing(20)
        self.setLayout(grid)

        self.create_btn = QPushButton("Create Test")
        self.create_btn.setFont(QFont('Arial', 13))
        self.create_btn.setFixedSize(130, 130)
        self.create_btn.clicked.connect(self.evt_create)

        self.pass_btn = QPushButton("Past The Test")
        self.pass_btn.setFixedSize(130, 130)
        self.pass_btn.setFont(QFont('Arial', 13))
        self.pass_btn.clicked.connect(self.evt_pass)

        grid.addWidget(self.create_btn, 0, 0)
        grid.addWidget(self.pass_btn, 0, 1)

    def evt_create(self):
        window = Create()
        self.windows.append(window)
        window.show()
        self.destroy()

    def evt_pass(self):
        window = Pass()
        self.windows.append(window)
        window.show()
        self.destroy()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StartWindow()
    window.show()
    sys.exit(app.exec())
