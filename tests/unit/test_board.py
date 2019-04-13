import pytest
from man.battleships.types.Board import (
    Board,
    PointAlreadyShotException,
    ShotOffBoardException,
    InvalidShipPlacementException,
)
from man.battleships.types.Point import Point
from man.battleships.types.Ship import Battleship, Destroyer, Orientation

from man.battleships.config import BOARD_SIZE


def test_create_board():
    board = Board(BOARD_SIZE)

    assert board.get_shot_locations() == set()
    assert board.get_ship_locations() == set()
    assert board.is_game_won() is False


def test_valid_place_ship():
    board = Board(BOARD_SIZE)
    board.place_ship(Battleship(), Point(4, 5), Orientation.Horizontal)

    assert board.get_ship_locations() == {Point(4, 5), Point(5, 5), Point(6, 5)}


def test_invalid_place_ship():
    board = Board(BOARD_SIZE)

    with pytest.raises(InvalidShipPlacementException):
        board.place_ship(
            Battleship(), Point(BOARD_SIZE - 1, BOARD_SIZE - 1), Orientation.Vertical
        )


def test_shoot_valid():
    board = Board(BOARD_SIZE)

    board.shoot(Point(7, 4))
    board.shoot(Point(0, 14))

    assert board.get_shot_locations() == {Point(7, 4), Point(0, 14)}


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

    board.place_ship(Destroyer(), Point(5, 1), Orientation.Horizontal)

    board.shoot(Point(5, 1))
    board.shoot(Point(5, 2))
    board.shoot(Point(5, 3))

    assert board.is_game_won() is False

    board.shoot(Point(6, 2))
    board.shoot(Point(7, 2))
    board.shoot(Point(7, 1))
    board.shoot(Point(7, 3))

    assert board.is_game_won() is True

    board.shoot(Point(11, 11))

    assert board.is_game_won() is True


def test_cannot_edit_board():
    board = Board(BOARD_SIZE)

    #  AttributeError: 'frozenset' object has no attribute 'add'
    with pytest.raises(AttributeError):
        board._board.add(Point(4, 4))


def test_cannot_edit_ships():
    board = Board(BOARD_SIZE)

    #  AttributeError: 'frozenset' object has no attribute 'add'
    with pytest.raises(AttributeError):
        board._ship_locations.add(Point(4, 4))


def test_cannot_edit_shots():
    board = Board(BOARD_SIZE)

    #  AttributeError: 'frozenset' object has no attribute 'add'
    with pytest.raises(AttributeError):
        board._shot_locations.add(Point(4, 4))
