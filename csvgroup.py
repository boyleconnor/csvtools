#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3
import csv
import sys
import string
import click
from header import Header


def to_number(num_string):
    try:
        number = int(num_string)
    except ValueError:
        try:
            number = float(num_string)
        except ValueError:
            raise ValueError("Could not convert '%s' to int or float" % num_string)
    return number


def clean_columns(column_string):
    if not column_string:
        return []
    columns = column_string.split(',')
    cleaned_columns = []
    for column in columns:
        bounds = column.split('-')
        if len(bounds) == 2 and bounds[0].isdigit() and bounds[1].isdigit():
            column_range = range(int(bounds[0]), int(bounds[1])+1)
            cleaned_columns += list(column_range)
        elif column.isdigit():
            cleaned_columns.append(int(column))
        else:
            cleaned_columns.append(column)
    return cleaned_columns


# Defaults
filename = None
i = 1
delimiter = ','
count_column = 'COUNT'
sum_columns = []
max_columns = []
min_columns = []
names = False




@click.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('--columns', '-c', type=str)
@click.option('--count', '-C', default='COUNT')
@click.option('sum_columns', '--sum', '-s')
@click.option('max_columns', '--max', '-M')
@click.option('min_columns', '--min', '-m')
@click.option('--delimiter', '-d', default=',')
@click.option('--tabs', '-t', default=False)
@click.option('--names', '-n', is_flag=True)
def csvgroup(filename, columns, count, sum_columns, max_columns, min_columns, delimiter, tabs, names):
    columns = clean_columns(columns)
    sum_columns = clean_columns(sum_columns)
    max_columns = clean_columns(max_columns)
    min_columns = clean_columns(min_columns)
    group_columns = set(sum_columns+max_columns+min_columns)

    # Set up input and output streams
    if filename:
        input_stream = open(filename, 'r')
    else:
        input_stream = sys.stdin
    reader = csv.reader(input_stream, delimiter=delimiter)
    writer = csv.writer(sys.stdout, lineterminator='\n')


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
                    'max': {header.get_label(column): to_number(row[header.get_index(column)]) for column in max_columns},
                    'min': {header.get_label(column): to_number(row[header.get_index(column)]) for column in min_columns},
                    'sum': {header.get_label(column): to_number(row[header.get_index(column)]) for column in sum_columns},
                    'count': 1
                }
            else:
                table[pk] = {
                    'max': {header.get_label(column): max(to_number(row[header.get_index(column)]), table[pk]['max'][header.get_label(column)]) for column in max_columns},
                    'min': {header.get_label(column): min(to_number(row[header.get_index(column)]), table[pk]['min'][header.get_label(column)]) for column in min_columns},
                    'sum': {header.get_label(column): to_number(row[header.get_index(column)]) + table[pk]['sum'][header.get_label(column)] for column in sum_columns},
                    'count': table[pk]['count'] + 1
                }


    output_header = tuple(header.get_label(column) for column in columns) + (count_column,) + \
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


if __name__ == '__main__':
    csvgroup()
