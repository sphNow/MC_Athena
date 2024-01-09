import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QAction, QStackedWidget
from MC_Athena.form.my_form_area_dept import MyFormAreaDept
from MC_Athena.form.my_form_mailbox import MyFormMailbox
from MC_Athena.form.my_form_mailbox_alias import MyFormMailboxAlias
from MC_Athena.form.my_form_users import MyFormUsers
from MC_Athena.form.my_form_users_team import MyFormUsersTeam
from MC_Athena.form.my_form_categories import MyFormCategories
from MC_Athena.form.my_form_units import MyFormUnits
from MC_Athena.form.my_form_areadeptcategory import MyFormAreaDeptCategory
from MC_Athena.form.my_form_planned import MyFormPlanned

class MainAthenaVBA(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Athena VBA")

        # Create stacked widget to hold forms
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Create forms
        self.form_area_dept = MyFormAreaDept()
        self.form_mailbox = MyFormMailbox()
        self.form_mailbox_alias = MyFormMailboxAlias()
        self.form_users = MyFormUsers()
        self.form_users_team = MyFormUsersTeam()
        self.form_categories = MyFormCategories()
        self.form_units = MyFormUnits()
        self.form_areadeptcategory = MyFormAreaDeptCategory()
        self.form_planned = MyFormPlanned()
        self.stacked_widget.addWidget(self.form_area_dept)
        self.stacked_widget.addWidget(self.form_mailbox)
        self.stacked_widget.addWidget(self.form_mailbox_alias)
        self.stacked_widget.addWidget(self.form_users)
        self.stacked_widget.addWidget(self.form_users_team)
        self.stacked_widget.addWidget(self.form_categories)
        self.stacked_widget.addWidget(self.form_units)
        self.stacked_widget.addWidget(self.form_areadeptcategory)
        self.stacked_widget.addWidget(self.form_planned)

        # Create menu bar
        menu_bar = self.menuBar()

        # Create Teams menu
        teams_menu = QMenu("Teams", self)
        area_dept_action = QAction("Area_Dept", self)
        area_dept_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.form_area_dept))
        teams_menu.addAction(area_dept_action)
        mailbox_action = QAction("MailBox", self)
        mailbox_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.form_mailbox))
        teams_menu.addAction(mailbox_action)
        mailbox_alias_action = QAction("MailBox_Alias", self)
        mailbox_alias_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.form_mailbox_alias))
        teams_menu.addAction(mailbox_alias_action)
        menu_bar.addMenu(teams_menu)

        # Create Users menu
        users_menu = QMenu("Users", self)
        user_action = QAction("User", self)
        user_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.form_users))
        users_menu.addAction(user_action)
        user_team_action = QAction("User_Team", self)
        user_team_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.form_users_team))
        users_menu.addAction(user_team_action)
        menu_bar.addMenu(users_menu)

        # Create Tasks menu
        tasks_menu = QMenu("Tasks", self)
        categories_action = QAction("Categories", self)
        categories_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.form_categories))
        tasks_menu.addAction(categories_action)
        units_action = QAction("Units", self)
        units_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.form_units))
        tasks_menu.addAction(units_action)
        area_dept_category_action = QAction("Area_Dept_Category", self)
        area_dept_category_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.form_areadeptcategory))
        tasks_menu.addAction(area_dept_category_action)
        planned = QAction("Task Planned", self)
        planned.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.form_planned))
        tasks_menu.addAction(planned)
        menu_bar.addMenu(tasks_menu)



#if __name__ == "__main__":
    #    app = QApplication(sys.argv)
    #window = MainAthenaVBA()
    #window.show()
    #sys.exit(app.exec_())