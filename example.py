import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QComboBox,\
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


class SpeedClaculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Average Speed Calculator")

        grid = QGridLayout()

        # create widgets
        distance_label = QLabel("Distance: ")
        self.distance_edit = QLineEdit()

        self.mile_km_box = QComboBox()
        self.mile_km_box.addItem('Metric (km)')
        self.mile_km_box.addItem('Imperial (Miles)')
        self.mile_km_box.activated.connect(self.current_index)

        time_label = QLabel("Time (hours): ")
        self.time_edit = QLineEdit()

        calculate_button = QPushButton("Calculate")
        calculate_button.clicked.connect(self.calculate_speed)

        self.output_label = QLabel("")

        # add unit variable
        self.unit = "kmh"

        # add widgets to grid
        grid.addWidget(distance_label, 0, 0)
        grid.addWidget(self.distance_edit, 0, 1)
        grid.addWidget(self.mile_km_box, 0, 2)

        grid.addWidget(time_label, 1, 0)
        grid.addWidget(self.time_edit, 1, 1)

        grid.addWidget(calculate_button, 2, 1)
        grid.addWidget(self.output_label, 3, 0, 1, 2)

        # add the grid to QWidget itself
        self.setLayout(grid)

    def current_index(self, index):
        cindex = self.mile_km_box.currentIndex()
        current_text = self.mile_km_box.currentText()
        print(f"Index signal: {index}, currentIndex {cindex}, text: {current_text}")
        if index == 1:
            self.unit = "mph"
        else:
            self.unit = "kmh"
        return index

    def calculate_speed(self):
        distance = float(self.distance_edit.text())
        time_passed = float(self.time_edit.text())
        avg = distance / time_passed
        self.output_label.setText(f"Average speed: {avg:.2f} {self.unit}")


app = QApplication(sys.argv)
# age_calculator = AgeCalculator()
# age_calculator.show()
speed_calculator = SpeedClaculator()
speed_calculator.show()


sys.exit(app.exec())
