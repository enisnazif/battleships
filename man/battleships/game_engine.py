from tqdm import tqdm
from man.battleships.types.Game import Game
from man.battleships.config import BOARD_SIZE, GAMES_PER_MATCH


# TODO: should a player own its own board?
# TODO: docstrings / type annotations
# TODO: Handle failures af
# TODO: Handle max move time


def play_match(player_1_bot, player_2_bot, n_games=GAMES_PER_MATCH):
    """ Plays 'n_games' between 'player_1_bot' and 'player_2_bot' and returns a dictionary of all game info"""

    pb_desc = f"Playing {n_games} games between {player_1_bot} and {player_2_bot}"

    game_data = []

    for game_id in tqdm(range(n_games), desc=pb_desc):
        g = Game(player_1_bot, player_1_bot, game_id)
        game_data.append(g.play_game())

    return game_data
