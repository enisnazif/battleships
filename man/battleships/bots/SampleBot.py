import random
from typing import List

from man.battleships.config import BOARD_SIZE
from man.battleships.game_types import Board
from man.battleships.game_types.Bot import Bot
from man.battleships.game_types.Point import Point
from man.battleships.game_types.Ship import Ship, Orientation


class SampleBot(Bot):
    """ Hello! I am a dumb sample bot who places their ships randomly and shoots randomly! """

    def __init__(self):
        super().__init__()
        self.my_shots = []

    def get_ship_placements(self, ships: List[Ship]):
        """
        Returns a set of point at which a ship will be placed

        :param ships:
        :return: List[Tuple[Ship, Point, Orientation]]
        """

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

    def get_shot(self):

        # Get the status of your last shot - could be useful in planning your next move!

        # last_shot_status looks like:
        # {
        #   shot: Point,
        #   is_hit: bool,
        #   is_sunk: bool,
        #   ship_sunk: ShipType
        # }

        last_shot_status = self.last_shot_status

        x = random.randrange(0, BOARD_SIZE)
        y = random.randrange(0, BOARD_SIZE)

        while Point(x, y) in self.my_shots:
            x = random.randrange(0, BOARD_SIZE)
            y = random.randrange(0, BOARD_SIZE)

        self.my_shots.append(Point(x, y))

        return Point(x, y)
