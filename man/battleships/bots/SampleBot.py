import random
from man.battleships.types.Bot import Bot
from man.battleships.types.Ship import Orientation
from man.battleships.types.Point import Point


class SampleBot(Bot):

    """ Hello! I am a dumb sample bot who places their ships randomly and shoots randomly! """

    def __init__(self, player_name):
        super().__init__(player_name)

    def place_ships(self, ships):
        placements = []

        random_orientation = random.choice(list(Orientation))

        for ship in ships:
            placements.append(ship.place((random.randint(0, 5), random.randint(0, 5)), random_orientation))

        return placements

    def get_shot(self, board):
        x = random.randint(0, 10)
        y = random.randint(0, 10)

        return Point(x, y)
