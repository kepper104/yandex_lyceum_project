from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QLabel
from app import File

def next_line():
    cur = 0
    while True:
        yield str(hex(cur))[2:].rjust(5, '0').ljust(6, '0')
        cur += 1


class TabForm(QWidget):
    def __init__(self, file_name='empty.txt', app=None):
        super().__init__()
        self.isExampleTab = False
        self.is_loading = False
        self.app = app
        self.file = File(file_name, app)
        self.setupUi()
        self.loadfile()

    def setupUi(self):
        self.tableWidget = QtWidgets.QTableWidget(self)
        self.tableWidget.setGeometry(QtCore.QRect(0, 10, 700, 471))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(15)
        self.tableWidget.setFont(font)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setStyleSheet("selection-background-color: rgb(85, 170, 255);")

        self.tableWidget_2 = QtWidgets.QTableWidget(self)
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


    def loadfile(self):
        """
        Loads file hex view, defaults to empty file created in init.

        Parameters:
            self
            name (str): name of the file to open
            parent_tab (TabForm): parent tab
        Returns:
            None
        """
        print("load")

        # res = self.file.readfile()
        headers_h, cur_cells, letter_cells = self.file.get_data()
        self.tableWidget.setColumnCount(16)
        headers_len = len(cur_cells)
        if headers_len <= 1:
            headers_len = 1000
        headers_v = []
        n = next_line()
        for i in range(headers_len):
            headers_v.append(next(n))
        self.tableWidget.setRowCount(headers_len)
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

        print("loaded")
    def reload_file(self):
        print("reload")

        # res = self.file.readfile()
        headers_h, cur_cells, letter_cells = self.file.get_data()
        print("wow:", letter_cells)
        print("reload")
        self.is_loading = True
        for row, i in enumerate(cur_cells):
            for col, j in enumerate(i):
                self.tableWidget.setItem(row, col, QTableWidgetItem(j))
        print("here")

        for index, i in enumerate(letter_cells):
            self.tableWidget_2.setItem(index // 16, index % 16, QTableWidgetItem(i))
        self.is_loading = False
        print("reloaded")
    def on_cell_edited(self, row, col):
        if not self.is_loading:
            new_item = self.tableWidget.item(row, col).text()
            self.file.change_file(row, col, new_item)
            self.reload_file()
    def on_cell_clicked(self, row, col):
        self.tableWidget.setCurrentCell(row, col)
        self.tableWidget_2.setCurrentCell(row, col)
        print(row, col)


class ExampleTab(QWidget):
    def __init__(self):
        super().__init__()
        self.isExampleTab = True
        self.initUI()

    def initUI(self):
        self.resize(490, 140)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 481, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label.setText("Добро пожаловать в Yandex Hex!")

