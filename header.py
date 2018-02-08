class Header:
    def __init__(self, header_tuple):
        self.header = header_tuple

    def get_index(self, column):
        if type(column) == int:
            return column-1
        elif type(column) == str:
            return self.header.index(column)

    def get_label(self, column):
        if type(column) == int:
            return self.header[column-1]
        elif type(column) == str:
            return column
