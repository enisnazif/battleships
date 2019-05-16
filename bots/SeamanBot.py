import random
from typing import List, Dict, Union, Tuple
from collections import namedtuple

from config import BOARD_SIZE
from game_types import Bot, Board, Point, Ship, ShipType, Orientation

NEIGHBOURS = [
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 0),
]

BoardPoint = namedtuple('BoardPoint', ['is_shot', 'is_hit', 'is_sunk'])


def get_left_count(board, x, y):
    i = 0
    while True:
        i += 1
        if x - i < 0:
            break
        if board[x - i][y][0] == 1:
            break
    return i - 1


def get_right_count(board, x, y):
    i = 0
    while True:
        i += 1
        if x + i >= BOARD_SIZE:
            break
        if board[x + i][y][0] == 1:
            break
    return i - 1


def get_top_count(board, x, y):
    i = 0
    while True:
        i += 1
        if y - i < 0:
            break
        if board[x][y - i][0] == 1:
            break
    return i - 1


def get_bottom_count(board, x, y):
    i = 0
    while True:
        i += 1
        if y + i <= BOARD_SIZE:
            break
        if board[x][y + i][0] == 1:
            break
    return i - 1


def is_valid_point(point: Point) -> bool:
    if point.x < 0:
        return False
    if point.y < 0:
        return False
    if point.x >= BOARD_SIZE:
        return False
    if point.y >= BOARD_SIZE:
        return False
    return True


def get_neighbours(point: Point) -> List[Point]:
    neighbours = []
    for x, y in NEIGHBOURS:
        neighbour = Point(point.x + x, point.y + y)
        if is_valid_point(neighbour):
            neighbours.append(neighbour)
    return neighbours


# def get_forward_point(point1: Point, point2: Point):
#     if not point1.x == point2.x or point1.y == point2.y:
#         return None
#     if point1.x == point2.x:
#         if abs(point1.y)


class SeamanBot(Bot):
    """ Hello! I am a dumb sample bot who places its ships randomly and shoots randomly! """

    def __init__(self):
        super().__init__()
        self.my_shots = []
        self.ships = []
        self.remaining_ships = []
        self.last_responses = []
        self.check_first = []
        self.hits = set()

        self.board = []

        for x in range(BOARD_SIZE):
            row = []
            self.board.append(row)
            for y in range(BOARD_SIZE):
                row.append([0, 0, 0])

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
        placements = [
            (ships[0],
             Point(2, 4),
             Orientation.Vertical),
            (ships[1],
             Point(1, 0),
             Orientation.Horizontal),
            (ships[2],
             Point(8, 3),
             Orientation.Vertical),
            (ships[3],
             Point(4, 5),
             Orientation.Vertical),
            (ships[4],
             Point(1, 2),
             Orientation.Horizontal),
        ]  # lol
        return placements


    def get_shot(self) -> Point:
        """
        Called each round by the game engine to get the next point to shoot on the opponents board.

        :return: The next point to shoot on the opponents board
        """

        # Get the status of your last shot - could be useful in planning your next move!
        last_shot_status = self.last_shot_status
        self.last_responses.append(last_shot_status)

        # Example response:

        # {
        #    'shot': Point(4, 5),                                # type: Point
        #    'is_hit': True,                                     # type: bool
        #    'is_sunk' True,                                     # type: bool
        #    'ship_sunk': <ShipType.Battleship: 'Battleship'>,   # type: ShipType
        #    'error': None                                       # type: Union[None, Exception]
        # }

        if last_shot_status['is_hit']:
            last_shot = last_shot_status['shot']
            self.board[last_shot.x][last_shot.y][1] = 1

            if last_shot_status['is_sunk']:
                self.board[last_shot.x][last_shot.y][2] = 1

        next_score = {}

        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if self.board[x][y][1] == 1:
                    hit_neighbours = get_neighbours(Point(x, y))
                    for neighbour in hit_neighbours:
                        if neighbour not in self.my_shots:
                            return self.shoot(neighbour)

                if self.board[x][y][0] == 0:
                    left_count = min(get_left_count(self.board, x, y), 5)
                    right_count = min(get_right_count(self.board, x, y), 5)
                    top_count = min(get_top_count(self.board, x, y), 5)
                    bottom_count = min(get_bottom_count(self.board, x, y), 5)
                    next_score[Point(x, y)] = left_count ** 2 + right_count ** 2 + top_count ** 2 + bottom_count ** 2

        next_score_sorted = sorted(next_score.items(), key=lambda x: x[1], reverse=True)
        # print(next_score_sorted)

        # print(next_score_sorted)
        # exit(1)

        return self.shoot(next_score_sorted[0][0])


        x = random.randrange(0, BOARD_SIZE)
        y = random.randrange(0, BOARD_SIZE)

        while Point(x, y) in self.my_shots:
            x = random.randrange(0, BOARD_SIZE)
            y = random.randrange(0, BOARD_SIZE)

        return self.shoot(Point(x, y))

    def shoot(self, point: Point) -> Point:
        self.board[point.x][point.y][0] = 1
        self.my_shots.append(point)
        return point