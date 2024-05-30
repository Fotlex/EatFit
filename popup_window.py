from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QPushButton, QSpinBox, QComboBox, QLabel, QLineEdit, QCalendarWidget


class PopupWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowIcon(QIcon(":/icons/resources/logo.png"))
        self.setMinimumSize(400, 200)

        self.setStyleSheet("""
            * {
                background-color: #1b1b27;
                color: white;
            }
            QComboBox, QSpinBox, QLineEdit {
                background-color: #27263c;
                color: white;
                border: 2px solid #4d4d4d;
                border-radius: 5px;
                padding: 5px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 0px;
                height: 0px;
                visibility: hidden;
            }
            QPushButton {
                color: white;
                padding: 10px 20px;
                border: 2px solid #4d4d4d;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #4d4d4d;
            }
        """)

        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)


class AddDailyProductDialog(PopupWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить продукт")

        self.date_label = QLabel("Дата")
        self.product_label = QLabel("Продукт")
        self.amount_label = QLabel("Количество, г.")

        self.date_edit = QLineEdit()
        self.date_edit.setReadOnly(True)

        self.product_combo = QComboBox()

        self.amount_edit = QSpinBox()
        self.amount_edit.setRange(1, 10000)

        self.layout.addWidget(self.date_label, 0, 0)
        self.layout.addWidget(self.date_edit, 0, 1)
        self.layout.addWidget(self.product_label, 1, 0)
        self.layout.addWidget(self.product_combo, 1, 1)
        self.layout.addWidget(self.amount_label, 2, 0)
        self.layout.addWidget(self.amount_edit, 2, 1)

        self.add_button = QPushButton("Добавить")
        self.layout.addWidget(self.add_button, 3, 0, 1, 2)


class EditDailyProductDialog(PopupWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Изменить продукт")

        self.date_label = QLabel("Дата")
        self.product_label = QLabel("Продукт")
        self.amount_label = QLabel("Количество, г.")

        self.date_edit = QLineEdit()
        self.date_edit.setReadOnly(True)

        self.product_combo = QComboBox()

        self.amount_edit = QSpinBox()
        self.amount_edit.setRange(1, 10000)

        self.layout.addWidget(self.date_label, 0, 0)
        self.layout.addWidget(self.date_edit, 0, 1)
        self.layout.addWidget(self.product_label, 1, 0)
        self.layout.addWidget(self.product_combo, 1, 1)
        self.layout.addWidget(self.amount_label, 2, 0)
        self.layout.addWidget(self.amount_edit, 2, 1)

        self.edit_button = QPushButton("Изменить")
        self.layout.addWidget(self.edit_button, 3, 0, 1, 2)


class AddProductDialog(PopupWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить продукт")
        self.setMinimumSize(400, 300)

        self.name_label = QLabel("Название, 100 г.")
        self.proteins_label = QLabel("Белки, г.")
        self.fats_label = QLabel("Жиры, г.")
        self.carbohydrates_label = QLabel("Углеводы, г.")
        self.calories_label = QLabel("Калории, ккал.")

        self.name_edit = QLineEdit()
        self.proteins_edit = QSpinBox()
        self.proteins_edit.setRange(0, 10000)
        self.fats_edit = QSpinBox()
        self.fats_edit.setRange(0, 10000)
        self.carbohydrates_edit = QSpinBox()
        self.carbohydrates_edit.setRange(0, 10000)
        self.calories_edit = QSpinBox()
        self.calories_edit.setRange(0, 10000)

        self.layout.addWidget(self.name_label, 0, 0)
        self.layout.addWidget(self.name_edit, 0, 1)
        self.layout.addWidget(self.proteins_label, 1, 0)
        self.layout.addWidget(self.proteins_edit, 1, 1)
        self.layout.addWidget(self.fats_label, 2, 0)
        self.layout.addWidget(self.fats_edit, 2, 1)
        self.layout.addWidget(self.carbohydrates_label, 3, 0)
        self.layout.addWidget(self.carbohydrates_edit, 3, 1)
        self.layout.addWidget(self.calories_label, 4, 0)
        self.layout.addWidget(self.calories_edit, 4, 1)

        self.add_button = QPushButton("Добавить")
        self.layout.addWidget(self.add_button, 5, 0, 1, 2)


class EditProductDialog(PopupWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Изменить продукт")
        self.setMinimumSize(400, 300)

        self.name_label = QLabel("Название, 100 г.")
        self.proteins_label = QLabel("Белки, г.")
        self.fats_label = QLabel("Жиры, г.")
        self.carbohydrates_label = QLabel("Углеводы, г.")
        self.calories_label = QLabel("Калории, ккал.")

        self.name_edit = QLineEdit()
        self.proteins_edit = QSpinBox()
        self.proteins_edit.setRange(0, 10000)
        self.fats_edit = QSpinBox()
        self.fats_edit.setRange(0, 10000)
        self.carbohydrates_edit = QSpinBox()
        self.carbohydrates_edit.setRange(0, 10000)
        self.calories_edit = QSpinBox()
        self.calories_edit.setRange(0, 10000)

        self.layout.addWidget(self.name_label, 0, 0)
        self.layout.addWidget(self.name_edit, 0, 1)
        self.layout.addWidget(self.proteins_label, 1, 0)
        self.layout.addWidget(self.proteins_edit, 1, 1)
        self.layout.addWidget(self.fats_label, 2, 0)
        self.layout.addWidget(self.fats_edit, 2, 1)
        self.layout.addWidget(self.carbohydrates_label, 3, 0)
        self.layout.addWidget(self.carbohydrates_edit, 3, 1)
        self.layout.addWidget(self.calories_label, 4, 0)
        self.layout.addWidget(self.calories_edit, 4, 1)

        self.edit_button = QPushButton("Изменить")
        self.layout.addWidget(self.edit_button, 5, 0, 1, 2)


class DateSelector(PopupWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Выбрать дату")

        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)
        self.calendar.setFirstDayOfWeek(Qt.Monday)

        self.calendar.setStyleSheet("""
            QCalendarWidget QWidget {
                alternate-background-color: #27263c;
                color: white;
            }
            QCalendarWidget QAbstractItemView::section {
                background-color: #1b1b27;
                color: white;
                font-size: 10pt;
            }
            QCalendarWidget QAbstractItemView:disabled {
                color: gray;
            }
        """)

        self.select_button = QPushButton('Выбрать')

        self.layout.addWidget(self.calendar, 0, 0, 1, 2)
        self.layout.addWidget(self.select_button, 1, 0, 1, 2)
