import constants.const as con
from classes.board import Board
from classes.player import Player
import pygame
from support_functions.chaos_won_first_stage import (
    check_rows, check_columns, check_diagonals, count_diagonals)
from support_functions.chaos_won_second_stage import second_stage


class Game:
    """Class representing game, responsible for realization of rounds
    and communication between different classes"""
    def __init__(self, board: Board = None, player: Player = None,
                 ai=None) -> None:
        self._sign_picked = False
        self._sign = 0
        self._current_player = player
        self._player = player
        self._ai = ai
        self._board = board
        self._previous_move = None

    def current_player(self):
        """Return ai or player, based on whose move it is"""
        return self._current_player

    def sign_picked(self) -> bool:
        """Return True if sign was picked, else False"""
        return self._sign_picked

    def sign(self) -> int:
        """Return sign which was last placed by Player"""
        return self._sign

    def ai(self):
        return self._ai

    def player(self):
        return self._player

    def board(self) -> Board:
        return self._board

    def previous_move(self) -> tuple:
        """Return Player's last move"""
        return self._previous_move

    def set_previous_move(self, row: int, col: int) -> None:
        self._previous_move = (row, col)

    def change_current_player(self) -> None:
        """Change current player on it's enemy"""
        player = self.player()
        ai = self.ai()
        current = self.current_player()
        self._current_player = ai if current == player else player

    def set_sign(self, new_sign: int) -> None:
        self._sign = new_sign

    def set_sign_picked(self) -> None:
        self._sign_picked = not self._sign_picked

    def round(self, event: pygame.event) -> None:
        """
        Implementation of a round by Player.
        It consists out of 2 parts: picking a sign and placing it
        """
        if self.current_player() == self.player():
            # reading coordinates out of a mouseclick
            mouseX = event.pos[0]
            mouseY = event.pos[1]
            # converting coordinates to values in range(0, con.BOARD_ROWS)
            row = int(mouseY // con.SQUARE_SIZE)
            col = int(mouseX // con.SQUARE_SIZE)
            board_clicked = row in range(0, 6) and col in range(0, 6)
            # picking a sign a player will mark a square with
            if row == 6 and col in [2, 3]:
                self.set_sign(1 if col == 2 else 2)
                if not self.sign_picked():
                    self.set_sign_picked()
            # marking a sign, remembering the move and changing current player
            elif board_clicked and self.sign_picked():
                if self.board().available_square(row, col):
                    self.board().mark_square(row, col, self.sign())
                    self.change_current_player()
                    self.set_sign_picked()
                    self.set_previous_move(row, col)

    def make_move_random(self) -> None:
        """Making a random move with AI"""
        row, col, sign = self.ai().decide_move_random()
        self.board().mark_square(row, col, sign)
        self.change_current_player()

    def game_won(self) -> bool:
        """
        Checking if game is won for Order: are there 5 like pieces in a row.
        If game is won calling draw_winning_line().
        """
        def check_same(line: list) -> bool:
            """Checking if there are 5 like pieces in a row in a line"""
            if len(line) == con.BOARD_COLS:
                if line.count(line[1]) == con.BOARD_COLS:
                    return False
                sublines = [line[0:con.BOARD_COLS-1], line[1:con.BOARD_COLS]]
            else:
                sublines = [line]
            for subline in sublines:
                not_empty = subline[1] != 0
                if subline.count(subline[1]) == len(subline) and not_empty:
                    return True
            return False

        table = self.board().table()
        for i, row in enumerate(table):
            if check_same(row):
                self.board().draw_winning_line(i, 'r')
                return True
        for i in range(con.BOARD_COLS):
            column_list = [element[i] for element in table]
            if check_same(column_list):
                self.board().draw_winning_line(i, 'c')
                return True
            amount_d = count_diagonals(con.BOARD_ROWS, con.BOARD_ROWS-1)
            j = int((amount_d/2 - 1)/2)
            for i in range(-j, j+1):
                left, right = self.ai().make_diagonals(table, i)
                left_diagonal, l_coords = left
                right_diagonal, r_coords = right
                if check_same(left_diagonal):
                    self.board().draw_winning_line(l_coords, 'l_d')
                    return True
                if check_same(right_diagonal):
                    self.board().draw_winning_line(r_coords, 'r_d')
                    return True
        return False

    def game_not_ended(self) -> bool:
        """Checking if game is won either for Chaos or Order"""
        return not self.game_won() and not self.game_won_chaos()

    def game_random(self):
        """Game match when AI is random"""
        run = True
        self.prepare_players()
        self.board().prepare_screen()
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if (event.type == pygame.MOUSEBUTTONDOWN and
                        self.game_not_ended()):
                    self.round(event)
                    self.board().draw_figures()
                    pygame.display.update()
                if (self.current_player() == self.ai() and
                        self.game_not_ended()):
                    pygame.time.wait(400)
                    self.make_move_random()
                self.board().draw_figures()
                pygame.display.update()
            if self.game_won() or self.game_won_chaos():
                pygame.display.update()
                pygame.time.wait(1500)
                break
        if self.game_won():
            if self.board().show_game_won('Order wins'):
                self.restart()
        elif self.game_won_chaos():
            if self.board().show_game_won('Chaos wins'):
                self.restart()
        pygame.quit()

    def game_won_chaos(self) -> bool:
        """Check if there are combinations left to play for Order"""
        if self.check_empty_lines():
            return False
        else:
            return second_stage(self.board().table())

    def check_empty_lines(self) -> bool:
        """Check if there are empty lines on the board"""
        array = self.board().table()
        if check_rows(array):
            return True
        if check_columns(array):
            return True
        if check_diagonals(array, 5):
            return True
        return False

    def prepare_players(self) -> None:
        """Changing current player, so Order makes a move first"""
        if (
            self.player().role() == 'chaos'
            and self.current_player() == self.player()
        ) or (self.player().role() == 'order'
              and self.current_player() == self.ai()
              ):
            self.change_current_player()
            self._previous_move = None

    def game_supreme(self) -> None:
        """Game match when AI is supreme"""
        run = True
        self.prepare_players()
        self.board().prepare_screen()
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if (event.type == pygame.MOUSEBUTTONDOWN and
                        self.game_not_ended()):
                    self.round(event)
                    self.board().draw_figures()
                    pygame.display.update()
                if (self.current_player() == self.ai() and
                        self.game_not_ended()):
                    pygame.time.wait(400)
                    if self.player().role() == 'chaos':
                        self.make_move_supreme_order()
                        self.board().draw_figures()
                        pygame.display.update()
                    else:
                        self.make_move_supreme_chaos()
                        self.board().draw_figures()
                        pygame.display.update()
                self.board().draw_figures()
                pygame.display.update()
            if self.game_won() or self.game_won_chaos():
                pygame.display.update()
                pygame.time.wait(1500)
                break
        if self.game_won():
            if self.board().show_game_won('Order wins'):
                self.restart()
        elif self.game_won_chaos():
            if self.board().show_game_won('Chaos wins'):
                self.restart()
        pygame.quit()

    def make_move_supreme_chaos(self) -> None:
        """Making a supreme move with AI as Chaos"""
        row, col, sign = self.ai().decide_move_chaos(self.previous_move(),
                                                     self.sign())
        self.board().mark_square(row, col, sign)
        self.change_current_player()

    def make_move_supreme_order(self) -> None:
        """Making a supreme move with AI as Order"""
        row, col, sign = self.ai().decide_move_order()
        self.board().mark_square(row, col, sign)
        self.change_current_player()

    def restart(self) -> None:
        """
        Restarting the game by cleaning the board and calling game functions
        """
        self.board().clean_board()
        if self.ai().name() == 'random':
            self.game_random()
        if self.ai().name() == 'supreme':
            self.game_supreme()
