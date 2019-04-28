import click
import os
from flask import Flask, jsonify
from flask_cors import CORS

from man.battleships.play_game import play_match
from man.battleships.web.formatter import format_match_output

app = Flask(__name__)
CORS(app)


@app.route("/")
def landing_page():
    return "Welcome to Battleships!"


@app.route("/bot_names/")
def get_bot_names():

    # TODO: This is a horrible hack. Fix it
    bots_path = str(os.sep.join(os.path.realpath(__file__).split(os.sep)[:-1])) + os.sep + 'bots'
    bot_names = [bot.split('.')[0] for bot in os.listdir(bots_path) if bot not in ['__init__.py', '__pycache__']]

    return jsonify(bot_names)


@app.route("/play_game/<player_1>/<player_2>")
def do_play_game(player_1: str, player_2: str):
    return jsonify(format_match_output(play_match(player_1, player_2, 1)))


@app.route("/play_match/<player_1>/<player_2>/<games>")
def do_play_match(player_1: str, player_2: str, games: int):
    """
    Plays a match of games between player_1 and player_2, and returns a json document summarising the games for visualisation
    :param player_1: str
    :param player_2: str
    :param games: int
    :return:
    """

    return jsonify(play_match(player_1, player_2, n_games=games))


@click.command()
@click.option("--port", default=5678, help="Port to run on")
def run_server(port):
    app.run("0.0.0.0", port=port, threaded=False)


if __name__ == "__main__":
    run_server()
