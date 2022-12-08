import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QFileDialog


def next_line():
    cur = 0
    while True:
        yield (str(hex(cur))[2:].rjust(5, '0').ljust(6, '0'))
        cur += 1


class App(QMainWindow):
    """
    Main class, contains all gui related things.
    """

    def __init__(self):
        """
        Is called only on program start and loads ui from design.ui
        By default generates an empty file
        Parameters:
            self
        Returns:
            None
        """

        super().__init__()
        with open("empty.txt", 'w') as f:
            pass
        uic.loadUi('design.ui', self)
        self.loadfile()

    def loadfile(self, name='empty.txt'):
        """
        Loads file hex view, defaults to empty file created in init.

        Parameters:
            self
            name (str): name of the file to open
        Returns:
            None
        """

        reader = Editor(name)
        res = reader.readfile()
        self.tableWidget.setColumnCount(16)
        self.tableWidget.setRowCount(len(res[1]))
        self.tableWidget.setHorizontalHeaderLabels(res[0])
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.setVerticalHeaderLabels(res[1])

        for index, i in enumerate(res[2]):
            for jndex, j in enumerate(i.split()):
                self.tableWidget.setItem(index, jndex, QTableWidgetItem(j))

        self.pushButton_2.clicked.connect(self.openfile)
        print()
        print(res[2])

    def openfile(self):
        """
        Prompts user to open a file and calls loadfile with inputted file name.

        Parameters:
            self
        Returns:
            None
        """

        file_name = QFileDialog.getOpenFileName(self, 'Select file', '')[0]
        self.loadfile(file_name)

    def stuff(self):
        self.loadfile()


class Editor:
    """
    Main editor class, handles reading files, editing files ...
    """

    def __init__(self, file_name):
        """
        Sets file_name that is being edited

        Parameters:
            self
            file_name (str): name of file edited

        Returns:
            None
        """
        self.file_name = file_name

    def printout(self):
        """
        Legacy function from a non gui hex reader, prints out hex view of file to terminal

        Parameters:
            self
        Returns:
            None
        """
        collected = ''

        print("          ", end='')
        for i in range(0, 16):
            print(str(hex(i))[2:].rjust(2, '0'), end=' ')
        print()
        print()

        n = next_line()
        a = next(n)
        print(a, end='    ')

        f = open(self.file_name, 'rb')
        count = 0

        # reading file symbol by symbol
        for i in f.read():
            letter = str(hex(i))[2:].rjust(2, '0')

            print(letter, end=' ')
            if count < 15:
                collected += chr(i)
                count += 1
            else:
                # print("line: ", line)

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
                print(a, end='    ')
                count = 0

        print(' ' * (4 + ((16 - len(collected)) * 3)), end='')

        for letter in collected:
            if letter.isprintable():
                print(letter, end='')
            else:
                print('.', end='')
        f.close()

    def readfile(self):
        """
        Function that reads edited file in hex, returns its contents to loadfile function from App class

        Parameters:
            self
        Returns:
            None
        """

        collected = ''
        cur_line = ""
        count = 0

        # stuff to return
        headers_h = []
        headers_v = []
        nums = []

        # horizontal headers
        for i in range(0, 16):
            headers_h.append(str(hex(i))[2:].rjust(2, '0'))

        # first vertical headers
        n = next_line()
        a = next(n)
        headers_v.append(a)

        # opening file itself
        f = open(self.file_name, 'rb')

        # reading file symbol by symbol
        for i in f.read():
            letter = str(hex(i))[2:].rjust(2, '0')
            cur_line += letter + " "
            # first 15 symbols are read as usual
            if count < 15:
                collected += chr(i)
                count += 1
            # for last symbol we write it to current line and add whole line to returned nums array
            else:
                nums.append(cur_line)
                cur_line = ""
                collected += chr(i)
                for letter in collected:
                    if letter.isprintable():
                        pass
                        # print(letter, end='')
                    else:
                        pass
                        # print('.', end='')

                collected = ''
                count = 0

                # other vertical headers
                a = next(n)
                headers_v.append(a)

        nums.append(cur_line)

        for letter in collected:
            if letter.isprintable():
                pass
                # print(letter, end='')
            else:
                pass
                # print('.', end='')

        f.close()

        return headers_h, headers_v, nums


if __name__ == '__main__':
    # editor = Editor("data.txt")
    # editor.printout()
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
