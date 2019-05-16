import random
from typing import List, Dict, Union, Tuple

from config import BOARD_SIZE
from game_types import Bot, Board, Point, Ship, ShipType, Orientation


class Team5Bot(Bot):

    def __init__(self):
        super().__init__()
        self.my_shots = []
        self.hits = []
        self.explored = []
        self.mode = 'search'
        self.to_check = set()


    def get_ship_placements(self, ships: List[Ship]) -> List[Tuple[Ship, Point, Orientation]]:
        """
        Returns a set of point at which a ship will be placed. For each ship, you must return a tuple of [Ship, Point, Orientation],
        where Point corresponds to the bottom left corner of the Ship, e.g:

                     -
        x - - -  or  -
                     -
                     x

        and Orientation is one of Orientation.Vertical and Orientation.Horizontal

        :param ships: A List of Ship which your bot should return placements for
        :return: A list of placements for each ship in 'ships'
        """

        # Perform random ship placement
        while True:
            placements = []
            for ship in ships:
                random_orientation = random.choice(list(Orientation))
                random_point = Point(
                    random.randrange(0, BOARD_SIZE), random.randrange(0, BOARD_SIZE)
                )

                placements.append((ship, random_point, random_orientation))

            if Board.is_valid_ship_placement(placements):
                break

        return placements

    def get_shot(self) -> Point:
        """
        Called each round by the game engine to get the next point to shoot on the opponents board.

        :return: The next point to shoot on the opponents board
        """

        # Get the status of your last shot - could be useful in planning your next move!
        last_shot_status = self.last_shot_status

        # Example response:

        # {
        #    'shot': Point(4, 5),                                # type: Point
        #    'is_hit': True,                                     # type: bool
        #    'is_sunk' True,                                     # type: bool
        #    'ship_sunk': <ShipType.Battleship: 'Battleship'>,   # type: ShipType
        #    'error': None                                       # type: Union[None, Exception]
        # }

        last_pt = self.last_shot_status['shot']
        self.explored.append(last_pt)

        if last_shot_status['is_hit']:
            self.hits.append(last_pt)
            self.mode = 'destroy'
            self._destroy_area(last_pt)

        if self.mode == 'destroy':
            try:
                pt = self.to_check.pop()
            except KeyError:
                self.mode = 'search'

        if self.mode == 'search':
            pt = staircase(last_shot_status, step_size=2)

        self.my_shots.append(pt)

        return pt

    def _destroy_area(self, pt):
        search_area = [
            Point(pt.x - 1, pt.y),
            Point(pt.x + 1, pt.y),
            Point(pt.x, pt.y - 1),
            Point(pt.x, pt.y + 1),
        ]
        for p in search_area:
            if _is_valid(p) and p not in self.explored:
                self.to_check.add(p)


def _is_valid(pt):
    return pt.x < BOARD_SIZE and pt.x >= 0 and pt.y < BOARD_SIZE and pt.y >= 0


def staircase(last_shot_status, step_size):
    if last_shot_status['shot'] is None:
        return Point(0, 0)
    last_pt = last_shot_status['shot']
    y = last_pt.y
    x = last_pt.x + step_size
    if x >= BOARD_SIZE:
        y = (y + 1) % BOARD_SIZE
        x = x % BOARD_SIZE
    return Point(x, y)
