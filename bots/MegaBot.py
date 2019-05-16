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
        self.hit_xs = [BOARD_SIZE] * BOARD_SIZE
        self.hit_ys = [BOARD_SIZE] * BOARD_SIZE
        self.hunt_mode = False
        self.hunted = set()

    def get_ship_placements(self, ships: List[Ship]) -> List[Tuple[Ship,
                                                                   Point, Orientation]]:
        """
        Returns a set of point at which a ship will be placed. For each
ship, you must return a tuple of [Ship, Point, Orientation],
        where Point corresponds to the bottom left corner of the Ship, e.g:

                     -
        x - - -  or  -
                     -
                     x

        and Orientation is one of Orientation.Vertical and
Orientation.Horizontal

        :param ships: A List of Ship which your bot should return
placements for
        :return: A list of placements for each ship in 'ships'
        """
        PLACEMENTS = [
            [
                (ships[0], Point(1, 1), Orientation.Horizontal),
                (ships[1], Point(7, 2), Orientation.Vertical),
                (ships[2], Point(6, 8), Orientation.Horizontal),
                (ships[3], Point(2, 7), Orientation.Horizontal),
                (ships[4], Point(1, 4), Orientation.Horizontal),
            ],
        ]

        ships = sorted(ships, key=lambda x: len(x), reverse=True)
        return random.choice(PLACEMENTS)

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
            if last_point:
                x = last_point.x
                y = last_point.y
                mx, my = 0, 0
                for i in range(BOARD_SIZE):
                    if Point(i, y) in self.my_shots:
                        mx += 1
                    if Point(x, i) in self.my_shots:
                        my += 1

                self.hit_xs[x] = mx
                self.hit_ys[y] = my

            self.my_shots[last_point] = last_shot
            is_sunk = last_shot.get('is_sunk', False)
            is_hit = last_shot.get('is_hit', False)

            if is_hit and not is_sunk:
                self.hunt_mode = True
                self.hunted = self.hunted.union(self.vicinity(last_point)) - set(self.my_shots.keys())
            elif is_sunk:
                self.hunt_mode = False

        if not self.hunt_mode:
            min_x = min(self.hit_xs)
            min_y = min(self.hit_ys)

            ix = [i for i, v in enumerate(self.hit_xs) if v == min_x]
            iy = [i for i, v in enumerate(self.hit_ys) if v == min_y]

            x = random.randrange(0, BOARD_SIZE)
            y = random.randrange(0, BOARD_SIZE)

            while Point(x, y) in self.my_shots:
                x = random.randrange(0, BOARD_SIZE)
                y = random.randrange(0, BOARD_SIZE)

            return Point(x, y)
        else:
            return self.hunted.pop()
