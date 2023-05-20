import random
from classes.board import Board
from random import randint, sample, choice
import constants.const as con
from support_functions.chaos_won_second_stage import (make_column,
                                                      check_single_line)
from support_functions.chaos_won_first_stage import array_for_diagonal


class Player:
    """Class representing all kind of players: live player and AIs"""

    def __init__(self, board: Board, role=None) -> None:
        self._board = board
        self._role = role

    def board(self) -> Board:
        return self._board

    def role(self) -> str:
        return self._role


class LivePlayer(Player):
    """Class representing live player"""

    def __init__(self, board: object, role) -> None:
        super().__init__(board, role)


class AiPlayer(Player):
    """Class representing 2 type of AIs: random and supreme"""

    def __init__(self, board: object, name) -> None:
        super().__init__(board)
        self._name = name

    def name(self) -> str:
        """Return AI's name"""
        return self._name

    def make_diagonals(self, array: list, index: int) -> tuple:
        """Makes left descending diagonal and right ascending diagonal.
        Returns a tuple of 2 tuples which consist out of a diagonal
        and its starting position"""

        a, b, c = 0, 0, 0
        d = con.BOARD_ROWS - 1
        # decide starting index
        if index < 0:
            a = -index
            d += index
        else:
            b, c = index, index
        # make 2 diagonals based on their starting indexes
        left_d = array_for_diagonal(array, a, b, 'right')
        right_d = array_for_diagonal(array, c, d, 'left')
        return (left_d, (a, b)), (right_d, (c, d))


class AiRandom(AiPlayer):
    """Class representing random AI"""

    def __init__(self, board: object, name='random') -> None:
        super().__init__(board, name)

    def decide_move_random(self) -> tuple:
        """Randomly pick a sign and pick an empty position to place it in."""
        signs = [1, 2]
        sign = choice(signs)
        found_empty = False
        while not found_empty:
            row, col = sample(range(0, con.BOARD_ROWS), 2)
            found_empty = self.board().available_square(row, col)
        return (row, col, sign)


class AiSupreme(AiPlayer):
    """Class representing supreme AI"""

    def __init__(self, board: object, name='supreme') -> None:
        super().__init__(board, name)
        self._moves_board = con.CHAOS_BOARD

    def moves_board(self) -> list:
        """Return a list with coordinates which Chaos uses to respond
        to Player's moves"""
        return self._moves_board

    def decide_move_chaos(self, coordinates, sign) -> tuple:
        """
        Decides what is the move for Chaos based on Player's last move

        Parameters
        ----------
        coordinates: tuple: (int, int)
            Row and column which Player marked on his previous move
        sign: int
            Sign Player marked a square with on his previous move

        If Player marked a square in the corner the sign will be the same
        as Player's, otherwise it will be opposite.
        Decides row and column with moves_board using pairing strategy
        """
        corner = [(0, 0), (0, con.BOARD_COLS - 1), (con.BOARD_ROWS - 1, 0),
                  (con.BOARD_ROWS - 1, con.BOARD_COLS - 1)]
        moves_board = self.moves_board()
        row, col = coordinates
        if coordinates in corner:
            ai_sign = sign
        else:
            ai_sign = sign % 2 + 1
        ai_row, ai_col = moves_board[row][col]
        return ai_row, ai_col, ai_sign

    def decide_move_order(self) -> tuple:
        """
        Finds a line with max amount of elements on the board if this line
        is not blocked.

        1. Finds lines with n elements
        2. Checks if they are not blocked.
        3. If at least one line stays after the check, finds best position
           on this line. If no line stays, find lines with n - 1 elements.
        """
        def number_of_elements(line: list, sign: int, n: int) -> bool:
            """Returns True if number of elements in line == n, else False"""
            return line.count(sign) == n

        array = self.board().table()
        signs = [1, 2]
        good_moves = []

        for i in range(con.BOARD_ROWS - 2, 0, -1):
            suitable_lines = []
            for sign in signs:
                # find lines with i elements
                for index, row in enumerate(array):
                    # iterate through rows
                    if number_of_elements(row, sign, i):
                        suitable_lines.append((index, row, sign, i, 'r'))
                for index in range(con.BOARD_COLS):
                    # iterate through columns
                    col = make_column(array, index)
                    if number_of_elements(col, sign, i):
                        suitable_lines.append((index, col, sign, i, 'c'))
                j = int((con.BOARD_ROWS/2 - 1)/2)
                for index in range(-j, j+1):
                    # iterate through diagonals
                    left, right = self.make_diagonals(array, index)
                    left_d, l_coords = left
                    right_d, r_coords = right
                    if number_of_elements(left_d, sign, i):
                        suitable_lines.append((l_coords, left_d,
                                               sign, i, 'l_d'))
                    if number_of_elements(right_d, sign, i):
                        suitable_lines.append((r_coords, right_d,
                                               sign, i, 'r_d'))

            for line in suitable_lines:
                sign = line[2]
                # check if line is not blocked
                if check_single_line(line[1], sign):
                    good_moves.append(line)
            # found a not blocked line
            if len(good_moves) != 0:
                break
            good_moves = []
        # find empty line, if no lines with even 1 element
        if len(good_moves) == 0:
            row, col, sign = self.find_empty_line()[0]
            return row, col, sign
        random.shuffle(good_moves)
        # find best position on line
        return self.decide_index(good_moves[0])

    def decide_index(self, move: list) -> tuple:
        """
        Find best position for a line in move[1].

        First checks if a line can become a winning move.
        If not, iterates through line starting from second element and
        finds empty square. Only then checks first element.

        Return (row, column, sign)
        """
        sign = move[2]
        if move[4] == 'r' or move[4] == 'c':
            index = move[0]
            line = move[1]
            # check if a line can become a winning move
            if self.winning_comb(line, sign):
                idx = self.find_winning_index(line, sign)
                if move[4] == 'r':
                    return index, idx, sign
                else:
                    return idx, index, sign
            # looking for an empty square
            for i in range(1, len(line)):
                if line[i] == 0:
                    if move[4] == 'r':
                        return index, i, sign
                    else:
                        return i, index, sign
            if line[0] == 0:
                if move[4] == 'r':
                    return index, 0, sign
                else:
                    return 0, index, sign
        if move[4] == 'l_d' or move[4] == 'r_d':
            row_d, col_d = move[0]
            diag = move[1]
            # check if a line can become a winning move
            if self.winning_comb(diag, sign):
                idx = self.find_winning_index(diag, sign)
                if move[4] == 'l_d':
                    return idx, idx, sign
                else:
                    return idx, con.BOARD_COLS - 1 - idx, sign
            if move[4] == 'l_d':
                row, col = row_d + 1, col_d + 1
            else:
                row, col = row_d + 1, col_d - 1
            # looking for an empty square
            for i in range(1, len(diag)):
                if diag[i] == 0:
                    return row, col, sign
                row += 1
                col = col + 1 if move[4] == 'l_d' else col - 1
            if diag[0] == 0:
                return row_d, col_d, sign

    def winning_comb(self, ar: list, sign: int) -> bool:
        """Check if a line is a combination which quarantees a win"""
        if len(ar) != con.BOARD_ROWS:
            return False
        combs = [[0, sign, sign, 0, sign, 0], [0, sign, 0, sign, sign, 0]]
        if ar in combs:
            return True
        return False

    def find_winning_index(self, ar: list, sign: int) -> int:
        """Returns index of a list which should be marked to get an open four:
        (4 in a row with nothing on the ends)"""
        if ar == [0, sign, sign, 0, sign, 0]:
            return 3
        if ar == [0, sign, 0, sign, sign, 0]:
            return 2

    def find_empty_line(self) -> tuple:
        """Find an empty line on a board.
        Return position on this line and a sign"""
        array = self.board().table()
        signs = [1, 2]
        empty_lines = []
        for i in range(con.BOARD_ROWS):
            # find empty row, if such exists
            if self.board().empty_line(array[i]):
                sign = choice(signs)
                col = random.randint(1, con.BOARD_COLS-2)
                empty_lines.append((i, col, sign))
            col = make_column(array, i)
            # find empty column, if such exists
            if self.board().empty_line(col):
                sign = choice(signs)
                row = random.randint(1, con.BOARD_ROWS-2)
                empty_lines.append((row, i, sign))
        j = int((con.BOARD_ROWS/2 - 1)/2)
        # find empty diagonals, if such exist
        for index in range(-j, j+1):
            left, right = self.make_diagonals(array, index)
            left_d, l_coords = left
            right_d, r_coords = right
            if self.board().empty_line(left_d):
                sign = choice(signs)
                row_s, col_s = l_coords
                n = randint(1, con.BOARD_ROWS - 2 - max(row_s, col_s))
                row = row_s + n
                col = col_s + n
                empty_lines.append((row, col, sign))
            if self.board().empty_line(right_d):
                sign = choice(signs)
                row_s, col_s = r_coords
                n = randint(1, col_s - row_s - 1)
                row = row_s + n
                col = col_s - n
                empty_lines.append((row, col, sign))
        return sample(empty_lines, 1)
