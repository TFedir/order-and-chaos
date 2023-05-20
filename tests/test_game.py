from classes.board import Board
from classes.game import Game
from classes.player import LivePlayer, AiSupreme


def test_game_won_row():
    board = Board()
    player = LivePlayer(board, 'order')
    ai = AiSupreme(board)
    game = Game(board, player, ai)
    for i in range(0, 5):
        board.mark_square(0, i, 1)
    assert game.game_won() is True


def test_game_won_column():
    board = Board()
    player = LivePlayer(board, 'order')
    ai = AiSupreme(board)
    game = Game(board, player, ai)
    for i in range(0, 5):
        board.mark_square(i, 0, 1)
    assert game.game_won() is True


def test_game_won_column_end():
    board = Board()
    player = LivePlayer(board, 'order')
    ai = AiSupreme(board)
    game = Game(board, player, ai)
    for i in range(1, 6):
        board.mark_square(i, 0, 1)
    assert game.game_won() is True


def test_game_not_won():
    board = Board()
    player = LivePlayer(board, 'order')
    ai = AiSupreme(board)
    game = Game(board, player, ai)
    assert game.game_won() is False


def test_game_won_diagonal():
    board = Board()
    player = LivePlayer(board, 'order')
    ai = AiSupreme(board)
    game = Game(board, player, ai)
    for i in range(0, 5):
        board.mark_square(i, i, 1)
    assert game.game_won() is True


def test_game_won_diagonal_up():
    board = Board()
    player = LivePlayer(board, 'order')
    ai = AiSupreme(board)
    game = Game(board, player, ai)
    for i in range(0, 5):
        board.mark_square(i, i+1, 1)
    assert game.game_won() is True


def test_game_won_asc_diagonal():
    board = Board()
    player = LivePlayer(board, 'order')
    ai = AiSupreme(board)
    game = Game(board, player, ai)
    for i in range(0, 5):
        board.mark_square(5-i, i, 1)
    assert game.game_won() is True


def test_game_won_asc_diagonal_up():
    board = Board()
    player = LivePlayer(board, 'order')
    ai = AiSupreme(board)
    game = Game(board, player, ai)
    for i in range(0, 5):
        board.mark_square(4-i, i, 1)
    assert game.game_won() is True


def test_game_won_asc_diagonal_down():
    board = Board()
    player = LivePlayer(board, 'order')
    ai = AiSupreme(board)
    game = Game(board, player, ai)
    for i in range(0, 5):
        board.mark_square(5-i, i+1, 1)
    assert game.game_won() is True
