from tqdm import tqdm
import click
from collections import Counter
from man.battleships.game_types import Game
from man.battleships.config import GAMES_PER_MATCH


def play_match(player_1_bot: str, player_2_bot: str, n_games=GAMES_PER_MATCH):
    """
    Plays 'n_games' between 'player_1_bot' and 'player_2_bot' and returns a dictionary of all game info

    :param player_1_bot:
    :param player_2_bot:
    :param n_games:
    :return:
    """

    pb_desc = f"Playing {n_games} games between {player_1_bot} and {player_2_bot}"

    game_data = [
        Game([player_1_bot, player_2_bot], game_id).play_game()
        for game_id in tqdm(range(n_games), desc=pb_desc)
    ]

    return game_data


@click.command()
@click.option("--n-games", default=1, help="Number of games to play", type=int)
@click.argument("player_1", default="ForwardBot")
@click.argument("player_2", default="BackwardBot")
def do_play_match(n_games, player_1, player_2):
    results = play_match(player_1, player_2, n_games=n_games)
    print()
    print(Counter([game["winner"] for game in results]))


if __name__ == "__main__":
    do_play_match()
