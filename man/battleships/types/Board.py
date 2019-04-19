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

        assert board_size > 0

        self.board_size = board_size
        self._ship_locations = set()
        self._shot_locations = set()

    @property
    def _board(self):
        return frozenset(
            [
                Point(x, y)
                for x in range(self.board_size)
                for y in range(self.board_size)
            ]
        )

    def __str__(self):
        """
        Return a nice string rendered version of the board

        :return: str
        """
        nice_board = np.zeros(shape=(self.board_size, self.board_size))

        for (x, y) in self._ship_locations:
            nice_board[x, y] = "1"

        for (x, y) in self._shot_locations:
            nice_board[x, y] = "2"

        return str(nice_board)

    def point_in_board(self, point):
        """
        Checks to see if 'point' is within the board

        :param point: Tuple
        :return: bool
        """
        return point in self._board

    def point_occupied_by_ship(self, point):
        """
        Checks to see if 'point' on the board is occupied by a ship

        :param point:
        :return:
        """
        return point in self._ship_locations

    def point_is_shot(self, point):
        """
        Checks to see if 'point' on the board has already been shot

        :param point:
        :return:
        """
        return point in self._shot_locations

    def get_shot_locations(self):
        """
        Return a set of all points that have been shot on the board

        :return: Set
        """

        return self._shot_locations

    def get_ship_locations(self):
        """
        Return a set of all points that are occupied by a ship

        :return: Set
        """
        return self._ship_locations

    def is_game_won(self):
        """
        Returns true if the board is currently in a winning state for the other player (i.e, all ships have been shot)

        :return:
        """
        # print(not (self._ship_locations - self._shot_locations))
        # print(self._ship_locations.intersection(self._shot_locations))
        return bool(self._ship_locations) and bool(
            not self._ship_locations.difference(self._shot_locations)
        )

    def place_ship(self, ship: Ship, location: Point, orientation):

        ship_point_set = ship.place(location, orientation)

        if self._board.issuperset(
            ship.place(location, orientation)
        ) and ship_point_set.isdisjoint(self._ship_locations):
            self._ship_locations.update(ship_point_set)
        else:
            raise InvalidShipPlacementException

        return self._ship_locations

    def shoot(self, point: Point):
        """
        Shoot the board location given by 'point'. Will raise ShotOffBoardException if 'point' is not on the board,
        and PointAlreadyShotException if 'point'
        has previously been shot

        :param point:
        :return:
        """

        # Shot off board
        if not self.point_in_board(point):
            raise ShotOffBoardException

        # Point has already been shot
        elif self.point_is_shot(point):
            raise PointAlreadyShotException

        else:
            self._shot_locations.add(point)

            if point in self._ship_locations:
                is_hit = True
            else:
                is_hit = False

            return is_hit
