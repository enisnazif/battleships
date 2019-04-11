import numpy as np
from man.battleships.types.Point import Point
from man.battleships.types.Ship import Ship


class PointAlreadyShotException(Exception):
    pass


class ShotOffBoardException(Exception):
    pass


class InvalidShipPlacementException(Exception):
    pass


class Board:

    def __init__(self, board_size):
        self.board_size = board_size
        self._board = set([(x, y) for x in range(board_size) for y in range(board_size)])
        self._ship_locations = set()
        self._shot_locations = set()

    def __str__(self):
        nice_board = np.zeros(shape=(self.board_size, self.board_size))

        for (x, y) in self._ship_locations:
            nice_board[x, y] = '1'

        for (x, y) in self._shot_locations:
            nice_board[x, y] = '2'

        return str(nice_board)

    def point_in_board(self, point):
        return point in self._board

    def point_occupied_by_ship(self, point):
        return point in self._ship_locations

    def point_is_shot(self, point):
        return point in self._shot_locations

    def get_shot_locations(self):
        return self._shot_locations

    def get_ship_locations(self):
        return self._ship_locations

    def is_game_won(self):
        return self._shot_locations.issuperset(self._ship_locations)

    def place_ship(self, ship_point_set: set):

        if self._board.issuperset(ship_point_set) and ship_point_set.isdisjoint(self._ship_locations):
            self._ship_locations.update(ship_point_set)
        else:
            raise InvalidShipPlacementException

    def shoot(self, point: Point):

        # Shot off board
        if not self.point_in_board(point):
            raise ShotOffBoardException

        # Point has already been shot
        elif self.point_is_shot(point):
            raise PointAlreadyShotException

        else:
            self._shot_locations.add(point)
