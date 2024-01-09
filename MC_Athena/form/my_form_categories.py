from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableView, QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtCore import Qt

from config import dbAthena_Net


class MyFormCategories(QWidget):
    def __init__(self):
        super().__init__()

        # Create database connection
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(dbAthena_Net)
        if not self.db.open():
            QMessageBox.critical(None, "Error", "Could not open database")

        # Create model and view
        self.model = QSqlTableModel()
        self.model.setTable("CATEGORY_DUTY")
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()
        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.doubleClicked.connect(self.populate_fields)

        # Create form widgets
        cat_1_label = QLabel("Category 1:")
        self.cat_1_edit = QLineEdit()
        cat_2_label = QLabel("Category 2:")
        self.cat_2_edit = QLineEdit()
        cat_3_label = QLabel("Category 3:")
        self.cat_3_edit = QLineEdit()
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add_record)
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete_record)
        update_button = QPushButton("Update")
        update_button.clicked.connect(self.update_record)

        # Create layout
        form_layout = QVBoxLayout()
        cat_1_layout = QHBoxLayout()
        cat_1_layout.addWidget(cat_1_label)
        cat_1_layout.addWidget(self.cat_1_edit)
        cat_2_layout = QHBoxLayout()
        cat_2_layout.addWidget(cat_2_label)
        cat_2_layout.addWidget(self.cat_2_edit)
        cat_3_layout = QHBoxLayout()
        cat_3_layout.addWidget(cat_3_label)
        cat_3_layout.addWidget(self.cat_3_edit)
        button_layout = QHBoxLayout()
        button_layout.addWidget(add_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(update_button)
        form_layout.addLayout(cat_1_layout)
        form_layout.addLayout(cat_2_layout)
        form_layout.addLayout(cat_3_layout)
        form_layout.addLayout(button_layout)
        form_layout.addWidget(self.view)
        self.setLayout(form_layout)

    def populate_fields(self, index):
        row = index.row()
        record = self.model.record(row)
        cat_1 = record.value("CAT_1")
        cat_2 = record.value("CAT_2")
        cat_3 = record.value("CAT_3")
        self.cat_1_edit.setText(cat_1)
        self.cat_2_edit.setText(cat_2)
        self.cat_3_edit.setText(cat_3)

    def add_record(self):
        cat_1 = self.cat_1_edit.text()
        cat_2 = self.cat_2_edit.text()
        cat_3 = self.cat_3_edit.text()
        if cat_1 and cat_2 and cat_3:
            record = self.model.record()
            record.setValue("CAT_1", cat_1)
            record.setValue("CAT_2", cat_2)
            record.setValue("CAT_3", cat_3)
            if self.model.insertRecord(-1, record):
                self.model.submitAll()
                self.cat_1_edit.clear()
                self.cat_2_edit.clear()
                self.cat_3_edit.clear()
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
            cat_1 = self.cat_1_edit.text()
            cat_2 = self.cat_2_edit.text()
            cat_3 = self.cat_3_edit.text()
            if cat_1 and cat_2 and cat_3:
                record.setValue("CAT_1", cat_1)
                record.setValue("CAT_2", cat_2)
                record.setValue("CAT_3", cat_3)
                if self.model.setRecord(row, record):
                    self.model.submitAll()
            else:
                QMessageBox.warning(None, "Warning", "Please fill in all fields")