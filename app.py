import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QFileDialog


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        with open("empty.txt", 'w') as f:
            pass
        uic.loadUi('design.ui', self)
        self.loadFile()
    def loadFile(self, name='empty.txt'):
        reader = Reader(name)
        res = reader.printout()
        self.tableWidget.setColumnCount(16)
        self.tableWidget.setRowCount(len(res[1]))
        self.tableWidget.setHorizontalHeaderLabels(res[0])
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.setVerticalHeaderLabels(res[1])

        for index, i in enumerate(res[2]):
            for jndex, j in enumerate(i.split()):
                self.tableWidget.setItem(index, jndex, QTableWidgetItem(j))

        self.pushButton_2.clicked.connect(self.openFile)
        print()
        print(res[2])
    def openFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Select file', '')[0]
        self.loadFile(fname)
def next_line():
    cur = 0
    while True:
        yield (str(hex(cur))[2:].rjust(5, '0').ljust(6, '0'))
        cur += 1


class Reader:
    def __init__(self, file_name):
        self.file_name = file_name
    def printout(self):
        collected = ''
        headers_h = []
        headers_v = []
        nums = []
        print("          ", end='')
        for i in range(0, 16):
            headers_h.append(str(hex(i))[2:].rjust(2, '0'))
            print(str(hex(i))[2:].rjust(2, '0'), end=' ')
        print()
        print()

        n = next_line()
        a = next(n)
        headers_v.append(a)
        print(a, end='    ')

        f = open(self.file_name, 'rb')
        count = 0
        line = ""
        for i in f.read():
            letter = str(hex(i))[2:].rjust(2, '0')
            line += letter + " "
            print(letter, end=' ')
            if count < 15:
                collected += chr(i)
                count += 1
            else:
                nums.append(line)
                # print("line: ", line)
                line = ""
                collected += chr(i)
                print('    ', end='')
                for letter in collected:
                    if letter.isprintable():
                        print(letter, end='')
                    else:
                        print('.', end='')
                print()
                collected = ''
                # print()
                a = next(n)
                headers_v.append(a)
                print(a, end='    ')

                count = 0
        nums.append(line)
        print(' ' * (4 + ((16 - len(collected)) * 3)), end='')

        for letter in collected:
            if letter.isprintable():
                print(letter, end='')
            else:
                print('.', end='')
        f.close()
        # print()
        # print(nums)
        return headers_h, headers_v, nums




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())