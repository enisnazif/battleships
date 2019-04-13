import importlib
import click
from flask import Flask, jsonify
from man.battleships.game_engine import play_match

app = Flask(__name__)


@app.route('/')
def landing_page():
    return "Welcome to Battleships!"


@app.route('/play_match/<player_1>/<player_2>')
def do_play_match(player_1, player_2):
    """
    Plays a match of games between player_1 and player_2, and returns a json document summarising the games for visualisation
    :param player_1: str
    :param player_2: str
    :return:
    """

    bots_path = 'man.battleships.bots'

    player_1_bot = importlib.import_module(f'{bots_path}.{player_1}')
    player_2_bot = importlib.import_module(f'{bots_path}.{player_2}')

    return jsonify(play_match(getattr(player_1_bot, player_1)(), getattr(player_2_bot, player_2)()))


@app.route('/get_game/<game_id>')
def get_game(game_id):
    """ Returns a complete game, including ship placements and all shots, ready for visualisation"""

    return get_game(game_id)


@click.command()
@click.option('--port', default=5555, help='Port to run on')
def run_server(port):
    app.run('0.0.0.0', port=port)


if __name__ == '__main__':
    run_server()
