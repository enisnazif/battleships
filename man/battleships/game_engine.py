from tqdm import tqdm
from man.battleships.types.Game import Game
from man.battleships.config import GAMES_PER_MATCH


# TODO: should a player own its own board?
# TODO: docstrings / type annotations
# TODO: Handle failures af
# TODO: Handle max move time


def play_match(player_1_bot: str, player_2_bot: str, n_games=GAMES_PER_MATCH):
    """
    Plays 'n_games' between 'player_1_bot' and 'player_2_bot' and returns a dictionary of all game info

    :param player_1_bot:
    :param player_2_bot:
    :param n_games:
    :return:
    """

    pb_desc = f"Playing {n_games} games between {player_1_bot} and {player_2_bot}"
    game_data = [Game(player_1_bot, player_1_bot, game_id).play_game() for game_id in tqdm(range(n_games), desc=pb_desc)]

    return game_data
