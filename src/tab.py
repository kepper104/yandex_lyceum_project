from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QTableWidget, QLabel

from file import File
from utils import show_error, next_line


class TabForm(QWidget):
    def __init__(self, file_name='empty.txt', app=None):
        """
        Inits new window, all variables and creates file instance it will be working on.

        Parameters:
            self
            file_name (str): name of file bound to this tab
            app (App): parent app window

        Returns:
            None
        """

        super().__init__()
        self.isExampleTab = False
        self.is_loading = False
        self.app = app
        self.file = File(file_name, app)
        self.setup_ui()
        self.load_file()

    def setup_ui(self):
        """
        Creates both tables and sets all their attributes using code.

        Parameters:
            self

        Returns:
            None
        """
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(QtCore.QRect(0, 10, 700, 471))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(15)
        self.tableWidget.setFont(font)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(9999)
        self.tableWidget.setStyleSheet("selection-background-color: rgb(85, 170, 255);")

        self.tableWidget_2 = QTableWidget(self)
        self.tableWidget_2.setGeometry(QtCore.QRect(710, 10, 530, 471))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(15)

        self.tableWidget_2.setFont(font)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(16)
        self.tableWidget_2.setRowCount(9999)
        self.tableWidget_2.resizeColumnsToContents()
        self.tableWidget_2.setStyleSheet("selection-background-color: rgb(85, 170, 255);")
        self.tableWidget_2.setEditTriggers(QTableWidget.NoEditTriggers)

    def load_file(self):
        """
        Loads file hex view, defaults to empty file created in init.

        Parameters:
            self

        Returns:
            None
        """
        headers_h, cur_cells, letter_cells = self.file.get_data()
        headers_len = len(cur_cells)
        if headers_len <= 1:
            headers_len = 1000
        headers_v = []
        n = next_line()

        for i in range(headers_len):
            headers_v.append(next(n))

        self.tableWidget.setColumnCount(16)
        self.tableWidget.setRowCount(headers_len)
        self.tableWidget_2.setRowCount(headers_len)
        self.tableWidget.setHorizontalHeaderLabels(headers_h)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.setVerticalHeaderLabels(headers_v)

        for row, i in enumerate(cur_cells):
            for col, j in enumerate(i):
                self.tableWidget.setItem(row, col, QTableWidgetItem(j))

        self.tableWidget.setCurrentCell(2, 2)
        self.tableWidget.cellChanged.connect(self.on_cell_edited)

        self.tableWidget.cellClicked.connect(self.on_cell_clicked)
        self.tableWidget_2.cellClicked.connect(self.on_cell_clicked)

        for index, i in enumerate(letter_cells):
            self.tableWidget_2.setItem(index // 16, index % 16, QTableWidgetItem(i))

    def reload_file(self):
        """
        Creates both tables and sets all their attributes using code.

        Parameters:
            self

        Returns:
            None
        """
        headers_h, cur_cells, letter_cells = self.file.get_data()

        self.is_loading = True

        for row, i in enumerate(cur_cells):
            for col, j in enumerate(i):
                self.tableWidget.setItem(row, col, QTableWidgetItem(j))

        for index, i in enumerate(letter_cells):
            self.tableWidget_2.setItem(index // 16, index % 16, QTableWidgetItem(i))

        self.is_loading = False

    def on_cell_edited(self, row, col):
        """
        Cell edited event handling

        Parameters:
            self
            row (int): row of edited cell
            col (int): column of edited cell

        Returns:
            None
        """
        if not self.is_loading:
            new_item = self.tableWidget.item(row, col).text()

            try:
                from_hex = int(new_item, 16)
                item = self.file.cur_cells[row][col]
                self.file.change_file(row, col, new_item)
                self.reload_file()

            except IndexError:
                self.file.expand_cells(row, col)
                self.file.change_file(row, col, new_item)
                self.reload_file()

            except ValueError:
                show_error(self.app,
                           "Input Error!",
                           "You hex number is not valid!",
                           "Reverting to previous cell value")

                self.tableWidget.setItem(row, col, QTableWidgetItem(self.file.cur_cells[row][col]))

    def on_cell_clicked(self, row, col):
        """
        Cell clicked event handling: select same cell in both tables

        Parameters:
            self
            row (int): row of selected cell
            col (int): column of selected cell

        Returns:
            None
        """
        self.tableWidget.setCurrentCell(row, col)
        self.tableWidget_2.setCurrentCell(row, col)


class ExampleTab(QWidget):
    def __init__(self):
        super().__init__()
        self.isExampleTab = True
        self.init_ui()

    def init_ui(self):
        """
        Home tab auto generated UI

        Parameters:
            self
        Returns:
            None
        """

        self.resize(490, 140)
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 481, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label.setText("Добро пожаловать в Yandex Hex!")
