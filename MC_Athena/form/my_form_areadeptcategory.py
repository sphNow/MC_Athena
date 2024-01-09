from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableView, QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtCore import Qt

from config import dbAthena_Net

class MyFormAreaDeptCategory(QWidget):
    def __init__(self):
        super().__init__()

        # Create database connection
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(dbAthena_Net)
        if not self.db.open():
            QMessageBox.critical(None, "Error", "Could not open database")

        # Create model and view
        self.model = QSqlTableModel()
        self.model.setTable("AREA_UNIT_CATEGORY")
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()
        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.doubleClicked.connect(self.populate_fields)

        # Create form widgets
        area_dept_cod_label = QLabel("Area Dept Cod:")
        self.area_dept_cod_edit = QLineEdit()
        unit_cod_label = QLabel("Unit Cod:")
        self.unit_cod_edit = QLineEdit()
        cat_cod_label = QLabel("Cat Cod:")
        self.cat_cod_edit = QLineEdit()
        pos_order_label = QLabel("Pos Order:")
        self.pos_order_edit = QLineEdit()
        mpu_label = QLabel("MPU:")
        self.mpu_edit = QLineEdit()
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
        unit_cod_layout = QHBoxLayout()
        unit_cod_layout.addWidget(unit_cod_label)
        unit_cod_layout.addWidget(self.unit_cod_edit)
        cat_cod_layout = QHBoxLayout()
        cat_cod_layout.addWidget(cat_cod_label)
        cat_cod_layout.addWidget(self.cat_cod_edit)
        pos_order_layout = QHBoxLayout()
        pos_order_layout.addWidget(pos_order_label)
        pos_order_layout.addWidget(self.pos_order_edit)
        mpu_layout = QHBoxLayout()
        mpu_layout.addWidget(mpu_label)
        mpu_layout.addWidget(self.mpu_edit)
        button_layout = QHBoxLayout()
        button_layout.addWidget(add_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(update_button)
        form_layout.addLayout(area_dept_cod_layout)
        form_layout.addLayout(unit_cod_layout)
        form_layout.addLayout(cat_cod_layout)
        form_layout.addLayout(pos_order_layout)
        form_layout.addLayout(mpu_layout)
        form_layout.addLayout(button_layout)
        form_layout.addWidget(self.view)
        self.setLayout(form_layout)

    def populate_fields(self, index):
        row = index.row()
        record = self.model.record(row)
        area_dept_cod = record.value("AREA_DEPT_COD")
        unit_cod = record.value("UNIT_COD")
        cat_cod = record.value("CAT_COD")
        pos_order = record.value("POS_ORDER")
        mpu = record.value("MPU")
        self.area_dept_cod_edit.setText(str(area_dept_cod))
        self.unit_cod_edit.setText(str(unit_cod))
        self.cat_cod_edit.setText(str(cat_cod))
        self.pos_order_edit.setText(str(pos_order))
        self.mpu_edit.setText(str(mpu))

    def add_record(self):
        area_dept_cod = self.area_dept_cod_edit.text()
        unit_cod = self.unit_cod_edit.text()
        cat_cod = self.cat_cod_edit.text()
        pos_order = self.pos_order_edit.text()
        mpu = self.mpu_edit.text()
        if area_dept_cod and unit_cod and cat_cod:
            record = self.model.record()
            record.setValue("AREA_DEPT_COD", int(area_dept_cod))
            record.setValue("UNIT_COD", int(unit_cod))
            record.setValue("CAT_COD", int(cat_cod))
            record.setValue("POS_ORDER", int(pos_order))
            record.setValue("MPU", int(mpu))
            if self.model.insertRecord(-1, record):
                self.model.submitAll()
                self.area_dept_cod_edit.clear()
                self.unit_cod_edit.clear()
                self.cat_cod_edit.clear()
                self.pos_order_edit.clear()
                self.mpu_edit.clear()
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
            unit_cod = self.unit_cod_edit.text()
            cat_cod = self.cat_cod_edit.text()
            pos_order = self.pos_order_edit.text()
            mpu = self.mpu_edit.text()
            if area_dept_cod and unit_cod and cat_cod:
                record.setValue("AREA_DEPT_COD", int(area_dept_cod))
                record.setValue("UNIT_COD", int(unit_cod))
                record.setValue("CAT_COD", int(cat_cod))
                record.setValue("POS_ORDER", int(pos_order))
                record.setValue("MPU", int(mpu))
                if self.model.setRecord(row, record):
                    self.model.submitAll()
            else:
                QMessageBox.warning(None, "Warning", "Please fill in all fields")