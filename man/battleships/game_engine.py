import numpy as np
from man.battleships.types.Board import Board, InvalidShipPlacementException, PointAlreadyShotException, ShotOffBoardException
from man.battleships.types.Ship import SHIP_ARRAY
from man.battleships.bots.SampleBot import SampleBot

GAME_CACHE = {}


def retry(f, n):




def get_game(game_id):
    return GAME_CACHE[game_id]

def play_game(player_1_bot, player_2_bot):
    """
    Play a single game between two bots and return the winner, along with the game history

    :param player_1_bot:
    :param player_2_bot:
    :return:
    """
    pass



def play_match(player_1_bot, player_2_bot, n_games=10, board_size=10):

    """ Plays 'n_games' between 'player_1_bot' and 'player_2_bot' and returns a dictionary of all games containing shots and the winner"""

    player_1_wins = 0
    player_2_wins = 0
    game_data = {}

    for game in range(n_games):
        player_1_board = Board(board_size)
        player_2_board = Board(board_size)

        # Load the players
        player_1 = player_1_bot
        player_2 = player_2_bot

        # Perform ship placement (Keep retrying until we get a correct placement)
        while True:
            try:
                for ship_placement in player_1.place_ships(SHIP_ARRAY):
                    player_1_board.place_ship(ship_placement)
            except InvalidShipPlacementException:
                continue

            break

        while True:
            try:
                for ship_placement in player_2.place_ships(SHIP_ARRAY):
                    player_2_board.place_ship(ship_placement)
            except InvalidShipPlacementException:
                continue

            break

        print(f'game {game}')
        while True:

            while True:
                try:
                    player_1_shot = player_1.get_shot(player_1_board)
                    player_2_board.shoot(player_1_shot)
                except PointAlreadyShotException:
                    continue
                except ShotOffBoardException:
                    continue
                break

            while True:
                try:
                    player_2_shot = player_2.get_shot(player_2_board)
                    player_1_board.shoot(player_2_shot)
                except PointAlreadyShotException:
                    continue
                except ShotOffBoardException:
                    continue
                break

            if player_1_board.is_game_won():
                player_1_wins += 1
                break

            if player_2_board.is_game_won():
                player_2_wins += 1
                break

    print('Scores:')
    print(f'{player_1.player_name}: {player_1_wins}')
    print(f'{player_2.player_name}: {player_2_wins}')
    print()
    print(f'Winner: Player {np.argmax([player_1_wins, player_2_wins]) + 1}')

    return game_data



if __name__ == '__main__':
    play_match(SampleBot('p1'), SampleBot('p2'))
