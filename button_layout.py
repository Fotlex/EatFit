from PyQt5 import QtWidgets, QtGui


class ButtonLayout(QtWidgets.QHBoxLayout):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSpacing(20)

        self.button_style = """
            QPushButton {
                background-color: #27263c;
                color: white;
                padding: 10px 20px;
                border: 2px solid #4d4d4d;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #4d4d4d;
            }
        """

        self.add_button = QtWidgets.QPushButton()
        self.add_button.setIcon(QtGui.QIcon(":/icons/resources/add.png"))
        self.add_button.setStyleSheet(self.button_style)
        self.addWidget(self.add_button)

        self.edit_button = QtWidgets.QPushButton()
        self.edit_button.setIcon(QtGui.QIcon(":/icons/resources/mini-edit.png"))
        self.edit_button.setStyleSheet(self.button_style)
        self.addWidget(self.edit_button)

        self.delete_button = QtWidgets.QPushButton()
        self.delete_button.setIcon(QtGui.QIcon(":/icons/resources/remove.png"))
        self.delete_button.setStyleSheet(self.button_style)
        self.addWidget(self.delete_button)
