from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableView, QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtCore import Qt

from config import dbAthena_Net

class MyFormUsersTeam(QWidget):
    def __init__(self):
        super().__init__()

        # Create database connection
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(dbAthena_Net)
        if not self.db.open():
            QMessageBox.critical(None, "Error", "Could not open database")

        # Create model and view
        self.model = QSqlTableModel()
        self.model.setTable("AREA_USER")
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()
        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.doubleClicked.connect(self.populate_fields)

        # Create form widgets
        area_dept_cod_label = QLabel("Area Dept Cod:")
        self.area_dept_cod_edit = QLineEdit()
        user_cod_label = QLabel("User Cod:")
        self.user_cod_edit = QLineEdit()
        role_cod_label = QLabel("Role Cod:")
        self.role_cod_edit = QLineEdit()
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add_record)
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete_record)
        update_button = QPushButton("Update")
        update_button.clicked.connect(self.update_record)

        # Create layout
        form_layout = QVBoxLayout()
        area_dept_cod_layout = QHBoxLayout()
        area_dept_cod_layout.addWidget(area_dept_cod_label)
        area_dept_cod_layout.addWidget(self.area_dept_cod_edit)
        user_cod_layout = QHBoxLayout()
        user_cod_layout.addWidget(user_cod_label)
        user_cod_layout.addWidget(self.user_cod_edit)
        role_cod_layout = QHBoxLayout()
        role_cod_layout.addWidget(role_cod_label)
        role_cod_layout.addWidget(self.role_cod_edit)
        button_layout = QHBoxLayout()
        button_layout.addWidget(add_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(update_button)
        form_layout.addLayout(area_dept_cod_layout)
        form_layout.addLayout(user_cod_layout)
        form_layout.addLayout(role_cod_layout)
        form_layout.addLayout(button_layout)
        form_layout.addWidget(self.view)
        self.setLayout(form_layout)

    def populate_fields(self, index):
        row = index.row()
        record = self.model.record(row)
        area_dept_cod = record.value("AREA_DEPT_COD")
        user_cod = record.value("USER_COD")
        role_cod = record.value("ROLE_COD")
        self.area_dept_cod_edit.setText(str(area_dept_cod))
        self.user_cod_edit.setText(str(user_cod))
        self.role_cod_edit.setText(str(role_cod))

    def add_record(self):
        area_dept_cod = self.area_dept_cod_edit.text()
        user_cod = self.user_cod_edit.text()
        role_cod = self.role_cod_edit.text()
        if area_dept_cod and user_cod and role_cod:
            record = self.model.record()
            record.setValue("AREA_DEPT_COD", int(area_dept_cod))
            record.setValue("USER_COD", int(user_cod))
            record.setValue("ROLE_COD", int(role_cod))
            if self.model.insertRecord(-1, record):
                self.model.submitAll()
                self.area_dept_cod_edit.clear()
                self.user_cod_edit.clear()
                self.role_cod_edit.clear()
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
            area_dept_cod = self.area_dept_cod_edit.text()
            user_cod = self.user_cod_edit.text()
            role_cod = self.role_cod_edit.text()
            if area_dept_cod and user_cod and role_cod:
                record.setValue("AREA_DEPT_COD", int(area_dept_cod))
                record.setValue("USER_COD", int(user_cod))
                record.setValue("ROLE_COD", int(role_cod))
                if self.model.setRecord(row, record):
                    self.model.submitAll()
            else:
                QMessageBox.warning(None, "Warning", "Please fill in all fields")