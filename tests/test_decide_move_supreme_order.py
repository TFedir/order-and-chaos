from classes.board import Board
from classes.player import AiSupreme


def test_decide_move_supreme():
    board = Board()
    board.mark_square(2, 4, 1)
    board.mark_square(3, 3, 1)
    board.mark_square(5, 1, 1)
    ai = AiSupreme(board)
    moves = [(1, 5, 1), (4, 2, 1)]
    assert ai.decide_move_order() in moves


def test_decide_move_border_case_row():
    board = Board()
    board.mark_square(0, 5, 1)
    ai = AiSupreme(board)
    moves = [(0, 1, 1), (1, 5, 1), (1, 4, 1)]
    ai_move = ai.decide_move_order()
    assert ai_move in moves


def test_decide_move_border_case_col():
    board = Board()
    board.mark_square(5, 5, 1)
    ai = AiSupreme(board)
    restricted = (0, 5, 1)
    assert ai.decide_move_order() != restricted


def test_decide_move_corner():
    board = Board()
    board.mark_square(5, 0, 1)
    ai = AiSupreme(board)
    restricted = (0, 5, 1)
    assert ai.decide_move_order() != restricted
