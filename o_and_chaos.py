from classes.board import Board
from classes.game import Game
from classes.player import AiSupreme, LivePlayer, AiRandom


def order_and_chaos(args):
    game = Game()
    ai_type = args.ai_type
    board = Board()
    live_player = LivePlayer(board, args.role)
    if ai_type == 'random':
        ai = AiRandom(board)
    else:
        ai = AiSupreme(board)
    game = Game(board, live_player, ai)
    if ai_type == 'random':
        game.game_random()
    if ai_type == 'supreme':
        game.game_supreme()


if __name__ == '__main__':
    order_and_chaos()
