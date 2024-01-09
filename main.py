# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys

from PyQt5.QtWidgets import QApplication
from MC_Athena.my_athena_vba import MainAthenaVBA
## from MC_Athena.my_pqty_test import my_pqty_test
## from MC_Athena.my_pqty_test_BU import my_pqty_test_BU


def main():
    app = QApplication(sys.argv)
    ex = MainAthenaVBA()
    ex.show()
    sys.exit(app.exec_())

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
