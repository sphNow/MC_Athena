from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableView, QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtCore import Qt

from config import dbAthena_Net

class MyFormUsers(QWidget):
    def __init__(self):
        super().__init__()

        # Create database connection
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(dbAthena_Net)
        if not self.db.open():
            QMessageBox.critical(None, "Error", "Could not open database")

        # Create model and view
        self.model = QSqlTableModel()
        self.model.setTable("USER")
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()
        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.doubleClicked.connect(self.populate_fields)

        # Create form widgets
        user_employee_label = QLabel("User Employee:")
        self.user_employee_edit = QLineEdit()
        user_email_label = QLabel("User Email:")
        self.user_email_edit = QLineEdit()
        user_name_label = QLabel("User Name:")
        self.user_name_edit = QLineEdit()
        is_alive_label = QLabel("Is Alive:")
        self.is_alive_edit = QLineEdit()
        is_blocked_label = QLabel("Is Blocked:")
        self.is_blocked_edit = QLineEdit()
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add_record)
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete_record)
        update_button = QPushButton("Update")
        update_button.clicked.connect(self.update_record)

        # Create layout
        form_layout = QVBoxLayout()
        user_employee_layout = QHBoxLayout()
        user_employee_layout.addWidget(user_employee_label)
        user_employee_layout.addWidget(self.user_employee_edit)
        user_email_layout = QHBoxLayout()
        user_email_layout.addWidget(user_email_label)
        user_email_layout.addWidget(self.user_email_edit)
        user_name_layout = QHBoxLayout()
        user_name_layout.addWidget(user_name_label)
        user_name_layout.addWidget(self.user_name_edit)
        is_alive_layout = QHBoxLayout()
        is_alive_layout.addWidget(is_alive_label)
        is_alive_layout.addWidget(self.is_alive_edit)
        is_blocked_layout = QHBoxLayout()
        is_blocked_layout.addWidget(is_blocked_label)
        is_blocked_layout.addWidget(self.is_blocked_edit)
        button_layout = QHBoxLayout()
        button_layout.addWidget(add_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(update_button)
        form_layout.addLayout(user_employee_layout)
        form_layout.addLayout(user_email_layout)
        form_layout.addLayout(user_name_layout)
        form_layout.addLayout(is_alive_layout)
        form_layout.addLayout(is_blocked_layout)
        form_layout.addLayout(button_layout)
        form_layout.addWidget(self.view)
        self.setLayout(form_layout)

    def populate_fields(self, index):
        row = index.row()
        record = self.model.record(row)
        user_employee = record.value("USER_EMPLOYEE")
        user_email = record.value("USER_EMAIL")
        user_name = record.value("USER_NAME")
        is_alive = record.value("IS_ALIVE")
        is_blocked = record.value("IS_BLOCKED")
        self.user_employee_edit.setText(user_employee)
        self.user_email_edit.setText(user_email)
        self.user_name_edit.setText(user_name)
        self.is_alive_edit.setText(str(is_alive))
        self.is_blocked_edit.setText(str(is_blocked))

    def add_record(self):
        user_employee = self.user_employee_edit.text()
        user_email = self.user_email_edit.text()
        user_name = self.user_name_edit.text()
        is_alive = self.is_alive_edit.text()
        is_blocked = self.is_blocked_edit.text()
        if user_employee and user_email and user_name and is_alive and is_blocked:
            record = self.model.record()
            record.setValue("USER_EMPLOYEE", user_employee)
            record.setValue("USER_EMAIL", user_email)
            record.setValue("USER_NAME", user_name)
            record.setValue("IS_ALIVE", int(is_alive))
            record.setValue("IS_BLOCKED", int(is_blocked))
            if self.model.insertRecord(-1, record):
                self.model.submitAll()
                self.user_employee_edit.clear()
                self.user_email_edit.clear()
                self.user_name_edit.clear()
                self.is_alive_edit.clear()
                self.is_blocked_edit.clear()
        else:
            QMessageBox.warning(None, "Warning", "Please fill in all fields")

    def delete_record(self):
        row = self.view.currentIndex().row()
        if row >= 0:
            self.model.removeRow(row)
            self.model.submitAll()

    def update_record(self):
        row = self.view.currentIndex().row()
        if row >= 0:
            record = self.model.record(row)
            user_employee = self.user_employee_edit.text()
            user_email = self.user_email_edit.text()
            user_name = self.user_name_edit.text()
            is_alive = self.is_alive_edit.text()
            is_blocked = self.is_blocked_edit.text()
            if user_employee and user_email and user_name and is_alive and is_blocked:
                record.setValue("USER_EMPLOYEE", user_employee)
                record.setValue("USER_EMAIL", user_email)
                record.setValue("USER_NAME", user_name)
                record.setValue("IS_ALIVE", int(is_alive))
                record.setValue("IS_BLOCKED", int(is_blocked))
                if self.model.setRecord(row, record):
                    self.model.submitAll()
            else:
                QMessageBox.warning(None, "Warning", "Please fill in all fields")