from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QTableWidget, QTableWidgetItem, QGridLayout, QLabel, \
    QAbstractItemView, QHeaderView

from button_layout import ButtonLayout
from data import ProductManager
from popup_window import AddProductDialog, EditProductDialog


class ProductsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.pm = ProductManager()

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

        self.products_label = QLabel("Список продуктов")
        self.products_label.setStyleSheet("font-size: 32px; font-weight: bold; margin-bottom: 10px;")
        self.scroll_content_layout.addWidget(self.products_label, 0, 0, alignment=Qt.AlignHCenter)

        self.button_layout = ButtonLayout()
        self.button_layout.add_button.clicked.connect(self.add_product)
        self.button_layout.edit_button.clicked.connect(self.edit_product)
        self.button_layout.delete_button.clicked.connect(self.delete_product)
        self.scroll_content_layout.addLayout(self.button_layout, 1, 0, alignment=Qt.AlignHCenter)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(
            ["Название, 100 г.", "Белки, г.", "Жиры, г.", "Углеводы, г.", "Калории, ккал"]
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

        self.show_products()

    def adjust_table_size(self):
        self.table_widget.resizeRowsToContents()
        header_height = self.table_widget.horizontalHeader().height()
        row_height = 0
        for i in range(self.table_widget.rowCount()):
            row_height += self.table_widget.rowHeight(i)
        total_height = header_height + row_height
        self.table_widget.setMinimumHeight(total_height)

    def show_products(self):
        data = self.pm.get_products()
        self.table_widget.setRowCount(len(data))
        for row, record in enumerate(data):
            for col, item in enumerate(record):
                self.table_widget.setItem(row, col, QTableWidgetItem(str(item)))
        self.adjust_table_size()

    def add_product(self):
        self.add_window = AddProductDialog()
        self.add_window.add_button.clicked.connect(self.add_product_to_db)
        self.add_window.exec_()

    def add_product_to_db(self):
        name = self.add_window.name_edit.text()
        proteins = self.add_window.proteins_edit.value()
        fats = self.add_window.fats_edit.value()
        carbohydrates = self.add_window.carbohydrates_edit.value()
        calories = self.add_window.calories_edit.value()

        self.pm.add_product(name, proteins, fats, carbohydrates, calories)
        self.show_products()
        self.add_window.close()

    def edit_product(self):
        selected_row = self.table_widget.currentRow()
        if selected_row != -1:
            self.edit_window = EditProductDialog()
            self.edit_window.name_edit.setText(self.table_widget.item(selected_row, 0).text())
            self.edit_window.proteins_edit.setValue(int(self.table_widget.item(selected_row, 1).text()))
            self.edit_window.fats_edit.setValue(int(self.table_widget.item(selected_row, 2).text()))
            self.edit_window.carbohydrates_edit.setValue(int(self.table_widget.item(selected_row, 3).text()))
            self.edit_window.calories_edit.setValue(int(self.table_widget.item(selected_row, 4).text()))
            self.edit_window.edit_button.clicked.connect(lambda: self.edit_product_in_db(selected_row))
            self.edit_window.exec_()

    def edit_product_in_db(self, selected_row):
        name = self.edit_window.name_edit.text()
        proteins = self.edit_window.proteins_edit.value()
        fats = self.edit_window.fats_edit.value()
        carbohydrates = self.edit_window.carbohydrates_edit.value()
        calories = self.edit_window.calories_edit.value()

        if selected_row < self.table_widget.rowCount():
            self.pm.update_product(self.table_widget.item(selected_row, 0).text(),
                                   name, proteins, fats, carbohydrates, calories)
            self.show_products()
            self.edit_window.close()

    def delete_product(self):
        selected_rows = self.table_widget.selectionModel().selectedRows()
        for row in selected_rows:
            self.pm.delete_product(self.table_widget.item(row.row(), 0).text())
        self.show_products()
