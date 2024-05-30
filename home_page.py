import datetime

import numpy as np
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QTableWidget, \
    QTableWidgetItem, QGridLayout, QAbstractItemView, QHeaderView, QComboBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from button_layout import ButtonLayout
from data import DailyProductManager, ProductManager, UserDataManager
from popup_window import AddDailyProductDialog, EditDailyProductDialog


class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.dpm = DailyProductManager()
        self.pm = ProductManager()
        self.udm = UserDataManager()
        self.current_date = datetime.date.today().strftime('%Y-%m-%d')

        self.layout = QVBoxLayout(self)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_area.setWidget(self.scroll_content)
        self.layout.addWidget(self.scroll_area)
        self.setLayout(self.layout)

        self.scroll_content_layout = QGridLayout()
        self.scroll_content_layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.scroll_content.setLayout(self.scroll_content_layout)

        # Создание диаграммы
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setMinimumSize(400, 300)
        self.scroll_content_layout.addWidget(self.canvas, 0, 0, alignment=Qt.AlignHCenter)

        self.button_layout = ButtonLayout()
        self.button_layout.add_button.clicked.connect(self.add_daily_product)
        self.button_layout.edit_button.clicked.connect(self.edit_daily_product)
        self.button_layout.delete_button.clicked.connect(self.delete_daily_product)
        self.scroll_content_layout.addLayout(self.button_layout, 1, 0, alignment=Qt.AlignHCenter)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(7)
        self.table_widget.setHorizontalHeaderLabels(
            ["Дата", "Продукт", "Количество, г.", "Белки, г.", "Жиры, г.", "Углеводы, г.", "Калории, ккал."]
        )
        self.table_widget.setWordWrap(True)
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_widget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table_widget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table_widget.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.scroll_content_layout.addWidget(self.table_widget, 2, 0, alignment=Qt.AlignHCenter)

        self.table_widget.setStyleSheet("""
            QTableWidget {
                background-color: #1b1b27;
                color: white;
                gridline-color: white;
            }

            QTableWidget QHeaderView::section {
                background-color: #27263c;
                color: white;
                padding: 5px;
            }

            QTableWidget QTableCornerButton::section { 
                background-color: #2d2d46; 
            }
        """)

        self.show_daily_products()

    def show_daily_products(self):
        actual = [0, 0, 0, 0]
        data = self.dpm.get_daily_products(self.current_date)
        self.table_widget.setRowCount(len(data))
        for row, record in enumerate(data):
            for col, item in enumerate(record):
                self.table_widget.setItem(row, col, QTableWidgetItem(str(item)))
                if col > 2:
                    actual[col - 3] += item
        self.adjust_table_size()
        self.plot_chart(actual)

    def adjust_table_size(self):
        self.table_widget.resizeRowsToContents()
        header_height = self.table_widget.horizontalHeader().height()
        row_height = 0
        for i in range(self.table_widget.rowCount()):
            row_height += self.table_widget.rowHeight(i)
        total_height = header_height + row_height
        self.table_widget.setMinimumHeight(total_height)

    def add_daily_product(self):
        self.add_window = AddDailyProductDialog()
        self.add_window.date_edit.setText(self.current_date)
        products = [row[0] for row in self.pm.get_all_names_products()]
        self.add_window.product_combo.addItems(products)
        self.add_window.add_button.clicked.connect(self.add_daily_product_to_db)
        self.add_window.exec_()

    def add_daily_product_to_db(self):
        date = self.add_window.date_edit.text()
        product_name = self.add_window.product_combo.currentText()
        amount = self.add_window.amount_edit.value()

        product_id = self.pm.get_product_id(product_name)
        self.dpm.add_daily_product(date, product_id, amount)

        self.show_daily_products()
        self.add_window.close()

    def edit_daily_product(self):
        selected_row = self.table_widget.currentRow()
        if selected_row != -1:
            self.edit_window = EditDailyProductDialog()
            self.edit_window.date_edit.setText(self.table_widget.item(selected_row, 0).text())
            self.product_combo = QComboBox()
            products = [row[0] for row in self.pm.get_all_names_products()]
            self.edit_window.product_combo.addItems(products)
            self.edit_window.product_combo.setCurrentText(self.table_widget.item(selected_row, 1).text())
            self.edit_window.amount_edit.setValue(int(self.table_widget.item(selected_row, 2).text()))
            self.edit_window.edit_button.clicked.connect(lambda: self.edit_daily_product_in_db(selected_row))
            self.edit_window.exec_()

    def edit_daily_product_in_db(self, selected_row):
        date = self.edit_window.date_edit.text()
        product_name = self.edit_window.product_combo.currentText()
        amount = self.edit_window.amount_edit.value()
        product_id = self.pm.get_product_id(product_name)
        old_product_id = self.pm.get_product_id(self.table_widget.item(selected_row, 1).text())
        daily_product_id = self.dpm.get_daily_product(date, old_product_id)[0]
        self.dpm.edit_daily_product(daily_product_id, date, product_id, amount)

        self.show_daily_products()
        self.edit_window.close()

    def delete_daily_product(self):
        selected_rows = self.table_widget.selectionModel().selectedRows()
        for row in selected_rows:
            date = self.table_widget.item(row.row(), 0).text()
            product_name = self.table_widget.item(row.row(), 1).text()

            product_id = self.pm.get_product_id(product_name)
            daily_product_id = self.dpm.get_daily_product(date, product_id)[0]
            self.dpm.delete_daily_product(daily_product_id)

        self.show_daily_products()

    def plot_chart(self, actual):
        user = self.udm.get_user_info()

        recommended_calories = 10 * user[1] + 6.25 * user[0] - 5 * user[2] + 5
        recommended_proteins = recommended_calories / 4 * 0.3
        recommended_fats = recommended_calories / 9 * 0.3
        recommended_carbs = recommended_calories / 4 * 0.4

        self.figure.clear()
        self.figure.set_facecolor('#1b1b27')
        ax = self.figure.add_subplot(111)
        ax.set_facecolor('#1b1b27')

        x = np.arange(4)
        recommended = [recommended_proteins, recommended_fats, recommended_carbs, recommended_calories]
        width = 0.35

        actual_color = '#E8E8E8'
        recommended_color = '#cc5bce'
        ax.bar(x - width / 2, actual, width, label='Фактически съедено', color=actual_color)
        ax.bar(x + width / 2, recommended, width, label='Рекомендуемая норма', color=recommended_color)

        ax.set_ylim(0, max(actual[3], recommended_calories) + 300)
        ax.set_xticks(x)
        ax.set_xticklabels(['Белки, г.', 'Жиры, г.', 'Углеводы, г.', 'Калории, ккал.'], color='white')
        ax.legend(facecolor='#1b1b27', edgecolor='#1b1b27', labelcolor='white')
        ax.set_title(f'Потребление за {self.current_date}', color='white', fontsize=15, fontweight="bold")
        ax.tick_params(axis='both', colors='white')

        for spine in ax.spines.values():
            spine.set_edgecolor('white')

        for i, (act, rec) in enumerate(zip(actual, recommended)):
            ax.text(i - width / 2, act + 10, str(int(act)), ha='center', va='bottom', color=actual_color)
            ax.text(i + width / 2, rec + 10, str(int(rec)), ha='center', va='bottom', color=recommended_color)

        self.canvas.draw()

    def change_current_date(self, new_date):
        self.current_date = new_date
        self.show_daily_products()
