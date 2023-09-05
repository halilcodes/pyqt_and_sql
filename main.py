import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QComboBox, QDialog, QVBoxLayout,\
    QGridLayout, QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QAction
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumHeight(400)
        self.setMinimumWidth(450)

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_nemu_item = self.menuBar().addMenu("&Edit")

        add_student_action = QAction("Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        search_action = QAction("Search", self)
        search_action.triggered.connect(self.search)
        edit_nemu_item.addAction(search_action)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)   # delete index numbers of table

        self.setCentralWidget(self.table)
        self.load_data()

    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_num, row_data in enumerate(result):
            # st_id, name, course, phone = row_data
            self.table.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                self.table.setItem(row_num, col_num, QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        print("search action triggered")
        search = SearchStudent()
        search.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert New Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # add student name QLine
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Student Name")

        # add courses combobox
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Architect", "Physics", "Engineering"]
        self.course_name.addItems(courses)

        # add phone number QLine
        self.student_phone = QLineEdit()
        self.student_phone.setPlaceholderText("Phone Number")

        # add submit button
        submit_button = QPushButton("Add Student")
        submit_button.clicked.connect(self.submit_student)

        layout.addWidget(self.student_name)
        layout.addWidget(self.course_name)
        layout.addWidget(self.student_phone)
        layout.addWidget(submit_button)

        self.setLayout(layout)

    def submit_student(self):
        name = self.student_name.text().title()
        phone = self.student_phone.text()
        course = self.course_name.currentText()
        print(f"{name =} {course = } {phone =}")
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
                       (name, course, phone))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()
        self.close()


class SearchStudent(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Name")

        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search)

        layout.addWidget(self.name_edit)
        layout.addWidget(search_button)

        self.setLayout(layout)

    def search(self):
        query = self.name_edit.text().title()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE name LIKE ?", ("%"+query+"%",))
        rows = list(result)
        names = [i[1] for i in rows]    # extract full names to search

        for name in names:
            # below code does not work if same exact name occurs more than once
            # item = main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)[0]
            items = main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
            for item in items:
                print(item)
                main_window.table.item(item.row(), 1).setSelected(True)

        cursor.close()
        connection.close()
        self.close()


app = QApplication(sys.argv)

main_window = MainWindow()
main_window.show()


sys.exit(app.exec())
