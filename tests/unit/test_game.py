import random
import pytest
import time
import itertools
from game_types import Game, Bot, Point
from config import BOARD_SIZE, MAX_SHOT_TIME, MAX_PLACE_TIME

# Set seed
random.seed(31)


def test_init_game_valid():
    game = Game(["SampleBot", "ForwardBot"], 4)
    assert game.game_id == 4
    assert game.first_player.name == "SampleBot"
    assert game.second_player.name == "ForwardBot"
    assert isinstance(game.first_player, Bot)
    assert isinstance(game.second_player, Bot)


def test_init_game_invalid():
    with pytest.raises(ModuleNotFoundError):
        Game(["BotThatDoesntExist", "SampleBot"], 4)
    with pytest.raises(ModuleNotFoundError):
        Game(["SampleBot", "BotThatDoesntExist"], 4)


def test_play_game():
    game = Game(["BackwardBot", "ForwardBot"], 4)
    game_data = game.play_game()

    assert len(game_data) == 8
    assert game_data["id"] == 4
    assert game_data["p1_name"] == "BackwardBot"
    assert game_data["p2_name"] == "ForwardBot"
    assert game_data["winner"] == "BackwardBot"
    # assert game_data["p2_shots"] == list(Point(s[1], s[0]) for s in itertools.product(range(10), range(10)))
    # # assert game_data["p2_shots"] == set(Point(s[1], s[0]) for s in itertools.product(range(10), range(10)))

    # Assert that the shots of the winner covered the ships of the loser
    assert not set(game_data["p1_ship_placements"]).issubset(game_data["p2_shots"])
    assert set(game_data["p2_ship_placements"]).issubset(game_data["p1_shots"])


def test_timeout_place_ships():
    pass


def test_timeout_get_shot():
    game = Game(["SlowBot", "ForwardBot"], 4)
    game_data = game.play_game()


def test_max_retries_reached():
    pass
