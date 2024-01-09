from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableView, QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtCore import Qt

from config import dbAthena_Net

class MyFormMailboxAlias(QWidget):
    def __init__(self):
        super().__init__()

        # Create database connection
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(dbAthena_Net)
        if not self.db.open():
            QMessageBox.critical(None, "Error", "Could not open database")

        # Create model and view
        self.model = QSqlTableModel()
        self.model.setTable("MAILBOX_ALIAS")
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()
        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.doubleClicked.connect(self.populate_fields)

        # Create form widgets
        mailbox_cod_label = QLabel("Mailbox Cod:")
        self.mailbox_cod_edit = QLineEdit()
        alias_desc_label = QLabel("Alias Description:")
        self.alias_desc_edit = QLineEdit()
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add_record)
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete_record)
        update_button = QPushButton("Update")
        update_button.clicked.connect(self.update_record)

        # Create layout
        form_layout = QVBoxLayout()
        mailbox_cod_layout = QHBoxLayout()
        mailbox_cod_layout.addWidget(mailbox_cod_label)
        mailbox_cod_layout.addWidget(self.mailbox_cod_edit)
        alias_desc_layout = QHBoxLayout()
        alias_desc_layout.addWidget(alias_desc_label)
        alias_desc_layout.addWidget(self.alias_desc_edit)
        button_layout = QHBoxLayout()
        button_layout.addWidget(add_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(update_button)
        form_layout.addLayout(mailbox_cod_layout)
        form_layout.addLayout(alias_desc_layout)
        form_layout.addLayout(button_layout)
        form_layout.addWidget(self.view)
        self.setLayout(form_layout)

    def populate_fields(self, index):
        row = index.row()
        record = self.model.record(row)
        mailbox_cod = record.value("MAILBOX_COD")
        alias_desc = record.value("ALIAS_DESC")
        self.mailbox_cod_edit.setText(str(mailbox_cod))
        self.alias_desc_edit.setText(alias_desc)

    def add_record(self):
        mailbox_cod = self.mailbox_cod_edit.text()
        alias_desc = self.alias_desc_edit.text()
        if mailbox_cod and alias_desc:
            record = self.model.record()
            record.setValue("MAILBOX_COD", int(mailbox_cod))
            record.setValue("ALIAS_DESC", alias_desc)
            if self.model.insertRecord(-1, record):
                self.model.submitAll()
                self.mailbox_cod_edit.clear()
                self.alias_desc_edit.clear()
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
            mailbox_cod = self.mailbox_cod_edit.text()
            alias_desc = self.alias_desc_edit.text()
            if mailbox_cod and alias_desc:
                record.setValue("MAILBOX_COD", int(mailbox_cod))
                record.setValue("ALIAS_DESC", alias_desc)
                if self.model.setRecord(row, record):
                    self.model.submitAll()
            else:
                QMessageBox.warning(None, "Warning", "Please fill in all fields")