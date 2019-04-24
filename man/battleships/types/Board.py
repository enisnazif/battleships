import numpy as np
from man.battleships.types.Point import Point
from man.battleships.types.Ship import Ship, Orientation, ships_to_place
from man.battleships.exceptions import PointAlreadyShotException, ShotOffBoardException, InvalidShipPlacementException
from man.battleships.config import BOARD_SIZE
from typing import Tuple, List

class Board:
    def __init__(self, board_size):

        assert board_size > 0

        self.board_size = board_size
        self._ship_locations = set()
        self._shot_locations = set()

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

    @property
    def board(self):
        return frozenset(
            [
                Point(x, y)
                for x in range(self.board_size)
                for y in range(self.board_size)
            ]
        )

    @property
    def ship_locations(self):
        return self._ship_locations

    @property
    def shot_locations(self):
        return self._shot_locations

    @ship_locations.setter
    def ship_locations(self, value):
        self._ship_locations = value

    @shot_locations.setter
    def shot_locations(self, value):
        self._shot_locations = value

    def point_in_board(self, point):
        """
        Checks to see if 'point' is within the board

        :param point: Tuple
        :return: bool
        """
        return point in self.board

    def point_occupied_by_ship(self, point):
        """
        Checks to see if 'point' on the board is occupied by a ship

        :param point:
        :return:
        """
        return point in self.ship_locations

    def point_is_shot(self, point):
        """
        Checks to see if 'point' on the board has already been shot

        :param point:
        :return:
        """
        return point in self.shot_locations

    def is_board_lost(self):
        """
        Returns true if the board is currently in a losing state for the owning player (i.e, all ships have been shot)

        :return:
        """

        return bool(self._ship_locations) and bool(
            not self.ship_locations.difference(self.shot_locations)
        )

    def place_ship(self, ship: Ship, location: Point, orientation: Orientation):
        """
        Places a ship at the given location / orientation
        :param ship:
        :param location:
        :param orientation:
        :return:
        """

        ship_point_set = ship.get_points(location, orientation)

        if self.board.issuperset(
                ship.get_points(location, orientation)
        ) and ship_point_set.isdisjoint(self.ship_locations):
            self.ship_locations.update(ship_point_set)
        else:
            raise InvalidShipPlacementException

        return self.ship_locations

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
            is_hit = True if point in self.ship_locations else False

        return is_hit

    @staticmethod
    def is_valid_ship_placement(placements: List[Tuple[Ship, Point, Orientation]]):

        all_points = set()

        for ship, point, orientation in placements:
            all_points.update(ship.get_points(point, orientation))

        correct_size = (len(all_points) == sum([len(s[0]) for s in placements]))

        board = set([
            Point(x, y)
            for x in range(BOARD_SIZE)
            for y in range(BOARD_SIZE)
        ])

        return all_points.issubset(board) and correct_size
