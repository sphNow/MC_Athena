from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableView, QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtCore import Qt

from config import dbAthena_Net

class MyFormUnits(QWidget):
    def __init__(self):
        super().__init__()

        # Create database connection
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(dbAthena_Net)
        if not self.db.open():
            QMessageBox.critical(None, "Error", "Could not open database")

        # Create model and view
        self.model = QSqlTableModel()
        self.model.setTable("UNIT")
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()
        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.doubleClicked.connect(self.populate_fields)

        # Create form widgets
        unit_label = QLabel("Unit:")
        self.unit_edit = QLineEdit()
        country_label = QLabel("Country:")
        self.country_edit = QLineEdit()
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add_record)
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete_record)
        update_button = QPushButton("Update")
        update_button.clicked.connect(self.update_record)

        # Create layout
        form_layout = QVBoxLayout()
        unit_layout = QHBoxLayout()
        unit_layout.addWidget(unit_label)
        unit_layout.addWidget(self.unit_edit)
        country_layout = QHBoxLayout()
        country_layout.addWidget(country_label)
        country_layout.addWidget(self.country_edit)
        button_layout = QHBoxLayout()
        button_layout.addWidget(add_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(update_button)
        form_layout.addLayout(unit_layout)
        form_layout.addLayout(country_layout)
        form_layout.addLayout(button_layout)
        form_layout.addWidget(self.view)
        self.setLayout(form_layout)

    def populate_fields(self, index):
        row = index.row()
        record = self.model.record(row)
        unit = record.value("UNIT")
        country = record.value("COUNTRY")
        self.unit_edit.setText(unit)
        self.country_edit.setText(country)

    def add_record(self):
        unit = self.unit_edit.text()
        country = self.country_edit.text()
        if unit and country:
            record = self.model.record()
            record.setValue("UNIT", unit)
            record.setValue("COUNTRY", country)
            if self.model.insertRecord(-1, record):
                self.model.submitAll()
                self.unit_edit.clear()
                self.country_edit.clear()
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
            unit = self.unit_edit.text()
            country = self.country_edit.text()
            if unit and country:
                record.setValue("UNIT", unit)
                record.setValue("COUNTRY", country)
                if self.model.setRecord(row, record):
                    self.model.submitAll()
            else:
                QMessageBox.warning(None, "Warning", "Please fill in all fields")