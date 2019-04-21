from abc import abstractmethod
from man.battleships.types import Ship, Board, Point, Orientation
from man.battleships.config import BOARD_SIZE
from typing import List


class Bot:
    def __init__(self):
        self._last_shot_status = (None, None)
        self._board = Board(BOARD_SIZE)

    @property
    def name(self):
        return str(type(self).__name__)

    @property
    def last_shot_status(self):
        return self._last_shot_status

    @property
    def board(self):
        return self._board

    @last_shot_status.setter
    def last_shot_status(self, value):
        self._last_shot_status = value

    @abstractmethod
    def place_ships(self, ships: List[Ship]):
        """ This method should return a valid ship placement on the board of the opponent. It is called once """
        pass

    @abstractmethod
    def get_shot(self):
        """ This method should return a valid shot on the board as an (x,y) coordinate. It is called by the game engine each round """
        pass

    def is_valid_ship_placement(
        self, ship: Ship, point: Point, orientation: Orientation
    ):

        placement = ship.get_points(point, orientation)

        in_board = [self.board.point_in_board(p) for p in placement]
        non_overlapping = [p not in self.board.get_ship_locations() for p in placement]

        return all(in_board) and all(non_overlapping)

    def is_valid_shot(self, point: Point):
        pass
