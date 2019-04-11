from flask import Flask
from man.battleships.game_engine import play_round, get_game

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/play_round')
def play_round():
    return play_round()


@app.route('/get_game/<game_id>')
def get_game(game_id):
    """ Returns a complete game, including ship placements and all shots, ready for visualisation"""

    return get_game(game_id)


if __name__ == '__main__':
    app.run()
