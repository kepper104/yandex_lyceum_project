from utils import show_error, next_line


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
        File getter, returns file's data

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
        Changes file's current, unsaved data

        Parameters:
            self
            row (int): changed item's row
            col (int): changed item's column
            new_item (str): new item

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
        """
        Save file's current data

        Parameters:
            self

        Returns:
            None
        """
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
        """
        Create new cells and fill empty ones with nulls

        Parameters:
            self
            row (int): to what row cells need to be expanded
            col (int): to what column cells need to be expanded

        Returns:
            None
        """
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
