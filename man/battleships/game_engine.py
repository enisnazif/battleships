import numpy as np
from tqdm import tqdm
from collections import Counter
from man.battleships.types.Board import Board, InvalidShipPlacementException, PointAlreadyShotException, ShotOffBoardException
from man.battleships.types.Ship import ships_to_place
from man.battleships.bots.SampleBot import SampleBot
from man.battleships.config import BOARD_SIZE, GAMES_PER_MATCH

GAME_CACHE = {}


def retry_dec(exception, max_retries=5):
    """
    Retry decorator that retries the wrapped function a maximum of 'max_retries' times if 'exception' is raised

    :param exception:
    :param max_retries:
    :return:
    """

    def deco_retry(f):
        def f_retry(*args, **kwargs):
            n_retries = 0
            while n_retries < max_retries:
                try:
                    f(*args, **kwargs)
                except exception:
                    n_retries += 1
                    continue
                break

        return f_retry

    return deco_retry


def get_game(game_id):
    return GAME_CACHE[game_id]


def play_game(player_1_bot, player_2_bot, game_id):
    """
    Play a single game between two bots and return the winner, along with the game history

    :param player_1_bot:
    :param player_2_bot:
    :return:
    """

    # Define boards
    player_1_board = Board(BOARD_SIZE)
    player_2_board = Board(BOARD_SIZE)

    # Load the players
    player_1 = player_1_bot
    player_2 = player_2_bot

    # Perform ship placement (Keep retrying until we get a correct placement)
    place_ships(player_1, player_1_board)
    place_ships(player_2, player_2_board)

    # Game loop - get shots until a player wins
    while True:

        do_shot(player_1, player_1_board, player_2_board)
        do_shot(player_2, player_2_board, player_1_board)

        if player_1_board.is_game_won():
            winner = player_1.get_bot_name()
            break

        if player_2_board.is_game_won():
            winner = player_2.get_bot_name()
            break

    return {'winner': winner,
            'p1_shots': [],
            'p1_ship_placements': [],
            'p2_shots': [],
            'p2_ship_placements': []
            }


@retry_dec(InvalidShipPlacementException)
def place_ships(player, board):
    player_ship_placements = player.place_ships(ships_to_place())

    for ship, point, orientation in player_ship_placements:
        board.place_ship(ship, point, orientation)


@retry_dec(ShotOffBoardException)
@retry_dec(PointAlreadyShotException)
def do_shot(player, player_board, board_to_shoot):
    player_shot = player.get_shot(player_board)
    board_to_shoot.shoot(player_shot)


def play_match(player_1_bot, player_2_bot, n_games=GAMES_PER_MATCH):
    """ Plays 'n_games' between 'player_1_bot' and 'player_2_bot' and returns a dictionary of all games containing shots and the winner"""

    game_data = []

    for game_id in tqdm(range(n_games), desc='Playing games'):
        game_data.append(play_game(player_1_bot, player_2_bot, game_id))

    return game_data


def process_game_data(data):
    """

    :param data:
    :return:
    """
    pass


if __name__ == '__main__':
    play_match(SampleBot(), SampleBot())
