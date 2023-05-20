from support_functions.chaos_won_first_stage import array_for_diagonal
import constants.const as con


def make_column(ar: list, col: int) -> list:
    """Make a column under index col from ar"""
    return [ar[i][col] for i in range(con.BOARD_COLS)]


def second_stage(ar: list) -> bool:
    """Check if all lines are blocked for Order"""
    for i in range(con.BOARD_ROWS):
        for j in range(con.BOARD_COLS):
            element = ar[i][j]
            if element == 0:
                continue
            lines = make_array_for_element(ar, i, j)
            for line in lines:
                if check_single_line(line, element):
                    return False
    return True


def check_length(diagonal: list) -> bool:
    """Return True if diagonal has 5 or more elements, else False"""
    return len(diagonal) >= 5


def make_full_desc_diagonal(ar: list, row: int, col: int) -> list:
    """Make a full descending diagonals which contains an element [row][col]"""
    decider = min(row, col)
    new_row = row
    new_col = col
    for _ in range(decider):
        new_row -= 1
        new_col -= 1
    return array_for_diagonal(ar, new_row, new_col, 'right')


def make_full_asc_diagonal(ar: list, row: int, col: int) -> list:
    """Make a full ascending diagonals which contains an element [row][col]"""
    decider = min(row, con.BOARD_COLS - 1 - col)
    new_row = row
    new_col = col
    for _ in range(decider):
        new_row -= 1
        new_col += 1
    return array_for_diagonal(ar, new_row, new_col, 'left')


def make_array_for_element(ar: list, i: int, j: int) -> list:
    """Make a list of lines containing element ar[i][j]"""
    lines = []
    row = ar[i]
    col = make_column(ar, j)
    lines.append(row)
    lines.append(col)
    desc_diagonal = make_full_desc_diagonal(ar, i, j)
    asc_diagonal = make_full_asc_diagonal(ar, i, j)
    if check_length(desc_diagonal):
        lines.append(desc_diagonal)
    if check_length(asc_diagonal):
        lines.append(asc_diagonal)
    return lines


def check_single_line(line: list, element: int) -> bool:
    """
    Check if in the line there is a chance to get 5 elements(element) in a row
    """
    sublines = []
    opposite_el = element % 2 + 1
    if len(line) == 6:
        sublines = [line[0:5], line[1:6]]
        # 6 in a row doesn't count as a win for Order, so the line is blocked
        if line[0] == line[5] and line[0] != 0:
            return False
    else:
        sublines.append(line)
    found_opposite = False
    # if subline has an opposite element - the line is blocked
    for subline in sublines:
        for sign in subline:
            if sign == opposite_el:
                found_opposite = True
        if not found_opposite:
            return True
        found_opposite = False
    return False
