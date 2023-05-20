# dimensions
WIDTH = 700
HEIGHT = WIDTH
BOARD_ROWS = 6
BOARD_COLS = 6
SQUARE_SIZE = WIDTH//BOARD_COLS
LINE_WIDTH = WIDTH//60
SIGN_SPACE = WIDTH//7
SPACE = SQUARE_SIZE//4
CROSS_WIDTH = WIDTH//25
RECT_INDENT = LINE_WIDTH//2
CIRCLE_RADIUS = SQUARE_SIZE//2 - SQUARE_SIZE//6
CIRCLE_WIDTH = WIDTH//40
WINNING_WIDTH = WIDTH//50
DIAGONAL_INDENT = WIDTH//28
ASCENDING_INDENT = WIDTH//23
END_INDENT = WIDTH//31
FONT_SIZE = WIDTH//10
TEXT_INDENT_X_1 = WIDTH//3
TEXT_INDENT_X_2 = WIDTH//4.6
TEXT_INDENT_Y_1 = (HEIGHT + SIGN_SPACE)//3
TEXT_INDENT_Y_2 = TEXT_INDENT_Y_1 + WIDTH//10
# colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CROSS_COLOR = (66, 66, 66)
WHITE = (255, 255, 255)
CIRCLE_COLOR = (239, 231, 200)
RECT_CIRCLE_COLOR = (66, 66, 66)
# list representing screen
SCREEN = [
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
]
# a list with moves for Order made using pairing strategy
CHAOS_BOARD = [
    [(5, 5), (4, 5), (0, 3), (0, 2), (4, 0), (5, 0)],
    [(5, 4), (3, 1), (1, 4), (3, 3), (1, 2), (5, 1)],
    [(3, 0), (2, 3), (4, 2), (2, 1), (4, 4), (3, 5)],
    [(2, 0), (1, 1), (3, 4), (1, 3), (3, 2), (2, 5)],
    [(0, 4), (4, 3), (2, 2), (4, 1), (2, 4), (0, 1)],
    [(0, 5), (1, 5), (5, 3), (5, 2), (1, 0), (0, 0)],
]
