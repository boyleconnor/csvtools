#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3
import sys
import csv
import importlib
import click
from header import Header


class Row:
    def __init__(self, header, row_tuple):
        self.header = header
        self.row_tuple = row_tuple

    def __getitem__(self, column):
        return self.row_tuple[self.header.get_index(column)]

    def __getattr__(self, column):
        return self.row_tuple[self.header.get_index(column)]


@click.command()
@click.option('--delimiter', '-d', default=',', help='Delimiting character of'\
        ' the input CSV file.')
@click.option('--tabs', '-t', is_flag=True, help='Specify that the input CSV'\
        ' file is delimited with tabs. Overrides "-d".')
@click.option('--label', '-l', default='', 'Label for new column')
@click.option('--function', '-f', default='', help='Expression for value in'\
        ' new column of given row.')
@click.option('prep_commands', '--prep', '-r', default='', help='Commands to'\
        ' be executed (e.g. import libraries, create data structures) before'\
        ' processing rows.')
@click.option('--names', '-n', is_flag=True, help='If flagged, output column '\
        'names and numbers, then exit.')
@click.argument('input_stream', type=click.File('r'), default=sys.stdin)
def csvfunc(input_stream, delimiter, tabs, label, function, prep_commands, names):
    '''Append a new column whose values are user-defined in terms of other
    values in the same row.
    '''
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


if __name__ == '__main__':
    csvfunc()
