from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableView, QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtCore import Qt

from config import dbAthena_Net

class MyFormMailbox(QWidget):
    def __init__(self):
        super().__init__()

        # Create database connection
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(dbAthena_Net)
        if not self.db.open():
            QMessageBox.critical(None, "Error", "Could not open database")

        # Create model and view
        self.model = QSqlTableModel()
        self.model.setTable("MAILBOX")
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()
        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.doubleClicked.connect(self.populate_fields)

        # Create form widgets
        mailbox_label = QLabel("Mailbox:")
        self.mailbox_edit = QLineEdit()
        email_label = QLabel("Email:")
        self.email_edit = QLineEdit()
        entry_inbox_label = QLabel("Entry Inbox:")
        self.entry_inbox_edit = QLineEdit()
        entry_draft_label = QLabel("Entry Draft:")
        self.entry_draft_edit = QLineEdit()
        entry_sent_label = QLabel("Entry Sent:")
        self.entry_sent_edit = QLineEdit()
        ddbb_data_file_label = QLabel("DDBB Data File:")
        self.ddbb_data_file_edit = QLineEdit()
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add_record)
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete_record)
        update_button = QPushButton("Update")
        update_button.clicked.connect(self.update_record)

        # Create layout
        form_layout = QVBoxLayout()
        mailbox_layout = QHBoxLayout()
        mailbox_layout.addWidget(mailbox_label)
        mailbox_layout.addWidget(self.mailbox_edit)
        email_layout = QHBoxLayout()
        email_layout.addWidget(email_label)
        email_layout.addWidget(self.email_edit)
        entry_inbox_layout = QHBoxLayout()
        entry_inbox_layout.addWidget(entry_inbox_label)
        entry_inbox_layout.addWidget(self.entry_inbox_edit)
        entry_draft_layout = QHBoxLayout()
        entry_draft_layout.addWidget(entry_draft_label)
        entry_draft_layout.addWidget(self.entry_draft_edit)
        entry_sent_layout = QHBoxLayout()
        entry_sent_layout.addWidget(entry_sent_label)
        entry_sent_layout.addWidget(self.entry_sent_edit)
        ddbb_data_file_layout = QHBoxLayout()
        ddbb_data_file_layout.addWidget(ddbb_data_file_label)
        ddbb_data_file_layout.addWidget(self.ddbb_data_file_edit)
        button_layout = QHBoxLayout()
        button_layout.addWidget(add_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(update_button)
        form_layout.addLayout(mailbox_layout)
        form_layout.addLayout(email_layout)
        form_layout.addLayout(entry_inbox_layout)
        form_layout.addLayout(entry_draft_layout)
        form_layout.addLayout(entry_sent_layout)
        form_layout.addLayout(ddbb_data_file_layout)
        form_layout.addLayout(button_layout)
        form_layout.addWidget(self.view)
        self.setLayout(form_layout)

    def populate_fields(self, index):
        row = index.row()
        record = self.model.record(row)
        mailbox = record.value("MAILBOX")
        email = record.value("EMAIL")
        entry_inbox = record.value("ENTRY_INBOX")
        entry_draft = record.value("ENTRY_DRAFT")
        entry_sent = record.value("ENTRY_SENT")
        ddbb_data_file = record.value("DDBB_DATA_FILE")
        self.mailbox_edit.setText(mailbox)
        self.email_edit.setText(email)
        self.entry_inbox_edit.setText(entry_inbox)
        self.entry_draft_edit.setText(entry_draft)
        self.entry_sent_edit.setText(entry_sent)
        self.ddbb_data_file_edit.setText(ddbb_data_file)

    def add_record(self):
        mailbox = self.mailbox_edit.text()
        email = self.email_edit.text()
        entry_inbox = self.entry_inbox_edit.text()
        entry_draft = self.entry_draft_edit.text()
        entry_sent = self.entry_sent_edit.text()
        ddbb_data_file = self.ddbb_data_file_edit.text()
        if mailbox and email and entry_inbox and entry_draft and entry_sent:
            record = self.model.record()
            record.setValue("MAILBOX", mailbox)
            record.setValue("EMAIL", email)
            record.setValue("ENTRY_INBOX", entry_inbox)
            record.setValue("ENTRY_DRAFT", entry_draft)
            record.setValue("ENTRY_SENT", entry_sent)
            record.setValue("DDBB_DATA_FILE", ddbb_data_file)
            if self.model.insertRecord(-1, record):
                self.model.submitAll()
                self.mailbox_edit.clear()
                self.email_edit.clear()
                self.entry_inbox_edit.clear()
                self.entry_draft_edit.clear()
                self.entry_sent_edit.clear()
                self.ddbb_data_file_edit.clear()
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
            mailbox = self.mailbox_edit.text()
            email = self.email_edit.text()
            entry_inbox = self.entry_inbox_edit.text()
            entry_draft = self.entry_draft_edit.text()
            entry_sent = self.entry_sent_edit.text()
            ddbb_data_file = self.ddbb_data_file_edit.text()
            if mailbox and email and entry_inbox and entry_draft and entry_sent:
                record.setValue("MAILBOX", mailbox)
                record.setValue("EMAIL", email)
                record.setValue("ENTRY_INBOX", entry_inbox)
                record.setValue("ENTRY_DRAFT", entry_draft)
                record.setValue("ENTRY_SENT", entry_sent)
                record.setValue("DDBB_DATA_FILE", ddbb_data_file)
                if self.model.setRecord(row, record):
                    self.model.submitAll()
            else:
                QMessageBox.warning(None, "Warning", "Please fill in all fields")