import click
import os
from flask import Flask, jsonify

from man.battleships.game_engine import play_match

app = Flask(__name__)


@app.route("/")
def landing_page():
    return "Welcome to Battleships!"


@app.route("/bot_names/")
def get_bot_names():

    # TODO: This is a horrible hack. Fix it
    bots_path = str('/'.join(os.path.realpath(__file__).split('/')[:-1])) + '/bots'
    bot_names = [bot.split('.')[0] for bot in os.listdir(bots_path) if bot != '__init__.py']

    return jsonify(bot_names)


@app.route("/play_match/<player_1>/<player_2>")
def do_play_match(player_1: str, player_2: str):
    """
    Plays a match of games between player_1 and player_2, and returns a json document summarising the games for visualisation
    :param player_1: str
    :param player_2: str
    :return:
    """

    return jsonify(play_match(player_1, player_2))


@click.command()
@click.option("--port", default=5678, help="Port to run on")
def run_server(port):
    app.run("0.0.0.0", port=port, threaded=False)


if __name__ == "__main__":
    run_server()
