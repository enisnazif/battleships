import random
from typing import List, Dict, Union
from config import BOARD_SIZE
from game_types import Bot, Board, Point, Ship, ShipType, Orientation


class SampleBot(Bot):
    """ Hello! I am a dumb sample bot who places their ships randomly and shoots randomly! """

    def __init__(self):
        super().__init__()
        self.my_shots = []

    def get_ship_placements(self, ships: List[Ship]):
        """
        Returns a set of point at which a ship will be placed. When specifying a point at which to place your ship, this corresponds to the bottom, left-most
        point of the ship.


                           -
        e.g:  x - - -  or  -
                           -
                           x

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
        """
        Return a single point corresponding to the location of where you want your bot to shoot next

        :return: Point
        """

        # Get the status of your last shot - could be useful in planning your next move!
        last_shot_status = self.last_shot_status  # type: Dict[str, Union[Point, bool, bool, ShipType, None]]

        x = random.randrange(0, BOARD_SIZE)
        y = random.randrange(0, BOARD_SIZE)

        while Point(x, y) in self.my_shots:
            x = random.randrange(0, BOARD_SIZE)
            y = random.randrange(0, BOARD_SIZE)

        self.my_shots.append(Point(x, y))

        return Point(x, y)
