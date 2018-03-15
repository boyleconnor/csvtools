def to_number(num_string):
    try:
        number = int(num_string)
    except ValueError:
        try:
            number = float(num_string)
        except ValueError:
            raise ValueError("Could not convert '%s' to int or float" % num_string)
    return number


def COUNT(column, distinct=False, non_empty=False):
    if non_empty:
        column = [value for value in column if value != '']
    if distinct:
        column = set(column)
    return len(column)


def SUM(column, convert_to_number=True):
    if convert_to_number:
        column = [to_number(value) for value in column]
        return sum(column)
    else:
        return ''.join(column)


def MIN(column, convert_to_number=True):
    if convert_to_number:
        column = [to_number(value) for value in column]
    return min(column)


def MAX(column, convert_to_number=True):
    if convert_to_number:
        column = [to_number(value) for value in column]
    return max(column)


def FIRST(column):
    return column[0]


def LAST(column):
    return column[-1]
