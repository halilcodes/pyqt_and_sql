import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QComboBox, QDialog, QVBoxLayout, \
    QGridLayout, QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QToolBar, QStatusBar, QMessageBox
from PyQt6.QtGui import QAction, QIcon
import sqlite3
import mysql.connector
from keys import mysql_root


class DatabaseConnection:
    def __init__(self, host="localhost", username="root", password=mysql_root, database="school"):
        self.host = host
        self.username = username
        self.password = password
        self.database = database

    def connect(self):
        connection = mysql.connector.connect(host=self.host, user=self.username,
                                             password=self.password, database=self.database)
        return connection


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        # self.setMinimumHeight(500)
        # self.setMinimumWidth(450)
        self.setMinimumSize(450, 500)

        # add menubar items
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_nemu_item = self.menuBar().addMenu("&Edit")

        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        add_exit_action = QAction("Exit", self)
        add_exit_action.triggered.connect(self.close)
        file_menu_item.addAction(add_exit_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.triggered.connect(self.about)

        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        search_action.triggered.connect(self.search)
        edit_nemu_item.addAction(search_action)

        # add main table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)  # delete index numbers of table

        self.setCentralWidget(self.table)
        self.load_data()

        # create toolbar
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        # add elements to toolbar
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        # create statusbar
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        # detect a cell click
        self.table.cellClicked.connect(self.cell_clicked)
        # add widgets to statusbar when cell is clicked

    def cell_clicked(self):
        self.statusbar.destroy()
        print("cell clicked")
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    def load_data(self):
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students")
        result = cursor.fetchall()
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
        search = SearchStudent()
        search.exec()

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

    def about(self):
        dialog = AboutDialog()
        dialog.exec()


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        content = """
        Created by Halil Can Hasmer in 2023.
        This app is part of my portfolio.
        Created during I study to a course of Ardit on Udemy.
        
        One day, when I build a tradebot, this will be a nice memoir.
        """
        self.setText(content)


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
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (%s, %s, %s)",
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
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students WHERE name LIKE %s", ("%" + query + "%",))
        result = cursor.fetchall()
        rows = list(result)
        names = [i[1] for i in rows]  # extract full names to search

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


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edit Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # get current information of the student
        index = main_window.table.currentRow()
        self.id_ = main_window.table.item(index, 0).text()
        student_name = main_window.table.item(index, 1).text()
        course = main_window.table.item(index, 2).text()
        phone = main_window.table.item(index, 3).text()

        # add student name QLine
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Student Name")

        # add courses combobox
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Architect", "Physics", "Engineering"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course)

        # add phone number QLine
        self.student_phone = QLineEdit(phone)
        self.student_phone.setPlaceholderText("Phone Number")

        # add update button
        update_button = QPushButton("Update Student")
        update_button.clicked.connect(self.update_student)

        # add widgets to window
        layout.addWidget(self.student_name)
        layout.addWidget(self.course_name)
        layout.addWidget(self.student_phone)
        layout.addWidget(update_button)

        self.setLayout(layout)

    def update_student(self):
        connection = DatabaseConnection().connect()
        print((self.student_name.text(), self.course_name.currentText(), self.student_phone.text(), self.id_))
        cursor = connection.cursor()
        # update selected row
        cursor.execute("UPDATE students SET name = %s, course = %s, mobile = %s WHERE id = %s",
                       (self.student_name.text().title(), self.course_name.currentText(),
                        self.student_phone.text(), self.id_))

        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()
        self.close()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        # self.setFixedWidth(250)
        # self.setFixedHeight(100)
        self.setWindowTitle("Delete Student Data")

        layout = QGridLayout()
        confirmation = QLabel("Are You Sure You Want To Delete Data?")
        yes_button = QPushButton("Yes")
        yes_button.clicked.connect(self.delete_student)
        no_button = QPushButton("No")
        no_button.clicked.connect(self.no_click)

        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes_button, 1, 0)
        layout.addWidget(no_button, 1, 1)

        self.setLayout(layout)

    def no_click(self):
        self.close()

    def delete_student(self):
        index = main_window.table.currentRow()
        id_ = main_window.table.item(index, 0).text()

        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        # delete selected row
        cursor.execute("DELETE FROM students WHERE id = %s", (id_,))

        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()
        self.close()

        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("Data successfully deleted")
        confirmation_widget.exec()


app = QApplication(sys.argv)

main_window = MainWindow()
main_window.show()

sys.exit(app.exec())
