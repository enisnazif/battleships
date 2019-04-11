
from man.battleships.types.Board import Board
from man.battleships.types.Point import Point

def test_create_board():
    board = Board(10)

    assert board.get_size() == (10, 10)
    assert board.all(0)


def test_place_ships():
    pass


def test_shoot_valid():
    pass


def test_shoot_already_shot():
    board = Board(10)
    board.shoot(Point(1, 1))


def test_shoot_off_board():
    board = Board(10)
    board.shoot(Point(11, 11))

    # Expect exception
