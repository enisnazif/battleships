from man.battleships.game_types.Point import Point
from man.battleships.game_types.Ship import Ship, Orientation, ShipType
from man.battleships.exceptions import (
    InvalidShotException,
    InvalidShipPlacementException,
)
from man.battleships.config import BOARD_SIZE
from typing import Tuple, List


class Board:
    def __init__(self, board_size=BOARD_SIZE):

        assert board_size > 0

        self.board_size = board_size
        self._shot_locations = set()
        self._all_ship_locations = set()
        self._individual_ship_locations = dict()  # A dict of sets - one for each ships

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
    def all_ship_locations(self):
        return self._all_ship_locations

    @property
    def individual_ship_locations(self):
        return self._individual_ship_locations

    @property
    def shot_locations(self):
        return self._shot_locations

    @all_ship_locations.setter
    def all_ship_locations(self, value):
        self._all_ship_locations = value

    @individual_ship_locations.setter
    def individual_ship_locations(self, value):
        self._individual_ship_locations = value

    @shot_locations.setter
    def shot_locations(self, value):
        self._shot_locations = value

    def point_in_board(self, point: Point):
        """
        Checks to see if 'point' is within the board

        :param point: Tuple
        :return: bool
        """
        return point in self.board

    def point_occupied_by_ship(self, point: Point):
        """
        Checks to see if 'point' on the board is occupied by a ship

        :param point:
        :return:
        """
        return point in self.all_ship_locations

    def point_is_shot(self, point: Point):
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

        return bool(self.all_ship_locations) and bool(
            not self.all_ship_locations.difference(self.shot_locations)
        )

    def place_ship(self, ship: Ship, location: Point, orientation: Orientation) -> None:
        """
        Places a ship at the given location / orientation
        :param ship:
        :param location:
        :param orientation:
        :return:
        """

        ship_point_set = ship.get_points(location, orientation)
        ship_type = ship.ship_type

        if self.board.issuperset(
                ship.get_points(location, orientation)
        ) and ship_point_set.isdisjoint(self.all_ship_locations):
            self.all_ship_locations.update(ship_point_set)
            self.individual_ship_locations[ship_type] = set(ship_point_set)
        else:
            raise InvalidShipPlacementException(f'Placement of {ship} at {location} in orientation {orientation.value} is invalid')

    def shoot(self, point: Point) -> Tuple[bool, bool, ShipType]:
        """
        Shoot the board location given by 'point'. Will raise ShotOffBoardException if 'point' is not on the board,
        and PointAlreadyShotException if 'point'
        has previously been shot

        :param point:
        :return:
        """

        # Shot off board
        if not self.point_in_board(point):
            raise InvalidShotException(f'{point} is not on the board')

        # Point has already been shot
        elif self.point_is_shot(point):
            raise InvalidShotException(f'{point} has already been shot')

        else:
            self.shot_locations.add(point)
            is_hit = True if point in self.all_ship_locations else False
            is_sunk = False
            ship_sunk = None

            if is_hit:
                # find out which one of the ships was shot
                for k, v in self.individual_ship_locations.items():
                    # (v was the ship that was shot)
                    if point in v:
                        # remove the point from v
                        v.remove(point)
                        if len(v) == 0:
                            is_sunk = True
                            ship_sunk = k

        return is_hit, is_sunk, ship_sunk

    @staticmethod
    def is_valid_ship_placement(placements: List[Tuple[Ship, Point, Orientation]]) -> bool:
        """
        A static helper function that checks to see if ship placements are valid

        :param placements:
        :return:
        """

        all_points = set()

        for ship, point, orientation in placements:
            all_points.update(ship.get_points(point, orientation))

        # Check there are no overlapping placements
        if not len(all_points) == sum([len(s[0]) for s in placements]):
            return False

        # Check all points are within the board
        return all_points.issubset(set([Point(x, y) for x in range(BOARD_SIZE) for y in range(BOARD_SIZE)]))
