from PyQt5.QtWidgets import QMessageBox, QDialog, QDialogButtonBox, QVBoxLayout, QLabel


# Hex lines generator for tables
def next_line():
    cur = 0
    while True:
        yield str(hex(cur))[2:].rjust(5, '0').ljust(6, '0')
        cur += 1


# Error window creator
def show_error(parent_window, title, text, inf_text):
    parent_window.error = QMessageBox()
    parent_window.error.setIcon(QMessageBox.Critical)
    parent_window.error.setText(text)
    parent_window.error.setInformativeText(inf_text)
    parent_window.error.setWindowTitle(title)
    parent_window.error.show()


# Warning window
class WarningWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("HELLO!")

        self.QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(self.QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("You are trying to close an unsaved file! Proceed?")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)