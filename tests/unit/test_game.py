import random
import pytest
from man.battleships.types.Game import Game
from man.battleships.types.Bot import Bot
from man.battleships.types.Board import Board

# Set seed
random.seed(31)


def test_init_game_valid():
    game = Game(["SampleBot", "SampleBot"], 4)
    assert game.game_id == 4
    assert game.first_player.name == "SampleBot"
    assert game.second_player.name == "SampleBot"
    assert isinstance(game.first_player, Bot)
    assert isinstance(game.second_player, Bot)
    assert isinstance(game.first_player.board, Board)
    assert isinstance(game.second_player.board, Board)


def test_init_game_invalid():
    with pytest.raises(ModuleNotFoundError):
        Game(["BotThatDoesntExist", "SampleBot"], 4)
    with pytest.raises(ModuleNotFoundError):
        Game(["SampleBot", "BotThatDoesntExist"], 4)


def test_play_game():
    game = Game(["SampleBot", "SampleBot"], 4)
    game_data = game.play_game()

    assert len(game_data) == 8
    assert game_data["id"] == 4
    assert game_data["p1_name"] == "SampleBot"
    assert game_data["p2_name"] == "SampleBot"
    assert game_data["winner"] == "SampleBot"

    # Assert that the shots of the winner covered the ships of the loser
    assert set(game_data["p1_ship_placements"]).issubset(game_data["p2_shots"])
    assert not set(game_data["p2_ship_placements"]).issubset(game_data["p1_shots"])
