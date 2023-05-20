import constants.const as con


def empty_elements(array: list) -> bool:
    """Return True, if there are 5 in a row empty elements, else False"""
    counter = 0
    for i in range(len(array)):
        if counter == 4 and array[i] == 0:
            return True
        if array[i] == 1:
            counter = 0
        else:
            counter += 1
    return False


def check_rows(array: list) -> bool:
    """Return True if any row has 5 in a row empty elements, else False"""
    for row in array:
        if empty_elements(row):
            return True
    return False


def check_columns(array: list) -> bool:
    """Return True if any column has 5 in a row empty elements, else False"""
    array_t = [
                [array[j][i] for j in range(len(array))]
                for i in range(len(array[0]))
              ]
    for column in array_t:
        if empty_elements(column):
            return True
    return False


def count_diagonals(matrix_size: int, target_count: int) -> int:
    """
    Return amount of diagonals which have target_count elements
    in a square matrix of size matrix_size
    """
    return ((matrix_size - target_count) * 2 + 1) * 2


def array_for_diagonal(array: list, row: int, col: int,
                       direction: str) -> list:
    """
    Make a diagonal which starts in [row][col], based on direction: left or
    right. Row, col expected to be in range of array.
    """
    diagonal = []
    if direction == 'right':
        decider = max(row, col)
        iterations = len(array) - decider
        for i in range(iterations):
            element = array[row+i][col+i]
            diagonal.append(element)
    if direction == 'left':
        closer_row = con.BOARD_ROWS - row
        closer_col = col + 1
        iterations = min(closer_row, closer_col)
        for i in range(iterations):
            element = array[row+i][col-i]
            diagonal.append(element)
    return diagonal


def check_diagonals(array: list, n: int) -> bool:
    """Return True if any diagonal has 5 in a row empty elements, else False"""
    amount_d = count_diagonals(con.BOARD_ROWS, n)
    j = int((amount_d/2 - 1)/2)
    for i in range(-j, j+1):
        a = 0
        b = 0
        c = 0
        d = con.BOARD_ROWS - 1
        if i < 0:
            a = -i
            d += i
        else:
            b = i
            c = i
        left_diagonal = array_for_diagonal(array, a, b, 'right')
        right_diagonal = array_for_diagonal(array, c, d, 'left')
        if empty_elements(left_diagonal):
            return True
        if empty_elements(right_diagonal):
            return True
    return False
