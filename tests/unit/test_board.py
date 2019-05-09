import pytest
from man.battleships.game_types.Board import (
    Board,
    PointAlreadyShotException,
    ShotOffBoardException,
    InvalidShipPlacementException,
)
from man.battleships.game_types.Point import Point
from man.battleships.game_types.Ship import Battleship, Destroyer, Orientation

from man.battleships.config import BOARD_SIZE


def test_create_board():
    board = Board(BOARD_SIZE)

    assert board.shot_locations == set()
    assert board.all_ship_locations == set()
    assert board.is_board_lost() is False


def test_valid_place_ship():
    board = Board(BOARD_SIZE)
    board.place_ship(Battleship(), Point(4, 5), Orientation.Horizontal)

    assert board.all_ship_locations == {Point(4, 5), Point(5, 5), Point(6, 5)}


def test_invalid_place_ship():
    board = Board(BOARD_SIZE)

    with pytest.raises(InvalidShipPlacementException):
        board.place_ship(
            Battleship(), Point(BOARD_SIZE - 1, BOARD_SIZE - 1), Orientation.Vertical
        )


def test_shoot_valid():
    board = Board(BOARD_SIZE)

    board.shoot(Point(7, 4))
    board.shoot(Point(0, BOARD_SIZE-1))

    assert board.shot_locations == {Point(7, 4), Point(0, BOARD_SIZE-1)}


def test_shoot_invalid_already_shot():
    board = Board(BOARD_SIZE)

    board.shoot(Point(1, 1))
    board.shoot(Point(5, 2))

    with pytest.raises(PointAlreadyShotException):
        board.shoot(Point(1, 1))


def test_shoot_invalid_off_board():
    board = Board(BOARD_SIZE)

    with pytest.raises(ShotOffBoardException):
        board.shoot(Point(BOARD_SIZE, BOARD_SIZE))


def test_game_is_won():
    board = Board(BOARD_SIZE)

    assert board.is_board_lost() is False

    board.place_ship(Destroyer(), Point(5, 1), Orientation.Horizontal)

    assert board.is_board_lost() is False

    board.shoot(Point(5, 1))
    board.shoot(Point(5, 2))
    board.shoot(Point(5, 3))

    assert board.is_board_lost() is False

    board.shoot(Point(6, 2))
    board.shoot(Point(7, 2))
    board.shoot(Point(7, 1))
    board.shoot(Point(7, 3))

    assert board.is_board_lost() is True

    board.shoot(Point(BOARD_SIZE-1, BOARD_SIZE-1))

    assert board.is_board_lost() is True
