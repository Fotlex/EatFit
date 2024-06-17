import sys

from PyQt5.QtCore import Qt, QRegularExpression
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtWidgets import QApplication, QMainWindow

from data import UserDataManager
from home_page import HomePage
from interface import *
from popup_window import DateSelector
from products_page import ProductsPage


class EatFitApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setMinimumSize(1400, 800)

        self.home_page = HomePage()
        self.products_page = ProductsPage()
        self.udm = UserDataManager()
        self.stackedWidget.addWidget(self.home_page)
        self.stackedWidget.addWidget(self.products_page)
        self.stackedWidget.setCurrentIndex(0)

        self.toggleLeftMenuBtn.clicked.connect(self.toggle_left_menu)
        self.toggleRightMenuBtn.clicked.connect(self.toggle_right_menu)
        self.calendarBtn.clicked.connect(self.show_date_selector)
        self.homeBtn.clicked.connect(self.show_home_page)
        self.productsBtn.clicked.connect(self.show_products_page)
        self.saveUserDataBtn.clicked.connect(self.save_user_data)

        regex = QRegularExpression(r"^[1-9]\d{0,2}$")
        validator = QRegularExpressionValidator(regex, self)
        self.weightLineEdit.setValidator(validator)
        self.heightLineEdit.setValidator(validator)
        self.ageLineEdit.setValidator(validator)
        self.update_user_info_placeholders()

    def toggle_left_menu(self):
        left_menu_visible = not self.leftMenu.isVisible()
        self.leftMenu.setVisible(left_menu_visible)

    def toggle_right_menu(self):
        right_menu_visible = not self.rightMenu.isVisible()
        self.rightMenu.setVisible(right_menu_visible)

    def show_date_selector(self):
        self.date_selector = DateSelector()
        self.date_selector.select_button.clicked.connect(self.select_date)
        self.date_selector.exec_()

    def select_date(self):
        selected_date = self.date_selector.calendar.selectedDate()
        iso_date = selected_date.toString(Qt.ISODate)
        self.home_page.change_current_date(iso_date)
        self.date_selector.close()

    def show_home_page(self):
        self.stackedWidget.setCurrentIndex(0)
        self.home_page.show_daily_products()

    def show_products_page(self):
        self.stackedWidget.setCurrentIndex(1)
        self.products_page.show_products()

    def save_user_data(self):
        weight = self.weightLineEdit.text()
        height = self.heightLineEdit.text()
        age = self.ageLineEdit.text()
        self.udm.update_user_info(height, weight, age)
        self.update_user_info_placeholders()
        self.home_page.show_daily_products()

    def update_user_info_placeholders(self):
        self.weightLineEdit.clear()
        self.heightLineEdit.clear()
        self.ageLineEdit.clear()

        user = self.udm.get_user_info()
        age = user[2]
        age_text = "год" if age % 10 == 1 else "года" if age % 10 <= 4 else "лет"
        self.weightLineEdit.setPlaceholderText(f"Вес: {user[1]} кг.")
        self.heightLineEdit.setPlaceholderText(f"Рост: {user[0]} см.")
        self.ageLineEdit.setPlaceholderText(f"Возраст: {age} {age_text}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EatFitApp()
    window.show()
    sys.exit(app.exec())
