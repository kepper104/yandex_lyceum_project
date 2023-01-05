import sys

import tab
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from utils import next_line, show_error

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(
        QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class App(QMainWindow):
    """
    Main class, contains all gui related things.
    """

    def __init__(self):
        """
        Loads ui from design.ui, creates home tab and connects all buttons
        Parameters:
            self
        Returns:
            None
        """

        super().__init__()
        uic.loadUi('../designs/design.ui', self)

        self.cur_tab_index = 0

        self.pushButton.clicked.connect(self.create_file)
        self.pushButton_2.clicked.connect(self.openfile)
        self.pushButton_3.clicked.connect(self.save_file)

        self.tabWidget.tabCloseRequested.connect(self.close_tab)
        self.tabWidget.currentChanged.connect(self.change_selected_tab)

        example_tab = tab.ExampleTab()

        self.tabWidget.addTab(example_tab, "Welcome!")

        # By default, is created with 2 tabs already open, so kill them
        self.tabWidget.removeTab(0)
        self.tabWidget.removeTab(0)

        self.tabs = []
        self.tabs.append(example_tab)

    def close_tab(self, index):
        self.tabs.pop(index)
        self.tabWidget.removeTab(index)

    def change_selected_tab(self, i):
        self.cur_tab_index = i

    def openfile(self):
        """
        Prompts user to open a file and calls add_tab with inputted file name.
        If user didn't select file, function does nothing.

        Parameters:
            self
        Returns:
            None
        """

        file_name = QFileDialog.getOpenFileName(self, 'Select file', '')[0]

        if file_name is None or file_name == '':
            return
        self.add_tab(file_name=file_name, tab_name=file_name)

    def add_tab(self, tab_name="New File.txt", file_name="empty.txt"):
        new_tab = tab.TabForm(file_name, self)
        tab_real_name = tab_name.split("/")[-1]
        self.tabWidget.addTab(new_tab, tab_real_name)
        self.tabs.append(new_tab)
        self.tabWidget.setCurrentIndex(len(self.tabs) - 1)

    def create_file(self):
        file_name = QFileDialog.getSaveFileName(self, "Choose file name", "")[0]
        with open(file_name, "w") as file:
            pass
        self.add_tab(tab_name=file_name, file_name=file_name)

    def change_tab_status(self, file_name, saved=False):
        if not saved:
            self.tabWidget.setTabText(self.cur_tab_index, file_name.split("/")[-1] + "*")
        else:
            self.tabWidget.setTabText(self.cur_tab_index, file_name.split("/")[-1])

    def save_file(self):
        if self.tabs[self.cur_tab_index].isExampleTab:
            return

        cur_file = self.tabs[self.cur_tab_index].file
        self.change_tab_status(cur_file.file_name, True)
        cur_file.save()


class File:
    """
    Main file class, handles reading files, editing files ...
    """

    def __init__(self, file_name, parent_app):
        """
        Sets file_name that is being edited

        Parameters:
            self
            file_name (str): name of file edited

        Returns:
            None
        """
        self.file_name = file_name
        self.headers_h = []
        self.cells = []
        self.cur_cells = []
        self.letter_cells = []
        self.app = parent_app
        self.read_data()
        self.cur_cells.extend(self.cells)

    def get_data(self):
        """
        Basic File getter, returns file's data

        Parameters:
            self
        Returns:
            self.headers
        """
        return self.headers_h, self.cur_cells, self.letter_cells

    def printout(self):
        """
        Legacy function from a cli hex reader, prints out hex view of file to terminal, don't look here...

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

    def read_data(self):
        """
        Function that reads edited file in hex, sets self parameters

        Parameters:
            self
        Returns:
            None
        """

        collected = ''
        cur_line = ""
        count = 0

        # stuff to save
        headers_h = []
        cells = []

        # horizontal headers
        for i in range(0, 16):
            headers_h.append(str(hex(i))[2:].rjust(2, '0'))

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
                cells.append(cur_line)
                cur_line = ""
                collected += chr(i)
                for letter in collected:
                    if letter.isprintable():
                        self.letter_cells.append(letter)
                    else:
                        self.letter_cells.append('.')
                collected = ''
                count = 0
        cells.append(cur_line)

        for letter in collected:
            if letter.isprintable():
                self.letter_cells.append(letter)
            else:
                self.letter_cells.append('.')

        f.close()

        for i in range(len(cells)):
            cells[i] = cells[i].split(' ')

        self.headers_h = headers_h
        self.cells = cells

    def change_file(self, row, col, new_item):
        """
        Changes file's data

        Parameters:
            self
        Returns:
            None
        """
        self.app.change_tab_status(self.file_name, saved=False)
        self.cur_cells[row][col] = new_item
        new_letters = []

        for i in self.cur_cells:
            for j in i:
                if j == '':
                    continue
                letter = chr(int(j, 16))
                if letter.isprintable():
                    new_letters.append(letter)
                else:
                    new_letters.append('.')

        self.letter_cells.clear()
        self.letter_cells.extend(new_letters)

    def save(self):
        cells = self.cur_cells
        all_cells = []

        for i in cells:
            for el in i:
                if el == '':
                    continue
                all_cells.append((int(el, 16)))

        try:
            with open(self.file_name, 'wb') as f:
                f.write(bytes(all_cells))

        except ValueError:
            show_error(self.app,
                       "Critical Error!",
                       "Something went wrong when writing to file",
                       "The program will close and file might get corrupted")

    def expand_cells(self, row, col):
        num_rows = len(self.cur_cells)

        # Set last character to null as expanding doesn't work on it
        self.cur_cells[-1][-1] = '00'

        # If the row or column indices are larger than the size of the cells table,
        # we need to expand the cells table
        if row >= num_rows:
            # Add rows to the table until it has the desired number of rows
            for i in range(num_rows, row + 1):
                self.cur_cells.append([])
            num_rows = row + 1
        if col >= len(self.cur_cells[row]):
            # Add columns to all rows until the table has the desired number of columns
            for i in range(num_rows):
                # In all rows prior to needed, all 16 cells are filled
                if i != row:
                    while len(self.cur_cells[i]) < 16:
                        self.cur_cells[i].append('00')
                else:
                    while len(self.cur_cells[i]) <= col:
                        self.cur_cells[i].append('00')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
