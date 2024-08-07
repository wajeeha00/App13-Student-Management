from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QFormLayout, QComboBox, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QMessageBox
import sys
import sqlite3

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Student Management System')
        file_menu_item = self.menuBar().addMenu('&File')
        help_menu_item = self.menuBar().addMenu('&Help')
        edit_menu_item = self.menuBar().addMenu('&Edit')

        add_student_action = QAction('Add Student', self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        search_student_action = QAction('Search Student', self)
        search_student_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_student_action)

        about_action = QAction('About', self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['ID', 'Name', 'Course', 'Mobile'])
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

    def load_data(self):
        connection = sqlite3.connect('database.db')
        result = connection.execute('SELECT * FROM students')
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        dialog = InsertDialog(self)
        dialog.exec()
    
    def search(self):
        dialog = SearchDialog(self)
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Add Student Data')
        self.setFixedWidth(300)
        self.setFixedHeight(200)

        layout = QVBoxLayout()

        self.student_name = QLineEdit(self)
        self.student_name.setPlaceholderText('Enter student name')
        layout.addWidget(self.student_name)

        self.course= QComboBox()
        courses = ['Math', 'Science', 'History', 'Geography', 'Computer Science']
        self.course.addItems(courses)
        layout.addWidget(self.course)

        self.mobile = QLineEdit(self)
        self.mobile.setPlaceholderText('Enter mobile number')
        layout.addWidget(self.mobile)

        self.button = QPushButton('Register', self)
        self.button.clicked.connect(self.add_student)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course.itemText(self.course.currentIndex())
        mobile = self.mobile.text()

        if name and course and mobile:
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()
            cursor.execute('INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)', (name, course, mobile))
            connection.commit()
            cursor.close()
            connection.close()

            self.parent().load_data()
            self.close()
        else:
            QMessageBox.warning(self, 'Error', 'Please fill in all fields')

class SearchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Search Student Data')
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.student_name = QLineEdit(self)
        self.student_name.setPlaceholderText('Enter student name')
        layout.addWidget(self.student_name)

        self.button = QPushButton('Search', self)
        self.button.clicked.connect(self.search_student)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def search_student(self):
        name = self.student_name.text()

        if name:
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM students WHERE name = ?', (name,))
            result = cursor.fetchone()
            cursor.close()
            connection.close()

            if result:
                QMessageBox.information(self, 'Success', f'Name: {result[1]}\nCourse: {result[2]}\nMobile: {result[3]}')
            else:
                QMessageBox.warning(self, 'Error', 'Student not found')
            self.close()
        else:
            QMessageBox.warning(self, 'Error', 'Please fill in all fields')

app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())
