import sys

from PyQt5.QtGui import QIcon

from interface import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtSql import QSqlTableModel


class EatFitApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("EatFit")
        self.setWindowIcon(QIcon(":/icons/resources/logo.png"))

        self.toggleLeftMenuBtn.clicked.connect(self.toggle_left_menu)
        self.toggleRightMenuBtn.clicked.connect(self.toggle_right_menu)
        self.homeBtn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.productsBtn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))

    def toggle_left_menu(self):
        left_menu_visible = not self.leftMenu.isVisible()
        self.leftMenu.setVisible(left_menu_visible)

    def toggle_right_menu(self):
        right_menu_visible = not self.rightMenu.isVisible()
        self.rightMenu.setVisible(right_menu_visible)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EatFitApp()
    window.show()
    sys.exit(app.exec())
