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
@click.argument('input_stream', type=click.File('r'), default=sys.stdin)
@click.option('--delimiter', '-d', default=',')
@click.option('--tabs', '-t', default=False)
@click.option('--label', '-l', default='')
@click.option('--function', '-f', default='')
@click.option('prep_commands', '--prep', '-r', default='')
@click.option('--names', '-n', is_flag=True)
def csvfunc(input_stream, delimiter, tabs, label, function, prep_commands, names):
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
