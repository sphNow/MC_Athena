from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableView, QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtCore import Qt
import pandas as pd

from config import dbAthena_Net

class MyFormPlanned(QWidget):
    def __init__(self):
        super().__init__()

        # Create database connection
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(dbAthena_Net)
        if not self.db.open():
            QMessageBox.critical(None, "Error", "Could not open database")

        # Create model and view
        self.model = QSqlTableModel()
        self.model.setTable("DUTY_PLANNED")
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()
        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.doubleClicked.connect(self.populate_fields)

        # Create form widgets
        area_dept_cat_cod_label = QLabel("Area Dept Cat Cod:")
        self.area_dept_cat_cod_edit = QLineEdit()
        turno_label = QLabel("Turno:")
        self.turno_edit = QLineEdit()
        desc_label = QLabel("Description:")
        self.desc_edit = QLineEdit()
        plann_cod_label = QLabel("Plann Cod:")
        self.plann_cod_edit = QLineEdit()
        unit_calendar_cod_label = QLabel("Unit Calendar Cod:")
        self.unit_calendar_cod_edit = QLineEdit()
        skip_holiday_label = QLabel("Skip Holiday:")
        self.skip_holiday_edit = QLineEdit()
        time_schedule_label = QLabel("Time Schedule:")
        self.time_schedule_edit = QLineEdit()
        plann_condition_label = QLabel("Plann Condition:")
        self.plann_condition_edit = QLineEdit()
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add_record)
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete_record)
        update_button = QPushButton("Update")
        update_button.clicked.connect(self.update_record)
        export_button = QPushButton("Export to Excel")
        export_button.clicked.connect(self.export_to_excel)

        # Create layout
        form_layout = QVBoxLayout()
        area_dept_cat_cod_layout = QHBoxLayout()
        area_dept_cat_cod_layout.addWidget(area_dept_cat_cod_label)
        area_dept_cat_cod_layout.addWidget(self.area_dept_cat_cod_edit)
        turno_layout = QHBoxLayout()
        turno_layout.addWidget(turno_label)
        turno_layout.addWidget(self.turno_edit)
        desc_layout = QHBoxLayout()
        desc_layout.addWidget(desc_label)
        desc_layout.addWidget(self.desc_edit)
        plann_cod_layout = QHBoxLayout()
        plann_cod_layout.addWidget(plann_cod_label)
        plann_cod_layout.addWidget(self.plann_cod_edit)
        unit_calendar_cod_layout = QHBoxLayout()
        unit_calendar_cod_layout.addWidget(unit_calendar_cod_label)
        unit_calendar_cod_layout.addWidget(self.unit_calendar_cod_edit)
        skip_holiday_layout = QHBoxLayout()
        skip_holiday_layout.addWidget(skip_holiday_label)
        skip_holiday_layout.addWidget(self.skip_holiday_edit)
        time_schedule_layout = QHBoxLayout()
        time_schedule_layout.addWidget(time_schedule_label)
        time_schedule_layout.addWidget(self.time_schedule_edit)
        plann_condition_layout = QHBoxLayout()
        plann_condition_layout.addWidget(plann_condition_label)
        plann_condition_layout.addWidget(self.plann_condition_edit)
        button_layout = QHBoxLayout()
        button_layout.addWidget(add_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(update_button)
        button_layout.addWidget(export_button)
        form_layout.addLayout(area_dept_cat_cod_layout)
        form_layout.addLayout(turno_layout)
        form_layout.addLayout(desc_layout)
        form_layout.addLayout(plann_cod_layout)
        form_layout.addLayout(unit_calendar_cod_layout)
        form_layout.addLayout(skip_holiday_layout)
        form_layout.addLayout(time_schedule_layout)
        form_layout.addLayout(plann_condition_layout)
        form_layout.addLayout(button_layout)
        form_layout.addWidget(self.view)
        self.setLayout(form_layout)

    def populate_fields(self, index):
        row = index.row()
        record = self.model.record(row)
        area_dept_cat_cod = record.value("AREA_DEPT_CAT_COD")
        turno = record.value("TURNO")
        desc = record.value("DESC")
        plann_cod = record.value("PLANN_COD")
        unit_calendar_cod = record.value("UNIT_CALENDAR_COD")
        skip_holiday = record.value("SKIP_HOLIDAY")
        time_schedule = record.value("TIME_SCHEDULE")
        plann_condition = record.value("PLANN_CONDITION")
        self.area_dept_cat_cod_edit.setText(str(area_dept_cat_cod))
        self.turno_edit.setText(str(turno))
        self.desc_edit.setText(desc)
        self.plann_cod_edit.setText(plann_cod)
        self.unit_calendar_cod_edit.setText(unit_calendar_cod)
        self.skip_holiday_edit.setText(skip_holiday)
        self.time_schedule_edit.setText(time_schedule)
        self.plann_condition_edit.setText(plann_condition)

    def add_record(self):
        area_dept_cat_cod = self.area_dept_cat_cod_edit.text()
        turno = self.turno_edit.text()
        desc = self.desc_edit.text()
        plann_cod = self.plann_cod_edit.text()
        unit_calendar_cod = self.unit_calendar_cod_edit.text()
        skip_holiday = self.skip_holiday_edit.text()
        time_schedule = self.time_schedule_edit.text()
        plann_condition = self.plann_condition_edit.text()
        if area_dept_cat_cod and desc and plann_cod:
            record = self.model.record()
            record.setValue("AREA_DEPT_CAT_COD", int(area_dept_cat_cod))
            record.setValue("TURNO", int(turno))
            record.setValue("DESC", desc)
            record.setValue("PLANN_COD", plann_cod)
            record.setValue("UNIT_CALENDAR_COD", unit_calendar_cod)
            record.setValue("SKIP_HOLIDAY", skip_holiday)
            record.setValue("TIME_SCHEDULE", time_schedule)
            record.setValue("PLANN_CONDITION", plann_condition)
            if self.model.insertRecord(-1, record):
                self.model.submitAll()
                self.area_dept_cat_cod_edit.clear()
                self.turno_edit.clear()
                self.desc_edit.clear()
                self.plann_cod_edit.clear()
                self.unit_calendar_cod_edit.clear()
                self.skip_holiday_edit.clear()
                self.time_schedule_edit.clear()
                self.plann_condition_edit.clear()
        else:
            QMessageBox.warning(None, "Warning", "Please fill in all required fields")

    def delete_record(self):
        row = self.view.currentIndex().row()
        if row >= 0:
            self.model.removeRow(row)
            self.model.submitAll()

    def update_record(self):
        row = self.view.currentIndex().row()
        if row >= 0:
            record = self.model.record(row)
            area_dept_cat_cod = self.area_dept_cat_cod_edit.text()
            turno = self.turno_edit.text()
            desc = self.desc_edit.text()
            plann_cod = self.plann_cod_edit.text()
            unit_calendar_cod = self.unit_calendar_cod_edit.text()
            skip_holiday = self.skip_holiday_edit.text()
            time_schedule = self.time_schedule_edit.text()
            plann_condition = self.plann_condition_edit.text()
            if area_dept_cat_cod and desc and plann_cod:
                record.setValue("AREA_DEPT_CAT_COD", int(area_dept_cat_cod))
                record.setValue("TURNO", int(turno))
                record.setValue("DESC", desc)
                record.setValue("PLANN_COD", plann_cod)
                record.setValue("UNIT_CALENDAR_COD", unit_calendar_cod)
                record.setValue("SKIP_HOLIDAY", skip_holiday)
                record.setValue("TIME_SCHEDULE", time_schedule)
                record.setValue("PLANN_CONDITION", plann_condition)
                if self.model.setRecord(row, record):
                    self.model.submitAll()
            else:
                QMessageBox.warning(None, "Warning", "Please fill in all required fields")

    def export_to_excel(self):
        # Get data from model
        df = pd.read_sql(self.model.query().lastQuery(), self.db)

        # Create Excel writer
        writer = pd.ExcelWriter("data.xlsx", engine="xlsxwriter")

        # Write data to Excel
        df.to_excel(writer, index=False)

        # Save Excel file
        writer.save()

        # Show success message
        QMessageBox.information(None, "Export to Excel", "Data exported to Excel successfully")