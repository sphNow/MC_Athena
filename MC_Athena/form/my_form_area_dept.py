from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableView, QMessageBox, QComboBox
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from config import dbAthena_Net

class MyFormAreaDept(QWidget):
    def __init__(self):
        super().__init__()

        # Create database connection
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(dbAthena_Net)
        if not self.db.open():
            QMessageBox.critical(None, "Error", "Could not open database")

        # Create model and view
        self.model = QSqlTableModel()
        self.model.setTable("AREA_DEPT")
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()
        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.doubleClicked.connect(self.populate_fields)

        # Create form widgets
        area_label = QLabel("Area:")
        self.area_edit = QLineEdit()
        dept_label = QLabel("Dept:")
        self.dept_edit = QLineEdit()
        mailbox_label = QLabel("Mailbox:")
        self.mailbox_combo = QComboBox()
        self.populate_mailbox_combo()
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add_record)
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete_record)
        update_button = QPushButton("Update")
        update_button.clicked.connect(self.update_record)

        # Create layout
        form_layout = QVBoxLayout()
        area_layout = QHBoxLayout()
        area_layout.addWidget(area_label)
        area_layout.addWidget(self.area_edit)
        dept_layout = QHBoxLayout()
        dept_layout.addWidget(dept_label)
        dept_layout.addWidget(self.dept_edit)
        mailbox_layout = QHBoxLayout()
        mailbox_layout.addWidget(mailbox_label)
        mailbox_layout.addWidget(self.mailbox_combo)
        button_layout = QHBoxLayout()
        button_layout.addWidget(add_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(update_button)
        form_layout.addLayout(area_layout)
        form_layout.addLayout(dept_layout)
        form_layout.addLayout(mailbox_layout)
        form_layout.addLayout(button_layout)
        form_layout.addWidget(self.view)
        self.setLayout(form_layout)

    def populate_mailbox_combo(self):
        query = QSqlQuery("SELECT MAILBOX_COD, MAILBOX FROM MAILBOX")
        while query.next():
            mailbox_cod = query.value(0)
            mailbox = query.value(1)
            self.mailbox_combo.addItem(mailbox, mailbox_cod)

    def populate_fields(self, index):
        row = index.row()
        record = self.model.record(row)
        area = record.value("AREA")
        dept = record.value("DEPT")
        mailbox_cod = record.value("MAILBOX_COD")
        self.area_edit.setText(area)
        self.dept_edit.setText(dept)
        index = self.mailbox_combo.findData(mailbox_cod)
        if index >= 0:
            self.mailbox_combo.setCurrentIndex(index)

    def add_record(self):
        area = self.area_edit.text()
        dept = self.dept_edit.text()
        mailbox_cod = self.mailbox_combo.currentData()
        if area and dept and mailbox_cod is not None:
            record = self.model.record()
            record.setValue("AREA", area)
            record.setValue("DEPT", dept)
            record.setValue("MAILBOX_COD", mailbox_cod)
            if self.model.insertRecord(-1, record):
                self.model.submitAll()
                self.area_edit.clear()
                self.dept_edit.clear()
                self.mailbox_combo.setCurrentIndex(0)
        else:
            QMessageBox.warning(None, "Warning", "Please enter an area, department, and mailbox")

    def delete_record(self):
        row = self.view.currentIndex().row()
        if row >= 0:
            self.model.removeRow(row)
            self.model.submitAll()

    def update_record(self):
        row = self.view.currentIndex().row()
        if row >= 0:
            record = self.model.record(row)
            area = self.area_edit.text()
            dept = self.dept_edit.text()
            mailbox_cod = self.mailbox_combo.currentData()
            if area and dept and mailbox_cod is not None:
                record.setValue("AREA", area)
                record.setValue("DEPT", dept)
                record.setValue("MAILBOX_COD", mailbox_cod)
                if self.model.setRecord(row, record):
                    self.model.submitAll()
            else:
                QMessageBox.warning(None, "Warning", "Please enter an area, department, and mailbox")