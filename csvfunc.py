#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3
import sys
import csv
import importlib
from header import Header


class Row:
    def __init__(self, header, row_tuple):
        self.header = header
        self.row_tuple = row_tuple

    def __getitem__(self, column):
        return row_tuple[header.get_index(column)]

    def __getattr__(self, column):
        return row_tuple[header.get_index(column)]


# Default args
delimiter = ','
label = ''
filename = ''
prep_commands = ''
names = False
modules = []


# Extract arguments
i = 1
while i < len(sys.argv):
    if sys.argv[i] in {'-d', '--delimiter'}:
        delimiter = sys.argv[i+1]
        i += 2
    elif sys.argv[i] in {'-t', '--tabs'}:
        delimiter = '\t'
        i += 1
    elif sys.argv[i] in {'-l', '--label'}:
        label = sys.argv[i+1]
        i += 2
    elif sys.argv[i] in {'-f', '--function'}:
        function = sys.argv[i+1]
        i += 2
    elif sys.argv[i] in {'-r', '--prep'}:
        prep_commands = sys.argv[i+1]
        i += 2
    elif sys.argv[i] in {'-n', '--names'}:
        names = True
        i += 1
    else:
        filename = sys.argv[i]
        i += 1


# Set up input and output streams
if filename:
    input_stream = open(filename, 'r')
else:
    input_stream = sys.stdin
reader = csv.reader(input_stream, delimiter=delimiter)
writer = csv.writer(sys.stdout, lineterminator='\n')


# Execute prep commands (import libraries, set up data structures, etc.)
exec(prep_commands)


# Feed to output
first_row = True
for row_tuple in reader:
    if first_row:
        if names:
            for i in range(len(row_tuple)):
                print('%s: %s' % (str(i+1).rjust(3), row_tuple[i]))
            exit()
        writer.writerow(row_tuple+[label])
        header = Header(row_tuple)
        first_row = False
    else:
        row = Row(header, row_tuple)
        value = eval(function)
        try:
            writer.writerow(row_tuple+[value])
        except BrokenPipeError:
            sys.stderr.close()
            break
