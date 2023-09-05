import sys
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget,\
                            QGridLayout, QLineEdit, QPushButton
import datetime as dt


class AgeCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Age Calculator")

        grid = QGridLayout()

        # create widgets
        name_label = QLabel("Name: ")
        self.name_line_edit = QLineEdit()

        date_label = QLabel("Date of Birth MM/DD/YYYY: ")
        self.date_line_edit = QLineEdit()

        calculate_button = QPushButton("Calculate Age")
        calculate_button.clicked.connect(self.calculate_age)
        self.output_label = QLabel("")

        # add to grid
        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name_line_edit, 0, 1)
        grid.addWidget(date_label, 1, 0)
        grid.addWidget(self.date_line_edit, 1, 1)

        grid.addWidget(calculate_button, 2, 0, 1, 2)    # row:2, column:0 / spanning across 1 Column, 2 Rows
        grid.addWidget(self.output_label, 3, 0, 1, 2)     # row:3, column:0 / spanning across 1 Column, 2 Rows

        # add the grid to QWidget itself
        self.setLayout(grid)

    def calculate_age(self):
        current_date = dt.datetime.now()
        str_input = self.date_line_edit.text()
        birth_date = dt.datetime.strptime(str_input, "%m/%d/%Y")
        age = current_date.year - birth_date.year
        if current_date.month > birth_date.month:
            age += 1
        elif current_date.month == birth_date.month and current_date.day >= birth_date.day:
            age += 1
        self.output_label.setText(f"{self.name_line_edit.text().title()} is {age} years old")
        return age


app = QApplication(sys.argv)
age_calculator = AgeCalculator()
age_calculator.show()

sys.exit(app.exec())
