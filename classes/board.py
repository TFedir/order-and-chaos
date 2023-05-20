import pygame
import constants.const as con
from support_functions.chaos_won_second_stage import make_column
from support_functions.chaos_won_first_stage import array_for_diagonal


class Board:
    """A class representing the board responsible for the drawing of
    figures and the grid"""
    def __init__(self):
        self._screen = pygame.display.set_mode(
            (con.WIDTH,
             con.HEIGHT+con.SIGN_SPACE)
            )
        self._caption = pygame.display.set_caption('Order and Chaos')
        self._table = con.SCREEN

    def screen(self) -> pygame.display:
        return self._screen

    def table(self) -> list:
        """Return list which represents the board"""
        return self._table

    def fill_screen(self, color: tuple) -> None:
        """Fill screen with color"""
        self._screen.fill(color)

    def draw_grid(self) -> None:
        """Draw the grid on which the game is played"""
        def draw_horizontal_lines(screen, color):
            START_X, END_X, ln = 0, con.WIDTH, con.LINE_WIDTH
            for Y in range(0, con.WIDTH+con.SQUARE_SIZE, con.SQUARE_SIZE):
                pygame.draw.line(screen, color, (START_X, Y), (END_X, Y), ln)

        def draw_vertical_lines(screen, color):
            START_Y, END_Y, ln = 0, con.WIDTH, con.LINE_WIDTH
            for X in range(0, con.WIDTH + con.SQUARE_SIZE, con.SQUARE_SIZE):
                pygame.draw.line(screen, color, (X, START_Y), (X, END_Y), ln)

        screen, color = self.screen(), con.LINE_COLOR
        draw_horizontal_lines(screen, color)
        draw_vertical_lines(screen, color)

    def mark_square(self, row: int, col: int, sign: int) -> None:
        """Mark square in row column with a sign"""
        self.table()[row][col] = sign

    def available_square(self, row: int, col: int) -> bool:
        """Check if a square in row column if empty"""
        return self.table()[row][col] == 0

    def empty_line(self, line: list) -> bool:
        """
        Check if there are len(line) - 1 empty elements in line.
        Expected that line is not empty
        """
        counter = 0
        for i in range(len(line)):
            if counter == (len(line) - 1) and line[i] == 0:
                return True
            if line[i] == 1:
                counter = 0
            else:
                counter += 1
        return False

    def clean_board(self) -> None:
        """Mark all squares on the board as empty"""
        for i in range(con.BOARD_ROWS):
            for j in range(con.BOARD_COLS):
                self.mark_square(i, j, 0)

    def draw_figures(self) -> None:
        """Draw figures based on the board elements"""
        for row in range(0, con.BOARD_ROWS):
            for col in range(0, con.BOARD_COLS):
                if self.table()[row][col] == 1:
                    self.draw_x(row, col)
                elif self.table()[row][col] == 2:
                    self.draw_o(row, col)

    def draw_x(self, row: int, col: int) -> None:
        """Draw an X on the screen in [row] [col] square"""

        def count_fist_indent(number: int) -> int:
            """Count indent, so X will be symmetrical"""
            return number * con.SQUARE_SIZE + con.SPACE

        def count_second_indent(number: int) -> int:
            """Count indent, so X will be symmetrical"""
            return number * con.SQUARE_SIZE + con.SQUARE_SIZE - con.SPACE

        start_x = count_fist_indent(col)
        start_y = count_second_indent(row)
        end_x = count_second_indent(col)
        end_y = count_fist_indent(row)
        ascend_start = (start_x, start_y)
        ascend_end = (end_x, end_y)
        descend_start = (start_x, end_y)
        descend_end = (end_x, start_y)
        # draw ascending diagonal
        pygame.draw.line(self.screen(), con.CROSS_COLOR,
                         ascend_start, ascend_end, con.CROSS_WIDTH)
        # draw decending diagonal
        pygame.draw.line(self.screen(), con.CROSS_COLOR,
                         descend_start, descend_end, con.CROSS_WIDTH)

    def draw_o(self, row: int, col: int) -> None:
        """Draw an O on the screen in [row] [col] square"""
        def count_centre(number: int) -> int:
            """Count the centre for circle"""
            return number * con.SQUARE_SIZE + con.SQUARE_SIZE//2

        screen, r, width = self.screen(), con.CIRCLE_RADIUS, con.CIRCLE_WIDTH
        color = con.CIRCLE_COLOR
        pygame.draw.circle(screen, color,
                           (int(count_centre(col)), int(count_centre(row))),
                           r, width)

    def draw_rect_for_sign(self) -> None:
        """Draw a rectangle used to pick signs"""
        for col in range(2, 4):
            x = col * con.SQUARE_SIZE
            y = 6 * con.SQUARE_SIZE + con.RECT_INDENT
            # draw rectangle
            pygame.draw.rect(self.screen(), con.BG_COLOR,
                             (x, y, con.SQUARE_SIZE, con.SQUARE_SIZE))
            if col == 2:
                # draw an X inside rectangle
                self.draw_x(con.BOARD_ROWS, col)
            else:
                # draw an O inside rectangle
                self.draw_o(con.BOARD_ROWS, col)
        screen, color, ln = self.screen(), con.LINE_COLOR, con.LINE_WIDTH
        START_Y, END_Y, X = 0, con.WIDTH + con.SQUARE_SIZE, 3 * con.SQUARE_SIZE
        pygame.draw.line(screen, color, (X, START_Y), (X, END_Y), ln)

    def prepare_screen(self) -> None:
        """
        Prepare screen for the game: fill the screen, draw grid and
        a rectangle for signs at the bottom
        """
        self.screen()
        self.fill_screen(con.BG_COLOR)
        self.draw_grid()
        self.draw_rect_for_sign()

    def draw_winning_line(self, index: int, pos: str) -> None:
        """
        Draw winning line based on index which indicates where to start and
        pos which indicates what type of line it is: row, column,
        left or right diagonal.
        """
        screen = self.screen()
        line = self.make_line(index, pos)
        start = self.decide_start(line)
        color = con.CROSS_COLOR if line[1] == 1 else con.CIRCLE_COLOR
        if not (pos == 'l_d' or pos == 'r_d'):
            start_y = index * con.SQUARE_SIZE + con.SQUARE_SIZE/2
            start_x = 10 + con.SQUARE_SIZE if start == 0 else 10
            end_x = con.WIDTH - 10 - (con.SQUARE_SIZE * start)
        if pos == 'r':
            pygame.draw.line(screen, color, (start_x, start_y),
                             (end_x, start_y), con.WINNING_WIDTH)
        elif pos == 'c':
            pygame.draw.line(screen, color, (start_y, start_x),
                             (start_y, end_x), con.WINNING_WIDTH)
        elif pos == 'l_d':
            self.draw_left_winning_diagonal(line, color, index, start)
        elif pos == 'r_d':
            self.draw_right_winning_diagonal(line, color, index, start)

    def draw_left_winning_diagonal(self, line: list, color: tuple,
                                   index: int, start: int) -> None:
        """Draw left(descending) winning diagonal"""
        screen = self.screen()
        a, b = index
        if len(line) == con.BOARD_ROWS:
            if start == 0:
                start_x = con.DIAGONAL_INDENT + con.SQUARE_SIZE
                start_y = con.DIAGONAL_INDENT + con.SQUARE_SIZE
            else:
                start_x = con.DIAGONAL_INDENT
                start_y = con.DIAGONAL_INDENT
            end_x = con.WIDTH - con.DIAGONAL_INDENT - con.SQUARE_SIZE * start
            end_y = con.HEIGHT - con.DIAGONAL_INDENT - con.SQUARE_SIZE * start
        else:
            end_x = con.WIDTH - con.DIAGONAL_INDENT - con.SQUARE_SIZE * a
            end_y = con.HEIGHT - con.DIAGONAL_INDENT - con.SQUARE_SIZE * b
            start_x = con.DIAGONAL_INDENT + con.SQUARE_SIZE * b
            start_y = con.DIAGONAL_INDENT + con.SQUARE_SIZE * a
        pygame.draw.line(screen, color, (start_x, start_y),
                         (end_x, end_y), con.CROSS_WIDTH)

    def draw_right_winning_diagonal(self, line: list, color: tuple,
                                    index: int, start: int) -> None:
        """Draw right(ascending) winning diagonal"""
        screen = self.screen()
        a, b = index
        b = con.BOARD_COLS - 1 - b
        indent, indent_end = con.ASCENDING_INDENT, con.END_INDENT
        if len(line) == con.BOARD_ROWS:
            if start == 1:
                start_x = con.WIDTH - indent
                start_y = con.DIAGONAL_INDENT
            else:
                start_x = con.WIDTH - con.SQUARE_SIZE - indent
                start_y = con.DIAGONAL_INDENT + con.SQUARE_SIZE
            end_x = indent_end + con.SQUARE_SIZE * start
            end_y = con.HEIGHT - con.DIAGONAL_INDENT - con.SQUARE_SIZE * start
        else:
            end_x = indent_end + con.SQUARE_SIZE * a
            end_y = con.HEIGHT - con.DIAGONAL_INDENT - con.SQUARE_SIZE * b
            start_x = con.WIDTH - indent - con.SQUARE_SIZE * b
            start_y = con.DIAGONAL_INDENT + con.SQUARE_SIZE * a
        pygame.draw.line(screen, color, (start_x, start_y),
                         (end_x, end_y), con.CROSS_WIDTH)

    def make_line(self, index: int, pos: str) -> list:
        """
        Make a list representing the line based on index(starting position
        of line) and pos(type of line)
        """
        table = self.table()
        if pos == 'r':
            line = table[index]
        elif pos == 'c':
            line = make_column(table, index)
        elif pos == 'l_d':
            a, b = index
            line = array_for_diagonal(table, a, b, 'right')
        elif pos == 'r_d':
            c, d = index
            line = array_for_diagonal(table, c, d, 'left')
        return line

    def decide_start(self, line: list) -> int:
        """Decides from what starting index the winning line will be drawn"""
        if len(line) == con.BOARD_ROWS:
            if line[0:con.BOARD_COLS - 1].count(line[0]) == con.BOARD_COLS - 1:
                start = 1
            elif line[1:con.BOARD_COLS].count(line[1]) == con.BOARD_COLS - 1:
                start = 0
        else:
            start = 0
        return start

    def show_game_won(self, msg: str) -> bool:
        """Show the restart window. If r is pressed, return True."""
        pygame.init()
        self.fill_screen(con.BG_COLOR)
        font = pygame.font.Font('Think Big.ttf', con.FONT_SIZE)
        restart = 'Press R to restart'
        text = font.render(msg, True, (255, 255, 255))
        self.screen().blit(text, (con.TEXT_INDENT_X_1,
                           con.TEXT_INDENT_Y_1))
        text = font.render(restart, True, (255, 255, 255))
        self.screen().blit(text, (con.TEXT_INDENT_X_2,
                           con.TEXT_INDENT_Y_2))
        pygame.display.update()
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return True
        return False
