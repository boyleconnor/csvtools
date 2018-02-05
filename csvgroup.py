#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3
import csv
import sys
import string


def clean_columns(column_string):
    columns = column_string.split(',')
    cleaned_columns = []
    for column in columns:
        if all([digit in string.digits for digit in column]):
            cleaned_columns.append(int(column))
        else:
            cleaned_columns.append(column)
    return cleaned_columns


# Defaults
filename = None
i = 1
delimiter = ','
count_column = ''
sum_columns = []
max_columns = []
min_columns = []
names = False


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


# Extract arguments
while i < len(sys.argv):
    if sys.argv[i] in {'-c', '--columns'}:
        columns = clean_columns(sys.argv[i+1])
        i += 2
    elif sys.argv[i] in {'-C', '--count'}:
        count_column = sys.argv[i+1]
        i += 2
    elif sys.argv[i] in {'-s', '--sum'}:
        sum_columns = clean_columns(sys.argv[i+1])
        i += 2
    elif sys.argv[i] in {'-M', '--max'}:
        max_columns = clean_columns(sys.argv[i+1])
        i += 2
    elif sys.argv[i] in {'-m', '--min'}:
        min_columns = clean_columns(sys.argv[i+1])
        i += 2
    elif sys.argv[i] in {'-d', '--delimiter'}:
        delimiter = sys.argv[i+1]
        i += 2
    elif sys.argv[i] in {'-t', '--tabs'}:
        delimiter = '\t'
        i += 1
    elif sys.argv[i] in {'-n', '--names'}:
        names = True
        i += 1
    else:
        filename = sys.argv[i]
        i += 1
group_columns = set(sum_columns+max_columns+min_columns)


# Set up input and output streams
if filename:
    input_stream = open(filename, 'r')
else:
    input_stream = sys.stdin
reader = csv.reader(input_stream, delimiter=delimiter)
writer = csv.writer(sys.stdout)


# Generate table from input
table = {}
first_row = True
for row in reader:

    # Figure out column numbers from header
    if first_row:
        # Just print names if "-n" or "--names"
        if names:
            for i in range(len(row)):
                print('%s: %s' % (str(i+1).rjust(3), row[i]))
            exit()
        header = Header(row)
        first_row = False

    # Generate table
    else:
        pk = tuple(row[header.get_index(i)] for i in columns)
        if pk not in table.keys():
            table[pk] = {
                'max': {header.get_label(column): int(row[header.get_index(column)]) for column in max_columns},
                'min': {header.get_label(column): int(row[header.get_index(column)]) for column in min_columns},
                'sum': {header.get_label(column): int(row[header.get_index(column)]) for column in sum_columns},
                'count': 1
            }
        else:
            table[pk] = {
                'max': {header.get_label(column): max(int(row[header.get_index(column)]), int(table[pk]['max'][header.get_label(column)])) for column in max_columns},
                'min': {header.get_label(column): min(int(row[header.get_index(column)]), int(table[pk]['min'][header.get_label(column)])) for column in min_columns},
                'sum': {header.get_label(column): int(row[header.get_index(column)]) + int(table[pk]['sum'][header.get_label(column)]) for column in sum_columns},
                'count': table[pk]['count'] + 1
            }


output_header = tuple(header.get_label(column) for column in columns) + (count_column if count_column else 'COUNT',) + \
    tuple('MAX_'+header.get_label(column) for column in max_columns) + \
    tuple('MIN_'+header.get_label(column) for column in min_columns) + \
    tuple('SUM_'+header.get_label(column) for column in sum_columns)
writer.writerow(output_header)


for pk in table.keys():
    row = pk + (table[pk]['count'],) + \
        tuple(table[pk]['max'][header.get_label(column)] for column in max_columns) + \
        tuple(table[pk]['min'][header.get_label(column)] for column in min_columns) + \
        tuple(table[pk]['sum'][header.get_label(column)] for column in sum_columns)
    try:
        writer.writerow(row)
    except BrokenPipeError:
        sys.stderr.close()
        break
