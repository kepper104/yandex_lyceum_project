from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QLabel
from app import File

class TabForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        # Form.setObjectName("Form")
        # Form.resize(1025, 489)
        self.tableWidget = QtWidgets.QTableWidget(self)
        self.tableWidget.setGeometry(QtCore.QRect(0, 10, 711, 471))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)

    def loadfile(self, name='empty.txt'):
        """
        Loads file hex view, defaults to empty file created in init.

        Parameters:
            self
            name (str): name of the file to open
        Returns:
            None
        """

        reader = File(name)
        res = reader.readfile()
        self.tableWidget.setColumnCount(16)
        self.tableWidget.setRowCount(len(res[1]))
        self.tableWidget.setHorizontalHeaderLabels(res[0])
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.setVerticalHeaderLabels(res[1])

        for index, i in enumerate(res[2]):
            for jndex, j in enumerate(i.split()):
                self.tableWidget.setItem(index, jndex, QTableWidgetItem(j))
        self.tableWidget.setCurrentCell(2, 2)
        print()
        print(res[2])

class ExampleTab(QWidget):
    def __init__(self):
        super().__init__()
        self.lbl = QLabel("")
        # self.lbl.setFont()
        self.lbl.move(20, 20)

class NewFileForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.setObjectName("Form")
        self.resize(360, 300)
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(30, 30, 311, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(28)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(20, 120, 321, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(40, 190, 281, 61))
        font = QtGui.QFont()
        font.setPointSize(26)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
