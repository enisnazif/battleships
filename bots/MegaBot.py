import random
from typing import List, Dict, Union, Tuple

from config import BOARD_SIZE
from game_types import Bot, Board, Point, Ship, ShipType, Orientation


class MegaBot(Bot):
    """ Hello! I am a dumb sample bot who places its ships randomly and shoots randomly! """

    def __init__(self):
        super().__init__()
        self.my_shots = dict()
        self.board = [[BOARD_SIZE] * BOARD_SIZE] * BOARD_SIZE
        self.max_xs = [BOARD_SIZE] * BOARD_SIZE
        self.max_ys = [BOARD_SIZE] * BOARD_SIZE
        self.hunt_mode = False
        self.hunted = set()

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

    @staticmethod
    def vicinity(p):
        return [x for x in [Point(p.x - 1, p.y), Point(p.x + 1, p.y), Point(p.x, p.y - 1), Point(p.x, p.y + 1)]
                if 0 <= x.x < BOARD_SIZE and 0 <= x.y < BOARD_SIZE]

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

        last_shot = self.last_shot_status
        last_point = last_shot.get('shot')
        error = last_shot.get('error')
        if not error:
            self.my_shots[last_point] = last_shot

        is_sunk = last_shot.get('is_sunk', False)
        is_hit = last_shot.get('is_hit', False)

        if is_hit and not is_sunk:
            self.hunt_mode = True
            self.hunted = self.hunted.union(self.vicinity(last_point)) - set(self.my_shots.keys())
        elif is_sunk:
            self.hunt_mode = False

        if not self.hunt_mode:
            x = random.randrange(0, BOARD_SIZE)
            y = random.randrange(0, BOARD_SIZE)

            while Point(x, y) in self.my_shots:
                x = random.randrange(0, BOARD_SIZE)
                y = random.randrange(0, BOARD_SIZE)

            return Point(x, y)
        else:
            return self.hunted.pop()
