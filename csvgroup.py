#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3
import csv
import sys
import string
import click
from column_functions import *
from header import Header


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


class Group:
    '''Represents the contents of a given "group". A tuple containing all
    values in a given column of the group (in original order) can be accessed
    in any of the following ways: group.<COLUMN_NAME>, group['<COLUMN_NAME>']
    or group[<COLUMN_NUMER>], where COLUMN_NUMBER is 1-indexed, and ignoring <
    and >.
    '''
    def __init__(self, header, group_dict):
        self.header = header
        self.group_dict = group_dict

    def __getitem__(self, column):
        return tuple(self.group_dict[self.header.get_label(column)])

    def __getattr__(self, column):
        return tuple(self.group_dict[self.header.get_label(column)])


@click.command()
@click.option('group_columns', '--columns', '-c', type=str, help='List of'\
        ' columns for new primary key.')
@click.option('output_columns', '--output', '-o', default='', multiple=True,
        help='New columns to output, e.g. COLUMN_LABEL=SOME_EXPRESSION.')
@click.option('--delimiter', '-d', default=',', help='Delimiting character of'\
        ' the input CSV file.')
@click.option('--tabs', '-t', is_flag=True, help='Specify that the input CSV'\
        ' file is delimited with tabs. Overrides "-d".')
@click.option('--names', '-n', is_flag=True, help='If flagged, output column '\
        'names and numbers, then exit.')
@click.argument('input_stream', type=click.File('r'), default=sys.stdin, metavar='[FILE]')
def csvgroup(input_stream, group_columns, output_columns, delimiter, tabs, names):
    '''Group columns by user-defined primary key
    '''
    group_columns = clean_columns(group_columns)
    output_columns = [(column.split('=')[0], column.split('=', 1)[1]) for column in output_columns]

    # Set up input and output streams
    reader = csv.reader(input_stream, delimiter=delimiter if not tabs else '\t')
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
            sum_columns = [column for column in row if column not in group_columns]
            first_row = False

        # Generate table
        else:
            pk = tuple(row[header.get_index(i)] for i in group_columns)
            if pk not in table.keys():
                table[pk] = {column: [row[header.get_index(column)]] for column in sum_columns}
            else:
                [table[pk][column].append(row[header.get_index(column)]) for column in sum_columns]

    # Output header
    output_header = tuple(header.get_label(column) for column in group_columns) + tuple(column[0] for column in output_columns)
    writer.writerow(output_header)

    # Output each group (by pk)
    for pk in table.keys():
        group_cells = pk
        group = Group(header, table[pk])
        output_cells = tuple()
        for column_label, column_function in output_columns:
            output_cells += (eval(column_function),)  # Evaluate user function
        row = group_cells + output_cells
        try:
            writer.writerow(row)
        except BrokenPipeError:
            sys.stderr.close()
            break


if __name__ == '__main__':
    csvgroup()
