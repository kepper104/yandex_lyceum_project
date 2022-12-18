import sys

import tab
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QFileDialog, QTableWidget
from PyQt5.QtWidgets import QWidget

def next_line():
    cur = 0
    while True:
        yield str(hex(cur))[2:].rjust(5, '0').ljust(6, '0')
        cur += 1



class App(QMainWindow):
    """
    Main class, contains all gui related things.
    """

    def __init__(self):
        """
        Is called only on program start and loads ui from design.ui
        Parameters:
            self
        Returns:
            None
        """

        super().__init__()
        # with open("empty.txt", 'w') as f:
        #     pass
        uic.loadUi('design.ui', self)
        self.cur_tab_index = 0
        self.pushButton_2.clicked.connect(self.openfile)
        self.pushButton.clicked.connect(self.create_file)
        self.pushButton_3.clicked.connect(self.save_file)
        self.tabWidget.tabCloseRequested.connect(self.close_tab)
        self.tabWidget.currentChanged.connect(self.change_selected_tab)
        self.tabWidget.removeTab(0)

        example_tab = tab.ExampleTab()

        self.tabWidget.addTab(example_tab, "Welcome!")
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
        Prompts user to open a file and calls loadfile with inputted file name.

        Parameters:
            self
        Returns:
            None
        """

        file_name = QFileDialog.getOpenFileName(self, 'Select file', '')[0]
        if file_name is None or file_name == '':
            return
        print(file_name)
        self.add_tab(file_name=file_name, tab_name=file_name)

    def add_tab(self, tab_name="New File.txt", file_name="empty.txt"):
        new_tab = tab.TabForm(file_name, self)
        # self.tabWidget.setTabText(0, "hi")

        tab_real_name = tab_name.split("/")[-1]
        self.tabWidget.addTab(new_tab, tab_real_name)
        self.tabs.append(new_tab)
        self.tabWidget.setCurrentIndex(len(self.tabs) - 1)

    def create_file(self):
        file_name = QFileDialog.getSaveFileName(self, "Choose file name", "")[0]
        with open(file_name, "w") as file:
            pass
        # print("Created", file_name)
        self.add_tab(tab_name=file_name, file_name=file_name)

    def change_tab_status(self, file_name, saved=False):
        if not saved:
            self.tabWidget.setTabText(self.cur_tab_index, file_name.split("/")[-1] + "*")
        else:
            self.tabWidget.setTabText(self.cur_tab_index, file_name.split("/")[-1])
    def save_file(self):
        print("saving..")



        if self.tabs[self.cur_tab_index].isExampleTab:
            return
        cur_file = self.tabs[self.cur_tab_index].file
        self.change_tab_status(cur_file.file_name, True)
        cur_file.save()
class File:
    """
    Main editor class, handles reading files, editing files ...
    """

    def __init__(self, file_name, app):
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
        self.app = app
        self.read_data()
        self.cur_cells.extend(self.cells)
    def get_data(self):
        return self.headers_h, self.cur_cells, self.letter_cells
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

    def read_data(self):
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
        cells = []

        # horizontal headers
        for i in range(0, 16):
            headers_h.append(str(hex(i))[2:].rjust(2, '0'))


        f = open(self.file_name, 'rb')
        # print(f.read())
        # reading file symbol by symbol
        for i in f.read():
            # print(i)
            # input()
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
        print(self.letter_cells)
        cells.append(cur_line)

        for letter in collected:
            if letter.isprintable():
                self.letter_cells.append(letter)
                # print(letter, end='')
            else:
                self.letter_cells.append('.')
                # print('.', end='')

        f.close()
        for i in range(len(cells)):
            cells[i] = cells[i].split(' ')

        self.headers_h = headers_h
        self.cells = cells

    def change_file(self, row, col, new_item):
        print("updating: ")
        print(self.cur_cells)
        print(self.cur_cells[row][col])
        self.app.change_tab_status(self.file_name, saved=False)
        self.cur_cells[row][col] = new_item
        print(self.cur_cells[row][col])
        new_letters = []
        for i in self.cur_cells:
            for j in i:
                if j == '':
                    print("herrr")
                    new_letters.append(' ')
                    continue
                print("hey", j)
                letter = chr(int(j, 16))
                if letter.isprintable():
                    new_letters.append(letter)
                else:
                    new_letters.append('.')
        self.letter_cells.clear()
        self.letter_cells.extend(new_letters)
        print("new let", new_letters)
        print("updated cur_cells")
        print(self.cur_cells)
        # print("Inside", row, col, self.cells[row][col])

    def save(self):
        cells = self.cur_cells
        all_cells = []
        print(cells)
        for i in cells:
            for el in i:
                if el == '':
                    continue
                all_cells.append((int(el, 16)))
        print(all_cells)
        with open(self.file_name, 'wb') as f:
            f.write(bytes(all_cells))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
