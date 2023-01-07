import sys

import tab
from utils import WarningWindow

from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog

# High Windows Scaling Fix
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
        """
        Delete selected file and tab internally on tab close click
        Also check and warn if file isn't saved

        Parameters:
            self
            index (int): tab selected

        Returns:
            None
        """

        if "*" in self.tabWidget.tabText(self.cur_tab_index):
            self.warn = WarningWindow()
            if self.warn.exec():
                self.tabs.pop(index)
                self.tabWidget.removeTab(index)
            else:
                pass
        else:
            self.tabs.pop(index)
            self.tabWidget.removeTab(index)

    def change_selected_tab(self, index):
        """
        Change selected file internally on tab select

        Parameters:
            self
            index (int): tab selected

        Returns:
            None
        """

        self.cur_tab_index = index

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
        """
        Delete selected file and tab internally on tab close click

        Parameters:
            self
            tab_name (str): tab name, usually a full path to file
            file_name (str): file that will be opened
        Returns:
            None
        """
        new_tab = tab.TabForm(file_name, self)
        tab_real_name = tab_name.split("/")[-1]
        self.tabWidget.addTab(new_tab, tab_real_name)
        self.tabs.append(new_tab)
        self.tabWidget.setCurrentIndex(len(self.tabs) - 1)

    def create_file(self):
        """
        Delete selected file and tab internally on tab close click

        Parameters:
            self

        Returns:
            None
        """
        file_name = QFileDialog.getSaveFileName(self, "Choose file name", "")[0]
        with open(file_name, "w") as file:
            pass
        self.add_tab(tab_name=file_name, file_name=file_name)

    def change_tab_status(self, file_name, saved=False):
        """
        Change tab's saved'ness of name file_name, by default, it is unsaved

        Parameters:
            self
            file_name (str): tab name that is changed
            saved (bool): what to change tab status to

        Returns:
            None
        """

        if not saved:
            self.tabWidget.setTabText(self.cur_tab_index, file_name.split("/")[-1] + "*")
        else:
            self.tabWidget.setTabText(self.cur_tab_index, file_name.split("/")[-1])

    def save_file(self):
        """
        Sets file_name that is being edited

        Parameters:
            self

        Returns:
            None
        """
        if self.tabs[self.cur_tab_index].isExampleTab:
            return

        cur_file = self.tabs[self.cur_tab_index].file
        self.change_tab_status(cur_file.file_name, True)
        cur_file.save()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
