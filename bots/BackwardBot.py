import itertools
import random
from typing import List, Tuple

from config import BOARD_SIZE
from game_types import Board, Bot, Point, Ship, Orientation


class BackwardBot(Bot):
    """ Hello! I am a dumb sample bot who shoots sequentially from (9,9) to (0,0) """

    def __init__(self):
        super().__init__()
        self.my_shots = []
        self.points = (i for i in reversed(list(Point(s[1], s[0]) for s in itertools.product(range(BOARD_SIZE), range(BOARD_SIZE)))))

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

        return next(self.points)
